#!/usr/bin/env python3
# file: update_build_recipes_from_datapack.py
# desc: Updates BuildRecipes table based on structure check datapack functions

from mc_database import Database

def clear_existing_recipes(db):
    """Clear all existing build recipes"""
    with db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM BuildRecipes")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='BuildRecipes'")
        print("🧹 Cleared existing build recipes")

def insert_recipe_item(cursor, structure_id, item_type, attributes, quantity):
    """Insert a single recipe item"""
    cursor.execute("""
        INSERT INTO BuildRecipes (structure_id, item_type, item_attributes, quantity)
        VALUES (?, ?, ?, ?)
    """, (structure_id, item_type, attributes, quantity))

def add_structure_1_recipe(db):
    """Structure 1 recipe from check_structure_1.mcfunction"""
    print("Adding Structure 1 recipe...")
    with db.get_connection() as conn:
        cursor = conn.cursor()
        
        # From the check function:
        insert_recipe_item(cursor, 1, "minecraft:light_gray_concrete", None, 25)
        insert_recipe_item(cursor, 1, "minecraft:oak_stairs", "[facing=south,half=bottom,shape=straight,waterlogged=false]", 5)
        insert_recipe_item(cursor, 1, "minecraft:oak_stairs", "[facing=east,half=bottom,shape=straight,waterlogged=false]", 5)
        insert_recipe_item(cursor, 1, "minecraft:oak_stairs", "[facing=west,half=bottom,shape=straight,waterlogged=false]", 5)
        insert_recipe_item(cursor, 1, "minecraft:oak_stairs", "[facing=north,half=bottom,shape=straight,waterlogged=false]", 5)
        insert_recipe_item(cursor, 1, "minecraft:iron_bars", "[east=false,north=false,south=false,waterlogged=false,west=false]", 5)

def add_structure_2_recipe(db):
    """Structure 2 recipe from check_structure_2.mcfunction"""
    print("Adding Structure 2 recipe...")
    with db.get_connection() as conn:
        cursor = conn.cursor()
        
        # Total oak_fence: 77 (all variants combined)
        insert_recipe_item(cursor, 2, "minecraft:oak_fence", None, 77)
        insert_recipe_item(cursor, 2, "minecraft:stripped_oak_wood", "[axis=y]", 1)
        insert_recipe_item(cursor, 2, "minecraft:stripped_oak_wood", "[axis=x]", 6)
        insert_recipe_item(cursor, 2, "minecraft:stripped_oak_wood", "[axis=z]", 4)

def add_structure_3_recipe(db):
    """Structure 3 recipe from check_structure_3.mcfunction"""
    print("Adding Structure 3 recipe...")
    with db.get_connection() as conn:
        cursor = conn.cursor()
        
        insert_recipe_item(cursor, 3, "minecraft:bricks", None, 13)
        insert_recipe_item(cursor, 3, "minecraft:heavy_weighted_pressure_plate", "[power=0]", 2)
        insert_recipe_item(cursor, 3, "minecraft:iron_door", "[facing=north,half=lower,hinge=left,open=false,powered=false]", 1)
        insert_recipe_item(cursor, 3, "minecraft:iron_door", "[facing=north,half=upper,hinge=left,open=false,powered=false]", 1)
        insert_recipe_item(cursor, 3, "minecraft:pale_oak_planks", None, 15)
        insert_recipe_item(cursor, 3, "minecraft:glass", None, 14)
        insert_recipe_item(cursor, 3, "minecraft:pale_oak_slab", "[type=double,waterlogged=false]", 4)
        insert_recipe_item(cursor, 3, "minecraft:pale_oak_slab", "[type=bottom,waterlogged=false]", 24)

def add_structure_4_recipe(db):
    """Structure 4 recipe from check_structure_4.mcfunction"""
    print("Adding Structure 4 recipe...")
    with db.get_connection() as conn:
        cursor = conn.cursor()
        
        insert_recipe_item(cursor, 4, "minecraft:iron_block", None, 12)
        # Powered trapdoors (exact orientations for redstone circuit)
        insert_recipe_item(cursor, 4, "minecraft:iron_trapdoor", "[facing=south,half=bottom,open=true,powered=true,waterlogged=false]", 1)
        insert_recipe_item(cursor, 4, "minecraft:iron_trapdoor", "[facing=east,half=bottom,open=true,powered=true,waterlogged=false]", 4)
        insert_recipe_item(cursor, 4, "minecraft:iron_trapdoor", "[facing=west,half=bottom,open=true,powered=true,waterlogged=false]", 4)
        insert_recipe_item(cursor, 4, "minecraft:redstone_torch", "[lit=true]", 4)
        insert_recipe_item(cursor, 4, "minecraft:iron_door", "[facing=north,half=lower,hinge=right,open=true,powered=true]", 1)
        insert_recipe_item(cursor, 4, "minecraft:iron_door", "[facing=north,half=upper,hinge=right,open=true,powered=true]", 1)
        insert_recipe_item(cursor, 4, "minecraft:orange_concrete", None, 19)
        # Unpowered trapdoors (flexible orientations - total 18)
        insert_recipe_item(cursor, 4, "minecraft:iron_trapdoor", "[facing=east,half=bottom,open=false,powered=false,waterlogged=false]", 6)
        insert_recipe_item(cursor, 4, "minecraft:iron_trapdoor", "[facing=north,half=bottom,open=false,powered=false,waterlogged=false]", 12)

def add_structure_5_recipe(db):
    """Structure 5 recipe from check_structure_5.mcfunction"""
    print("Adding Structure 5 recipe...")
    with db.get_connection() as conn:
        cursor = conn.cursor()
        
        insert_recipe_item(cursor, 5, "minecraft:light_gray_concrete", None, 16)
        insert_recipe_item(cursor, 5, "minecraft:iron_block", None, 49)
        insert_recipe_item(cursor, 5, "minecraft:iron_door", "[facing=west,half=lower,hinge=left,open=false,powered=false]", 1)
        insert_recipe_item(cursor, 5, "minecraft:iron_door", "[facing=west,half=upper,hinge=left,open=false,powered=false]", 1)
        insert_recipe_item(cursor, 5, "minecraft:pale_oak_trapdoor", "[facing=north,half=bottom,open=true,powered=false,waterlogged=false]", 18)
        insert_recipe_item(cursor, 5, "minecraft:stone_button", "[face=wall,facing=east,powered=false]", 1)
        insert_recipe_item(cursor, 5, "minecraft:stone_button", "[face=wall,facing=west,powered=false]", 1)
        insert_recipe_item(cursor, 5, "minecraft:glass", None, 1)
        insert_recipe_item(cursor, 5, "minecraft:deepslate_tile_stairs", "[facing=east,half=bottom,shape=straight,waterlogged=false]", 18)
        insert_recipe_item(cursor, 5, "minecraft:deepslate_tile_stairs", "[facing=west,half=bottom,shape=straight,waterlogged=false]", 18)
        insert_recipe_item(cursor, 5, "minecraft:end_rod", "[facing=east]", 2)
        insert_recipe_item(cursor, 5, "minecraft:end_rod", "[facing=west]", 2)
        insert_recipe_item(cursor, 5, "minecraft:pale_oak_trapdoor", "[facing=south,half=bottom,open=true,powered=false,waterlogged=false]", 2)

def add_structure_6_recipe(db):
    """Structure 6 recipe from check_structure_6.mcfunction"""
    print("Adding Structure 6 recipe...")
    with db.get_connection() as conn:
        cursor = conn.cursor()
        
        insert_recipe_item(cursor, 6, "minecraft:light_gray_concrete", None, 15)

        # Brick walls (total 41 - simplified to avoid complex connection states)
        insert_recipe_item(cursor, 6, "minecraft:brick_wall", None, 41)
        insert_recipe_item(cursor, 6, "minecraft:waxed_oxidized_cut_copper_stairs", "[facing=north,half=bottom,shape=straight,waterlogged=false]", 3)
        insert_recipe_item(cursor, 6, "minecraft:polished_diorite_stairs", "[facing=south,half=bottom,shape=straight,waterlogged=false]", 7)
        insert_recipe_item(cursor, 6, "minecraft:dark_oak_hanging_sign", "[attached=false,rotation=0,waterlogged=false]", 1)
        # Iron trapdoors (flexible orientations - total 21)
        insert_recipe_item(cursor, 6, "minecraft:iron_trapdoor", "[facing=north,half=bottom,open=false,powered=false,waterlogged=false]", 7)
        insert_recipe_item(cursor, 6, "minecraft:iron_trapdoor", "[facing=south,half=bottom,open=false,powered=false,waterlogged=false]", 8)
        insert_recipe_item(cursor, 6, "minecraft:iron_trapdoor", "[facing=east,half=bottom,open=false,powered=false,waterlogged=false]", 6)

def add_structure_7_recipe(db):
    """Structure 7 recipe from check_structure_7.mcfunction"""
    print("Adding Structure 7 recipe...")
    with db.get_connection() as conn:
        cursor = conn.cursor()
        
        insert_recipe_item(cursor, 7, "minecraft:peony", "[half=lower]", 4)
        insert_recipe_item(cursor, 7, "minecraft:peony", "[half=upper]", 4)
        insert_recipe_item(cursor, 7, "minecraft:oak_planks", None, 8)
        # Oak fence (total 44 - simplified)
        insert_recipe_item(cursor, 7, "minecraft:oak_fence", None, 44)
        insert_recipe_item(cursor, 7, "minecraft:stripped_oak_wood", "[axis=y]", 20)
        insert_recipe_item(cursor, 7, "minecraft:oak_trapdoor", "[facing=east,half=bottom,open=true,powered=false,waterlogged=false]", 4)
        insert_recipe_item(cursor, 7, "minecraft:oak_trapdoor", "[facing=west,half=bottom,open=true,powered=false,waterlogged=false]", 4)
        insert_recipe_item(cursor, 7, "minecraft:oak_trapdoor", "[facing=south,half=bottom,open=true,powered=false,waterlogged=false]", 4)
        insert_recipe_item(cursor, 7, "minecraft:oak_trapdoor", "[facing=north,half=bottom,open=true,powered=false,waterlogged=false]", 4)
        insert_recipe_item(cursor, 7, "minecraft:oak_trapdoor", "[facing=west,half=top,open=false,powered=false,waterlogged=false]", 1)
        insert_recipe_item(cursor, 7, "minecraft:lantern", "[hanging=true,waterlogged=false]", 12)
        # Fence gates (simplified)
        insert_recipe_item(cursor, 7, "minecraft:oak_fence_gate", "[facing=north,in_wall=false,open=false,powered=false]", 2)
        insert_recipe_item(cursor, 7, "minecraft:oak_fence_gate", "[facing=west,in_wall=false,open=false,powered=false]", 1)
        insert_recipe_item(cursor, 7, "minecraft:oak_fence_gate", "[facing=east,in_wall=false,open=false,powered=false]", 1)
        # Nether brick stairs (simplified totals)
        insert_recipe_item(cursor, 7, "minecraft:nether_brick_stairs", None, 48)

def add_structure_8_recipe(db):
    """Structure 8 recipe from check_structure_8.mcfunction"""
    print("Adding Structure 8 recipe...")
    with db.get_connection() as conn:
        cursor = conn.cursor()
        
        insert_recipe_item(cursor, 8, "minecraft:chiseled_stone_bricks", None, 24)
        insert_recipe_item(cursor, 8, "minecraft:smooth_stone_slab", "[type=bottom,waterlogged=false]", 32)
        insert_recipe_item(cursor, 8, "minecraft:smooth_stone_slab", "[type=top,waterlogged=false]", 13)
        insert_recipe_item(cursor, 8, "minecraft:stone_brick_wall", "[east=none,north=none,south=none,up=true,waterlogged=false,west=none]", 14)
        insert_recipe_item(cursor, 8, "minecraft:end_rod", "[facing=down]", 4)
        insert_recipe_item(cursor, 8, "minecraft:end_rod", "[facing=up]", 1)


def add_structure_9_recipe(db):
    """Structure 9 recipe from check_structure_9.mcfunction"""
    print("Adding Structure 9 recipe...")
    with db.get_connection() as conn:
        cursor = conn.cursor()
        
        insert_recipe_item(cursor, 9, "minecraft:iron_bars", "[east=false,north=false,south=false,waterlogged=false,west=false]", 18)
        insert_recipe_item(cursor, 9, "minecraft:smooth_stone_slab", "[type=bottom,waterlogged=false]", 19)
        # Iron trapdoors (flexible orientations - total 16)
        insert_recipe_item(cursor, 9, "minecraft:iron_trapdoor", "[facing=west,half=bottom,open=false,powered=false,waterlogged=false]", 8)
        insert_recipe_item(cursor, 9, "minecraft:iron_trapdoor", "[facing=east,half=bottom,open=false,powered=false,waterlogged=false]", 2)
        insert_recipe_item(cursor, 9, "minecraft:iron_trapdoor", "[facing=south,half=bottom,open=false,powered=false,waterlogged=false]", 1)
        insert_recipe_item(cursor, 9, "minecraft:iron_trapdoor", "[facing=north,half=bottom,open=false,powered=false,waterlogged=false]", 5)

def add_structure_10_recipe(db):
    """Structure 10 recipe from check_structure_10.mcfunction"""
    print("Adding Structure 10 recipe...")
    with db.get_connection() as conn:
        cursor = conn.cursor()
        
        insert_recipe_item(cursor, 10, "minecraft:iron_block", None, 7)
        insert_recipe_item(cursor, 10, "minecraft:iron_bars", None, 6)
        # Iron trapdoors (flexible orientations - total 6)
        insert_recipe_item(cursor, 10, "minecraft:iron_trapdoor", "[facing=east,half=bottom,open=false,powered=false,waterlogged=false]", 4)
        insert_recipe_item(cursor, 10, "minecraft:iron_trapdoor", "[facing=north,half=bottom,open=false,powered=false,waterlogged=false]", 1)
        insert_recipe_item(cursor, 10, "minecraft:iron_trapdoor", "[facing=south,half=bottom,open=false,powered=false,waterlogged=false]", 1)
        # Red banners
        insert_recipe_item(cursor, 10, "minecraft:red_wall_banner", "[facing=north]", 2)
        insert_recipe_item(cursor, 10, "minecraft:red_wall_banner", "[facing=west]", 2)
        insert_recipe_item(cursor, 10, "minecraft:red_wall_banner", "[facing=east]", 2)
        insert_recipe_item(cursor, 10, "minecraft:red_wall_banner", "[facing=south]", 2)

def main():
    print("🏗️  Starting Build Recipe Database Update from Datapack Functions")
    
    # Initialize database
    db = Database()
    db.init_tables()
    
    # Clear existing recipes
    clear_existing_recipes(db)
    
    # Add all structure recipes
    structure_functions = [
        add_structure_1_recipe,
        add_structure_2_recipe,
        add_structure_3_recipe,
        add_structure_4_recipe,
        add_structure_5_recipe,
        add_structure_6_recipe,
        add_structure_7_recipe,
        add_structure_8_recipe,
        add_structure_9_recipe,
        add_structure_10_recipe
    ]
    
    for i, func in enumerate(structure_functions, 1):
        try:
            func(db)
            print(f"✅ Successfully added Structure {i} recipe")
        except Exception as e:
            print(f"❌ Error adding Structure {i} recipe: {e}")
            import traceback
            traceback.print_exc()
    
    # Verify results
    with db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT structure_id, COUNT(*) as item_count FROM BuildRecipes GROUP BY structure_id ORDER BY structure_id")
        results = cursor.fetchall()
        
        print("\n📊 Recipe Summary:")
        total_items = 0
        for row in results:
            print(f"  Structure {row['structure_id']}: {row['item_count']} different items")
            total_items += row['item_count']
        
        print(f"  Total recipe items: {total_items}")
    
    print("\n🎉 Build recipe database update complete!")

if __name__ == "__main__":
    main()