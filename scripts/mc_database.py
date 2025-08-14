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
        tables = ['Users', 'UserInventory', 'BuildRecipes', 'GameMap']
        
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


class UserDataService:
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