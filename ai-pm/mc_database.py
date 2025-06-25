#!/usr/bin/env python3
# mc_database.py - Database operations only

import sqlite3
from datetime import datetime
from contextlib import contextmanager

class Database:
    def __init__(self, db_path="/database/aipm.db"):
        self.db_path = db_path
        self.init_tables()
    
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
    
    def init_tables(self):
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
            
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_username ON Users(minecraft_username)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_online ON Users(is_online)")
    
    def add_user(self, username):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR IGNORE INTO Users (minecraft_username, last_updated)
                VALUES (?, ?)
            """, (username, datetime.now()))
    
    def set_online(self, username, online=True):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE Users 
                SET is_online = ?, last_updated = ?
                WHERE minecraft_username = ?
            """, (online, datetime.now(), username))
    
    def update_position(self, username, x, y, z):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE Users 
                SET current_x = ?, current_y = ?, current_z = ?, last_updated = ?
                WHERE minecraft_username = ?
            """, (x, y, z, datetime.now(), username))
    
    def update_inventory(self, username, item_type, quantity):
        with self.get_connection() as conn:
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
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT minecraft_username, current_x, current_y, current_z, last_updated
                FROM Users WHERE is_online = 1
                ORDER BY minecraft_username
            """)
            return [dict(row) for row in cursor.fetchall()]
    
    def get_user_inventory(self, username):
        with self.get_connection() as conn:
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
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT minecraft_username, is_online, current_x, current_y, current_z, last_updated
                FROM Users
                ORDER BY minecraft_username
            """)
            return [dict(row) for row in cursor.fetchall()]
    
    def cleanup_offline_users(self, hours=24):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM Users 
                WHERE is_online = 0 
                AND datetime(last_updated) < datetime('now', '-{} hours')
            """.format(hours))
            return cursor.rowcount