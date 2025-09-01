#!/usr/bin/env python3
# file: create_processing_area_table.py
# desc: Inits datatable for processing area items - VERIFICATION MODE

from mc_database import Database
from nbt_client import SchematicReader
from collections import Counter
from datetime import datetime
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

def get_chest_contents(schematic_reader):
    """Extract items from all chests in the schematic"""
    block_entities = schematic_reader.get_block_entities()
    chest_items = set()
    
    print(f"\n=== ANALYZING CHEST CONTENTS ===")
    print(f"Found {len(block_entities)} block entities")
    
    for be in block_entities:
        entity_id = be.get('id', '')
        position = be.get('position', [0, 0, 0])
        
        print(f"Block entity: {entity_id} at {position}")
        
        # Check if this is a chest
        if 'chest' in entity_id.lower():
            data = be.get('data', {})
            items = data.get('Items', [])
            
            print(f"  📦 Found chest with {len(items)} item types")
            
            for item in items:
                if isinstance(item, dict):
                    item_id = str(item.get('id', ''))
                    count = int(item.get('Count', 0))
                    slot = int(item.get('Slot', -1))
                    
                    if item_id:
                        chest_items.add(item_id)
                        print(f"    - {item_id} x{count} (slot {slot})")
                else:
                    print(f"    - Unexpected item format: {item}")
    
    return chest_items

def get_unique_blocks(schematic_reader):
    """Get unique block types from a schematic file (no counts needed)"""
    palette = schematic_reader.get_block_palette()
    block_data = schematic_reader.get_block_data()
    
    # Convert palette indices to block names and get unique set
    index_to_block = {v: k for k, v in palette.items()}
    block_names = [index_to_block[idx] for idx in block_data]
    
    # Return both the counter (for debug) and unique set
    block_counts = Counter(block_names)
    unique_blocks = set(block_names)
    
    return block_counts, unique_blocks

def filter_excluded_blocks(unique_blocks, excluded_blocks):
    """Remove excluded blocks from the unique blocks set"""
    excluded_full_names = set()
    for block in excluded_blocks:
        excluded_full_names.add(f"minecraft:{block}")
        excluded_full_names.add(block)
    
    filtered_blocks = set()
    excluded_found = set()
    
    for block_state in unique_blocks:
        # Check if this block should be excluded
        block_name = block_state.split('[')[0]  # Remove attributes for comparison
        if block_name not in excluded_full_names and block_state not in excluded_full_names:
            filtered_blocks.add(block_state)
        else:
            excluded_found.add(block_state)
    
    return filtered_blocks, excluded_found

def analyze_processing_area(schematic_file):
    """Analyze processing area schematic and print results for verification"""
    print(f"\n=== ANALYZING PROCESSING AREA ===")
    
    # Blocks to exclude from the processing area inventory
    excluded_blocks = ['sea_lantern', 
    'bedrock', 
    'light_gray_concrete',
    'stone_brick',
    'stone_brick_slab',
    'end_rod',
    'bamboo_hanging_sign',
    'bamboo_fence',
    'air',
    'spruce_fence',
    'dark_oak_planks',
    'deepslate_tile_wall'
     ]
    
    try:
        # Load processing area schematic
        print(f"Loading schematic: {schematic_file}")
        schematic = SchematicReader(schematic_file)
        schematic.load()
        
        # Get schematic info
        info = schematic.get_info()
        print(f"Schematic dimensions: {info['width']} x {info['height']} x {info['length']}")
        print(f"Total volume: {info['width'] * info['height'] * info['length']} blocks")
        
        # Get block data
        print("Analyzing blocks...")
        block_counts, unique_blocks = get_unique_blocks(schematic)
        
        # Get chest contents
        chest_items = get_chest_contents(schematic)
        
        print(f"\n=== DEBUG: ALL BLOCKS IN SCHEMATIC ===")
        print(f"Total unique block types: {len(unique_blocks)}")
        print(f"Total blocks placed: {sum(block_counts.values())}")
        print("\nAll blocks found (with counts for reference):")
        for block_state, count in sorted(block_counts.items()):
            print(f"  {block_state}: {count}")
        
        print(f"\n=== CHEST CONTENTS ===")
        if chest_items:
            print(f"Found {len(chest_items)} unique item types in chests:")
            for item in sorted(chest_items):
                print(f"  📦 {item}")
        else:
            print("No items found in chests")
        
        print(f"\n=== UNIQUE BLOCK TYPES (NO COUNTS) ===")
        print("All unique block types found:")
        for block_state in sorted(unique_blocks):
            print(f"  {block_state}")
        
        # Combine blocks and chest items
        all_items = unique_blocks.union(chest_items)
        print(f"\n=== COMBINED BLOCKS + CHEST ITEMS ===")
        print(f"Total unique items (blocks + chest contents): {len(all_items)}")
        print("All items (blocks and chest contents):")
        for item in sorted(all_items):
            source = []
            if item in unique_blocks:
                source.append("block")
            if item in chest_items:
                source.append("chest")
            print(f"  {item} ({', '.join(source)})")
        
        # Filter out excluded blocks
        print(f"\n=== FILTERING EXCLUDED BLOCKS ===")
        print(f"Excluding: {excluded_blocks}")
        filtered_blocks, excluded_found = filter_excluded_blocks(all_items, excluded_blocks)
        
        if excluded_found:
            print("Excluded blocks found:")
            for block_state in sorted(excluded_found):
                print(f"  ❌ {block_state}")
        else:
            print("No excluded blocks found in schematic")
        
        print(f"\n=== FINAL PROCESSING AREA ITEMS ===")
        print(f"Remaining unique items (blocks + chest contents): {len(filtered_blocks)}")
        
        if filtered_blocks:
            print("\nFinal processing area inventory (unique items only):")
            for item in sorted(filtered_blocks):
                item_type, attributes = parse_block_state(item)
                source = []
                if item in unique_blocks:
                    source.append("block")
                if item in chest_items:
                    source.append("chest")
                    
                if attributes:
                    print(f"  ✅ {item_type} (with attributes: {attributes}) [{', '.join(source)}]")
                else:
                    print(f"  ✅ {item_type} [{', '.join(source)}]")
                    
            print(f"\n📋 SUMMARY FOR DATABASE:")
            print("Items that would be stored in ProcessingArea table:")
            for item in sorted(filtered_blocks):
                item_type, attributes = parse_block_state(item)
                source = []
                if item in unique_blocks:
                    source.append("block")
                if item in chest_items:
                    source.append("chest")
                print(f"  - item_type: '{item_type}', item_attributes: '{attributes or 'NULL'}' # from: {', '.join(source)}")
        else:
            print("⚠️  No items found for processing area after filtering")
            
        print(f"\n🔍 VERIFICATION COMPLETE")
        print("Review the output above. If it looks correct, uncomment database operations in the script.")
        
        # Return filtered_blocks and source info for database operations
        return filtered_blocks, unique_blocks, chest_items
            
    except Exception as e:
        print(f"❌ Error analyzing processing area: {e}")
        import traceback
        traceback.print_exc()
        return set(), set(), set()  # Return empty sets on error


def insert_processing_area_items(db, filtered_blocks, unique_blocks, chest_items):
    """Insert processing area items into the ProcessingArea table"""
    with db.get_connection() as conn:
        cursor = conn.cursor()
        
        for item in filtered_blocks:
            item_type, attributes = parse_block_state(item)
            
            # If item is from chest and has no attributes, set attributes to "from chest"
            if item in chest_items and not attributes:
                attributes = "from chest"
            
            cursor.execute("""
                INSERT OR REPLACE INTO ProcessingArea 
                (item_type, item_attributes, last_updated)
                VALUES (?, ?, ?)
            """, (item_type, attributes, datetime.now()))
            
            print(f"  ✅ Added: {item_type} {attributes or ''}")

if __name__ == "__main__":
    # Process the processing area schematic
    schem_path = "/mc-data/plugins/WorldEdit/schematics/processing_area.schem"
    filtered_blocks, unique_blocks, chest_items = analyze_processing_area(schem_path)
    
    print(f"\n🎯 Analysis complete! Review output before enabling database operations.")
    
    # DATABASE OPERATIONS COMMENTED OUT FOR VERIFICATION
    # Initialize database
    db = Database()
    db.init_tables()
    
    # Clear existing processing area data
    with db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM ProcessingArea")
        print("🧹 Cleared existing processing area data")
    
    insert_processing_area_items(db,
    filtered_blocks=filtered_blocks,
    unique_blocks=unique_blocks,
    chest_items=chest_items
    )