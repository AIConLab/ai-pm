#!/usr/bin/env python3
# mc_database.py - Database operations only

import sqlite3
from datetime import datetime
from contextlib import contextmanager
import json
import os



class Database:
    def __init__(self, db_path="/app/database/aipm.db", user_config=None):
        self.db_path = db_path
        self.user_config = user_config
    
    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def init_round_data_table(self):
        """
        Initialize the RoundData table with proper foreign key references.
        This should be done after 
        
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS RoundData (
                    round_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    current_round INTEGER NOT NULL,
                    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)


            # Junction table for RoundData -> BuildRecipes relationships  
            # Matches current round number to structure number 
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS RoundData_BuildRecipes (
                    round_id INTEGER,
                    recipe_id INTEGER,
                    PRIMARY KEY (round_id, recipe_id),
                    FOREIGN KEY (round_id) REFERENCES RoundData (round_id),
                    FOREIGN KEY (recipe_id) REFERENCES BuildRecipes (recipe_id)
                )
            """)
            
            # Junction table for RoundData -> GameMap relationships
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS RoundData_GameMap (
                    round_id INTEGER,
                    waypoint_id INTEGER,
                    PRIMARY KEY (round_id, waypoint_id),
                    FOREIGN KEY (round_id) REFERENCES RoundData (round_id),
                    FOREIGN KEY (waypoint_id) REFERENCES GameMap (waypoint_id)
                )
            """)

            # Game map is static so we use that update that table now...
            # TODO:
            
            
            # Junction table for RoundData -> ProcessingArea relationships
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS RoundData_ProcessingArea (
                    round_id INTEGER,
                    item_id INTEGER,
                    PRIMARY KEY (round_id, item_id),
                    FOREIGN KEY (round_id) REFERENCES RoundData (round_id),
                    FOREIGN KEY (item_id) REFERENCES ProcessingArea (item_id)
                )
            """)


            # Processing Area is static so we use that update that table now...
            # TODO:
            
            
            # Junction table for RoundData -> ResourceArea relationships
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS RoundData_ResourceArea (
                    round_id INTEGER,
                    item_id INTEGER,
                    PRIMARY KEY (round_id, item_id),
                    FOREIGN KEY (round_id) REFERENCES RoundData (round_id),
                    FOREIGN KEY (item_id) REFERENCES ResourceArea (item_id)
                )
            """)


            # Resource Area is static so we use that update that table now...
            # TODO:
            
            # Create indexes for better performance
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_round_data_round ON RoundData(current_round)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_round_data_updated ON RoundData(last_updated)")

    def init_resource_area_table(self):
        """Initialize the ProcessingArea table"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            
            # Create new table without quantity column
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ResourceArea (
                    item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    item_type TEXT NOT NULL,
                    item_attributes TEXT,
                    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(item_type, item_attributes)
                )
            """)
            
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_processing_area_item_type ON ProcessingArea(item_type)")

    def init_processing_area_table(self):
        """Initialize the ProcessingArea table"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            
            # Create new table without quantity column
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ProcessingArea (
                    item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    item_type TEXT NOT NULL,
                    item_attributes TEXT,
                    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(item_type, item_attributes)
                )
            """)
            
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_processing_area_item_type ON ProcessingArea(item_type)")

    def init_user_data_table(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    minecraft_username TEXT UNIQUE NOT NULL,
                    is_online BOOLEAN DEFAULT 0,
                    current_x REAL DEFAULT 0.0,
                    current_y REAL DEFAULT 0.0,
                    current_z REAL DEFAULT 0.0,
                    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_username ON Users(minecraft_username)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_online ON Users(is_online)")

    def init_user_inventory_table(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS UserInventory (
                    inventory_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    item_type TEXT NOT NULL,
                    quantity INTEGER DEFAULT 0,
                    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES Users (user_id),
                    UNIQUE(user_id, item_type)
                )
            """)

    def init_build_recipes_table(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS BuildRecipes (
                    recipe_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    structure_id INTEGER NOT NULL,
                    item_type TEXT NOT NULL,
                    item_attributes TEXT,
                    quantity INTEGER NOT NULL,
                    UNIQUE(structure_id, item_type, item_attributes)
                )
            """)
            
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_build_recipes_structure ON BuildRecipes(structure_id)")

    def init_map_table(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Create the GameMap table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS GameMap (
                    waypoint_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    waypoint_name TEXT UNIQUE NOT NULL,
                    waypoint_type TEXT NOT NULL,
                    x REAL NOT NULL,
                    y REAL NOT NULL,
                    z REAL NOT NULL,
                    description TEXT,
                    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create index for faster lookups
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_waypoint_name ON GameMap(waypoint_name)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_waypoint_type ON GameMap(waypoint_type)")
            
            # If config is provided, populate the table with waypoint data
            if self.user_config and 'minecraft' in self.user_config:
                minecraft_config = self.user_config['minecraft']
                
                # Define the waypoints mapping
                waypoint_mappings = {
                    'build_area_xyz': {
                        'name': 'build_area',
                        'type': 'build',
                        'description': 'Main building and construction area'
                    },
                    'resource_area_xyz': {
                        'name': 'resource_area', 
                        'type': 'resource',
                        'description': 'Resource gathering and mining area'
                    },
                    'processing_area_xyz': {
                        'name': 'processing_area',
                        'type': 'processing', 
                        'description': 'Item processing and crafting area'
                    }
                }
                
                # Clear existing waypoints first (in case config changed)
                cursor.execute("DELETE FROM GameMap")

                # Reset the auto-increment counter to start from 1
                cursor.execute("DELETE FROM sqlite_sequence WHERE name='GameMap'")
                
                # Insert waypoints from config
                for config_key, waypoint_info in waypoint_mappings.items():
                    if config_key in minecraft_config:
                        coords = minecraft_config[config_key]
                        
                        # Ensure we have exactly 3 coordinates
                        if len(coords) >= 3:
                            cursor.execute("""
                                INSERT INTO GameMap (waypoint_name, waypoint_type, x, y, z, description, last_updated)
                                VALUES (?, ?, ?, ?, ?, ?, ?)
                            """, (
                                waypoint_info['name'],
                                waypoint_info['type'],
                                float(coords[0]),  # x
                                float(coords[1]),  # y  
                                float(coords[2]),  # z
                                waypoint_info['description'],
                                datetime.now()
                            ))
                            
                            print(f"✅ Added waypoint: {waypoint_info['name']} at ({coords[0]}, {coords[1]}, {coords[2]})")
                        else:
                            print(f"❌ Invalid coordinates for {config_key}: {coords}")

    def init_tables(self):
        try:
            self.init_user_data_table()
            self.init_user_inventory_table()
            self.init_build_recipes_table()
            self.init_map_table()
            self.init_processing_area_table()
            self.init_resource_area_table()
            self.init_round_data_table()

        except Exception as e:
            raise e

    def export_table_to_json(self, table_name, output_dir="/app/exports"):
        """Export a single table to JSON file"""
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        output_file = os.path.join(output_dir, f"{table_name.lower()}.json")
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Get all data from table
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            
            if not rows:
                print(f"⚠️  Table {table_name} is empty")
                # Still create empty JSON file
                with open(output_file, 'w', encoding='utf-8') as jsonfile:
                    json.dump([], jsonfile, indent=2)
                return output_file
            
            # Convert rows to list of dictionaries
            data = [dict(row) for row in rows]
            
            # Write JSON with nice formatting
            with open(output_file, 'w', encoding='utf-8') as jsonfile:
                json.dump(data, jsonfile, indent=2, ensure_ascii=False)
            
            print(f"✅ Exported {len(rows)} rows from {table_name} to {output_file}")
            return output_file

    def export_all_tables_to_json(self, output_dir="/app/exports"):
        """Export all tables to JSON files"""
        tables = [
            'Users', 
            'UserInventory', 
            'BuildRecipes', 
            'GameMap', 
            'ProcessingArea',
            'ResourceArea',
            'RoundData',
            'RoundData_BuildRecipes',
            'RoundData_GameMap', 
            'RoundData_ProcessingArea',
            'RoundData_ResourceArea'
        ]
        
        print(f"📁 Exporting all tables to {output_dir}")
        exported_files = []
        
        for table in tables:
            try:
                file_path = self.export_table_to_json(table, output_dir)
                exported_files.append(file_path)
            except Exception as e:
                print(f"❌ Failed to export {table}: {e}")
        
        print(f"🎯 Export complete! Files: {len(exported_files)}")
        return exported_files

class RoundDataService:
    """
    Service class to update RoundData Table in DB
    """
    def __init__(self, db: Database):
        self.db = db

    def update_current_round_number(self, round_num):
        """
        Update or insert the current round number in RoundData table.
        Only updates if the round has actually changed.
        """
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            
            # Check if we already have this round number
            cursor.execute("""
                SELECT round_id, current_round FROM RoundData 
                ORDER BY last_updated DESC 
                LIMIT 1
            """)
            
            existing_round = cursor.fetchone()
            
            if existing_round and existing_round['current_round'] == round_num:
                # Round hasn't changed, just update timestamp
                cursor.execute("""
                    UPDATE RoundData 
                    SET last_updated = ? 
                    WHERE round_id = ?
                """, (datetime.now(), existing_round['round_id']))
                
                print(f"🔄 Round {round_num} still active (round_id: {existing_round['round_id']})")
                return existing_round['round_id']
            else:
                # Round has changed, clear old data and insert new
                cursor.execute("DELETE FROM RoundData")
                
                # Insert the new current round
                cursor.execute("""
                    INSERT INTO RoundData (current_round, last_updated)
                    VALUES (?, ?)
                """, (round_num, datetime.now()))
                
                # Get the round_id that was just inserted
                round_id = cursor.lastrowid
                print(f"✅ NEW round detected: {round_num} (round_id: {round_id})")
                
                return round_id

    def update_current_round_links(self, round_num):
        """
        Update all RoundData junction tables to link the current round with:
        - BuildRecipes for the corresponding structure_id
        - All GameMap waypoints (static data)
        - All ProcessingArea items (static data) 
        - All ResourceArea items (static data)
        """
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            
            # Get the current round_id from RoundData
            cursor.execute("SELECT round_id FROM RoundData WHERE current_round = ?", (round_num,))
            result = cursor.fetchone()
            
            if not result:
                print(f"❌ No round data found for round {round_num}")
                return
            
            round_id = result['round_id']
            
            # Check if we already have any links for this round_id
            cursor.execute("""
                SELECT COUNT(*) as link_count 
                FROM RoundData_BuildRecipes 
                WHERE round_id = ?
            """, (round_id,))
            
            existing_links = cursor.fetchone()['link_count']
            
            if existing_links > 0:
                print(f"🔄 Round {round_num} already linked to all data")
                return
            
            # Link to BuildRecipes for current structure
            cursor.execute("""
                SELECT recipe_id FROM BuildRecipes 
                WHERE structure_id = ?
            """, (round_num,))
            
            recipes = cursor.fetchall()
            for recipe in recipes:
                cursor.execute("""
                    INSERT INTO RoundData_BuildRecipes (round_id, recipe_id)
                    VALUES (?, ?)
                """, (round_id, recipe['recipe_id']))
            
            # Link to all GameMap waypoints (static)
            cursor.execute("SELECT waypoint_id FROM GameMap")
            waypoints = cursor.fetchall()
            for waypoint in waypoints:
                cursor.execute("""
                    INSERT INTO RoundData_GameMap (round_id, waypoint_id)
                    VALUES (?, ?)
                """, (round_id, waypoint['waypoint_id']))
            
            # Link to all ProcessingArea items (static)
            cursor.execute("SELECT item_id FROM ProcessingArea")
            processing_items = cursor.fetchall()
            for item in processing_items:
                cursor.execute("""
                    INSERT INTO RoundData_ProcessingArea (round_id, item_id)
                    VALUES (?, ?)
                """, (round_id, item['item_id']))
            
            # Link to all ResourceArea items (static)
            cursor.execute("SELECT item_id FROM ResourceArea")
            resource_items = cursor.fetchall()
            for item in resource_items:
                cursor.execute("""
                    INSERT INTO RoundData_ResourceArea (round_id, item_id)
                    VALUES (?, ?)
                """, (round_id, item['item_id']))
            
            print(f"✅ NEW round: Linked {len(recipes)} recipes, {len(waypoints)} waypoints, {len(processing_items)} processing items, {len(resource_items)} resource items")

    def clear_round_data(self):
        """
        Clear all round data (useful for testing or reset)
        """
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            
            # Clear junction tables first (foreign key constraints)
            cursor.execute("DELETE FROM RoundData_BuildRecipes")
            cursor.execute("DELETE FROM RoundData_GameMap") 
            cursor.execute("DELETE FROM RoundData_ProcessingArea")
            cursor.execute("DELETE FROM RoundData_ResourceArea")
            
            # Clear main table
            cursor.execute("DELETE FROM RoundData")
            
            print("✅ Cleared all round data")

class UserDataService:
    """
    Service class to update UserData Table in DB
    """
    def __init__(self, db: Database):
        self.db = db
    
    def add_user(self, username):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR IGNORE INTO Users (minecraft_username, last_updated)
                VALUES (?, ?)
            """, (username, datetime.now()))

    def set_online(self, username, online=True):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE Users 
                SET is_online = ?, last_updated = ?
                WHERE minecraft_username = ?
            """, (online, datetime.now(), username))

    def update_position(self, username, x, y, z):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE Users 
                SET current_x = ?, current_y = ?, current_z = ?, last_updated = ?
                WHERE minecraft_username = ?
            """, (x, y, z, datetime.now(), username))

    def update_inventory(self, username, item_type, quantity):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            
            # Get user_id first
            cursor.execute("SELECT user_id FROM Users WHERE minecraft_username = ?", (username,))
            result = cursor.fetchone()
            if not result:
                return
            
            user_id = result['user_id']
            cursor.execute("""
                INSERT OR REPLACE INTO UserInventory (user_id, item_type, quantity, last_updated)
                VALUES (?, ?, ?, ?)
            """, (user_id, item_type, quantity, datetime.now()))

    def get_online_users(self):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT minecraft_username, current_x, current_y, current_z, last_updated
                FROM Users WHERE is_online = 1
                ORDER BY minecraft_username
            """)
            return [dict(row) for row in cursor.fetchall()]

    def get_user_inventory(self, username):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT ui.item_type, ui.quantity, ui.last_updated
                FROM UserInventory ui
                JOIN Users u ON ui.user_id = u.user_id
                WHERE u.minecraft_username = ?
                ORDER BY ui.item_type
            """, (username,))
            return [dict(row) for row in cursor.fetchall()]

    def get_all_users(self):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT minecraft_username, is_online, current_x, current_y, current_z, last_updated
                FROM Users
                ORDER BY minecraft_username
            """)
            return [dict(row) for row in cursor.fetchall()]

    def cleanup_offline_users(self, hours=24):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM Users 
                WHERE is_online = 0 
                AND datetime(last_updated) < datetime('now', '-{} hours')
            """.format(hours))
            return cursor.rowcount

    def delete_user(self, username):
        """Delete user and all associated data from database"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            
            # Get user_id first
            cursor.execute("SELECT user_id FROM Users WHERE minecraft_username = ?", (username,))
            result = cursor.fetchone()
            if not result:
                return 0  # User doesn't exist
            
            user_id = result['user_id']
            
            # Delete inventory records first (foreign key constraint)
            cursor.execute("DELETE FROM UserInventory WHERE user_id = ?", (user_id,))
            
            # Delete user record
            cursor.execute("DELETE FROM Users WHERE user_id = ?", (user_id,))
            
            return cursor.rowcount  # Returns 1 if user was deleted, 0 if not found

    def delete_users_not_in_list(self, allowed_usernames):
        """Delete all users not in the allowed list"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            
            if not allowed_usernames:
                # If no allowed users, delete everyone
                cursor.execute("DELETE FROM UserInventory")
                cursor.execute("DELETE FROM Users")
                return cursor.rowcount
            
            # Create placeholders for the IN clause
            placeholders = ','.join('?' * len(allowed_usernames))
            
            # Get user_ids to delete
            cursor.execute(f"""
                SELECT user_id FROM Users 
                WHERE minecraft_username NOT IN ({placeholders})
            """, allowed_usernames)
            
            user_ids_to_delete = [row['user_id'] for row in cursor.fetchall()]
            
            if user_ids_to_delete:
                # Delete inventory records first
                placeholders_ids = ','.join('?' * len(user_ids_to_delete))
                cursor.execute(f"DELETE FROM UserInventory WHERE user_id IN ({placeholders_ids})", user_ids_to_delete)
                
                # Delete user records
                cursor.execute(f"DELETE FROM Users WHERE user_id IN ({placeholders_ids})", user_ids_to_delete)
            
            return len(user_ids_to_delete)

    def clear_user_inventory(self, username):
        """Clear all inventory items for a specific user"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            
            # Get user_id first
            cursor.execute("SELECT user_id FROM Users WHERE minecraft_username = ?", (username,))
            result = cursor.fetchone()
            if not result:
                return 0
            
            user_id = result['user_id']
            cursor.execute("DELETE FROM UserInventory WHERE user_id = ?", (user_id,))
            return cursor.rowcount

    def replace_user_inventory(self, username, inventory_dict):
        """Replace entire inventory for a user (clear old + add new)"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            
            # Get user_id first
            cursor.execute("SELECT user_id FROM Users WHERE minecraft_username = ?", (username,))
            result = cursor.fetchone()
            if not result:
                return
            
            user_id = result['user_id']
            
            # Clear existing inventory
            cursor.execute("DELETE FROM UserInventory WHERE user_id = ?", (user_id,))
            
            # Add new inventory items
            for item_type, quantity in inventory_dict.items():
                cursor.execute("""
                    INSERT INTO UserInventory (user_id, item_type, quantity, last_updated)
                    VALUES (?, ?, ?, ?)
                """, (user_id, item_type, quantity, datetime.now()))