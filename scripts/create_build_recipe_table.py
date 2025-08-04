#!/usr/bin/env python3
# file: create_build_recipe_table.py
# desc: Populates table for build recipes

from mc_database import Database
from nbt_client import SchematicReader
from collections import Counter
import re

def parse_block_state(block_state_str):
    """Parse minecraft block state into item_type and attributes"""
    if '[' in block_state_str:
        # Has attributes: minecraft:iron_trapdoor[facing=north,half=bottom,...]
        item_type = block_state_str.split('[')[0]
        attributes = '[' + block_state_str.split('[')[1]
        return item_type, attributes
    else:
        # No attributes: minecraft:iron_block
        return block_state_str, None

def get_block_counts(schematic_reader):
    """Get block counts from a schematic file"""
    palette = schematic_reader.get_block_palette()
    block_data = schematic_reader.get_block_data()
    
    # Convert palette indices to block names and count them
    index_to_block = {v: k for k, v in palette.items()}
    block_names = [index_to_block[idx] for idx in block_data]
    
    return Counter(block_names)


def insert_build_recipe(db, structure_id, build_requirements):
    """Insert build requirements into database"""
    with db.get_connection() as conn:
        cursor = conn.cursor()
        
        for block_state, quantity in build_requirements.items():
            item_type, attributes = parse_block_state(block_state)
            
            cursor.execute("""
                INSERT OR REPLACE INTO BuildRecipes 
                (structure_id, item_type, item_attributes, quantity)
                VALUES (?, ?, ?, ?)
            """, (structure_id, item_type, attributes, quantity))
            
            print(f"  Added: {item_type} {attributes or ''} x{quantity}")


def process_structure(db, structure_id, complete_file, init_file):
    """Process a single structure pair and populate database"""
    print(f"\n=== Processing Structure {structure_id} ===")
    
    try:
        # Load complete structure
        print(f"Loading complete: {complete_file}")
        complete_schem = SchematicReader(complete_file)
        complete_schem.load()
        
        # Load init structure
        print(f"Loading init: {init_file}")
        init_schem = SchematicReader(init_file)
        init_schem.load()
        
        # Calculate build requirements
        print("Calculating build requirements...")
        
        # Get block counts from both schematics
        complete_blocks = get_block_counts(complete_schem)
        init_blocks = get_block_counts(init_schem)
        
        # Calculate what needs to be added (complete - init)
        build_requirements = {}
        for block_state, complete_count in complete_blocks.items():
            # Skip dirt blocks - they're created when grass blocks are built on
            if block_state == 'minecraft:dirt':
                continue
                
            init_count = init_blocks.get(block_state, 0)
            needed = complete_count - init_count
            if needed > 0:
                build_requirements[block_state] = needed
        
        print(f"Found {len(build_requirements)} different block types needed")
        print(f"Total blocks to add: {sum(build_requirements.values())}")
        
        # Insert into database
        if build_requirements:
            insert_build_recipe(db, structure_id, build_requirements)
            print(f"✅ Successfully populated structure {structure_id}")
        else:
            print(f"⚠️  No build requirements found for structure {structure_id}")
            
    except Exception as e:
        print(f"❌ Error processing structure {structure_id}: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":

    print("🏗️  Starting Build Recipe Table Population")
    
    # Initialize database
    db = Database()
    db.init_tables()
    
    # Clear existing build recipes (for clean testing)
    with db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM BuildRecipes")
        print("🧹 Cleared existing build recipes")
    
    for i in range(1,13):
        # Process structure 1
        structure_complete = f"/mc-data/plugins/WorldEdit/schematics/{i}_complete.schem"
        structure_init = f"/mc-data/plugins/WorldEdit/schematics/{i}_init.schem"
        process_structure(db, i, structure_complete, structure_init)