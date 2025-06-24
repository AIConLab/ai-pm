#!/usr/bin/env python3
# mc_database.py
import sqlite3
import threading
import time
from datetime import datetime
from contextlib import contextmanager

class Database:
    def __init__(self, db_path="/mc-data/players.db"):
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
    
    def get_online_users(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT minecraft_username, current_x, current_y, current_z
                FROM Users WHERE is_online = 1
            """)
            return [dict(row) for row in cursor.fetchall()]

