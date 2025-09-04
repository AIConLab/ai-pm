# file: check_structure_7_final.mcfunction
# Silent structure checking - runs every tick from timer.mcfunction
# This function is generated based on the exact build recipe.

# Initialize check
scoreboard players set #valid bm_status 1

# --- Simple Block Counts ---
# Peony (lower)
execute store result score #count bm_timer run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:barrier replace minecraft:peony[half=lower]
execute run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:peony[half=lower] replace minecraft:barrier
execute unless score #count bm_timer matches 4 run scoreboard players set #valid bm_status 0

# Peony (upper) - was missing from original check
execute store result score #count bm_timer run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:barrier replace minecraft:peony[half=upper]
execute run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:peony[half=upper] replace minecraft:barrier
execute unless score #count bm_timer matches 4 run scoreboard players set #valid bm_status 0

# Oak Planks
execute store result score #count bm_timer run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:barrier replace minecraft:oak_planks
execute run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:oak_planks replace minecraft:barrier
execute unless score #count bm_timer matches 8 run scoreboard players set #valid bm_status 0

# Stripped Oak Wood (axis=y)
execute store result score #count bm_timer run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:barrier replace minecraft:stripped_oak_wood[axis=y]
execute run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:stripped_oak_wood[axis=y] replace minecraft:barrier
execute unless score #count bm_timer matches 20 run scoreboard players set #valid bm_status 0

# Lanterns
execute store result score #count bm_timer run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:barrier replace minecraft:lantern[hanging=true,waterlogged=false]
execute run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:lantern[hanging=true,waterlogged=false] replace minecraft:barrier
execute unless score #count bm_timer matches 12 run scoreboard players set #valid bm_status 0

# --- Complex Block Counts (Flexible) ---
# Oak Fence (Total) - Sum of all variants in recipe is 44
execute store result score #count bm_timer run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:barrier replace minecraft:oak_fence
execute run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:oak_fence replace minecraft:barrier
execute unless score #count bm_timer matches 44 run scoreboard players set #valid bm_status 0

# --- Exact State Checks (Non-Destructive) ---
# Oak Fence Gates
execute store result score #count bm_timer run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:barrier replace minecraft:oak_fence_gate[facing=north,in_wall=false,open=false,powered=false]
execute run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:oak_fence_gate[facing=north,in_wall=false,open=false,powered=false] replace minecraft:barrier
execute unless score #count bm_timer matches 2 run scoreboard players set #valid bm_status 0

execute store result score #count bm_timer run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:barrier replace minecraft:oak_fence_gate[facing=west,in_wall=false,open=false,powered=false]
execute run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:oak_fence_gate[facing=west,in_wall=false,open=false,powered=false] replace minecraft:barrier
execute unless score #count bm_timer matches 1 run scoreboard players set #valid bm_status 0

execute store result score #count bm_timer run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:barrier replace minecraft:oak_fence_gate[facing=east,in_wall=false,open=false,powered=false]
execute run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:oak_fence_gate[facing=east,in_wall=false,open=false,powered=false] replace minecraft:barrier
execute unless score #count bm_timer matches 1 run scoreboard players set #valid bm_status 0

# Oak Trapdoors
execute store result score #count bm_timer run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:barrier replace minecraft:oak_trapdoor[facing=east,half=bottom,open=true,powered=false,waterlogged=false]
execute run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:oak_trapdoor[facing=east,half=bottom,open=true,powered=false,waterlogged=false] replace minecraft:barrier
execute unless score #count bm_timer matches 4 run scoreboard players set #valid bm_status 0

execute store result score #count bm_timer run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:barrier replace minecraft:oak_trapdoor[facing=west,half=bottom,open=true,powered=false,waterlogged=false]
execute run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:oak_trapdoor[facing=west,half=bottom,open=true,powered=false,waterlogged=false] replace minecraft:barrier
execute unless score #count bm_timer matches 4 run scoreboard players set #valid bm_status 0

execute store result score #count bm_timer run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:barrier replace minecraft:oak_trapdoor[facing=south,half=bottom,open=true,powered=false,waterlogged=false]
execute run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:oak_trapdoor[facing=south,half=bottom,open=true,powered=false,waterlogged=false] replace minecraft:barrier
execute unless score #count bm_timer matches 4 run scoreboard players set #valid bm_status 0

execute store result score #count bm_timer run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:barrier replace minecraft:oak_trapdoor[facing=north,half=bottom,open=true,powered=false,waterlogged=false]
execute run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:oak_trapdoor[facing=north,half=bottom,open=true,powered=false,waterlogged=false] replace minecraft:barrier
execute unless score #count bm_timer matches 4 run scoreboard players set #valid bm_status 0

execute store result score #count bm_timer run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:barrier replace minecraft:oak_trapdoor[facing=west,half=top,open=false,powered=false,waterlogged=false]
execute run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:oak_trapdoor[facing=west,half=top,open=false,powered=false,waterlogged=false] replace minecraft:barrier
execute unless score #count bm_timer matches 1 run scoreboard players set #valid bm_status 0

# --- Nether Brick Stairs (Exact Recipe Checks) ---
execute store result score #count bm_timer run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:barrier replace minecraft:nether_brick_stairs[facing=east,half=bottom,shape=outer_right,waterlogged=false]
execute run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:nether_brick_stairs[facing=east,half=bottom,shape=outer_right,waterlogged=false] replace minecraft:barrier
execute unless score #count bm_timer matches 2 run scoreboard players set #valid bm_status 0

execute store result score #count bm_timer run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:barrier replace minecraft:nether_brick_stairs[facing=south,half=bottom,shape=straight,waterlogged=false]
execute run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:nether_brick_stairs[facing=south,half=bottom,shape=straight,waterlogged=false] replace minecraft:barrier
execute unless score #count bm_timer matches 9 run scoreboard players set #valid bm_status 0

execute store result score #count bm_timer run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:barrier replace minecraft:nether_brick_stairs[facing=west,half=bottom,shape=outer_left,waterlogged=false]
execute run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:nether_brick_stairs[facing=west,half=bottom,shape=outer_left,waterlogged=false] replace minecraft:barrier
execute unless score #count bm_timer matches 3 run scoreboard players set #valid bm_status 0

execute store result score #count bm_timer run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:barrier replace minecraft:nether_brick_stairs[facing=east,half=bottom,shape=straight,waterlogged=false]
execute run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:nether_brick_stairs[facing=east,half=bottom,shape=straight,waterlogged=false] replace minecraft:barrier
execute unless score #count bm_timer matches 9 run scoreboard players set #valid bm_status 0

execute store result score #count bm_timer run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:barrier replace minecraft:nether_brick_stairs[facing=west,half=bottom,shape=straight,waterlogged=false]
execute run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:nether_brick_stairs[facing=west,half=bottom,shape=straight,waterlogged=false] replace minecraft:barrier
execute unless score #count bm_timer matches 9 run scoreboard players set #valid bm_status 0

execute store result score #count bm_timer run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:barrier replace minecraft:nether_brick_stairs[facing=east,half=bottom,shape=outer_left,waterlogged=false]
execute run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:nether_brick_stairs[facing=east,half=bottom,shape=outer_left,waterlogged=false] replace minecraft:barrier
execute unless score #count bm_timer matches 2 run scoreboard players set #valid bm_status 0

execute store result score #count bm_timer run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:barrier replace minecraft:nether_brick_stairs[facing=north,half=bottom,shape=straight,waterlogged=false]
execute run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:nether_brick_stairs[facing=north,half=bottom,shape=straight,waterlogged=false] replace minecraft:barrier
execute unless score #count bm_timer matches 9 run scoreboard players set #valid bm_status 0

execute store result score #count bm_timer run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:barrier replace minecraft:nether_brick_stairs[facing=west,half=bottom,shape=outer_right,waterlogged=false]
execute run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:nether_brick_stairs[facing=west,half=bottom,shape=outer_right,waterlogged=false] replace minecraft:barrier
execute unless score #count bm_timer matches 2 run scoreboard players set #valid bm_status 0

execute store result score #count bm_timer run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:barrier replace minecraft:nether_brick_stairs[facing=south,half=bottom,shape=outer_left,waterlogged=false]
execute run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:nether_brick_stairs[facing=south,half=bottom,shape=outer_left,waterlogged=false] replace minecraft:barrier
execute unless score #count bm_timer matches 1 run scoreboard players set #valid bm_status 0

execute store result score #count bm_timer run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:barrier replace minecraft:nether_brick_stairs[facing=north,half=bottom,shape=outer_right,waterlogged=false]
execute run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:nether_brick_stairs[facing=north,half=bottom,shape=outer_right,waterlogged=false] replace minecraft:barrier
execute unless score #count bm_timer matches 1 run scoreboard players set #valid bm_status 0

execute store result score #count bm_timer run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:barrier replace minecraft:nether_brick_stairs[facing=north,half=bottom,shape=outer_left,waterlogged=false]
execute run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:nether_brick_stairs[facing=north,half=bottom,shape=outer_left,waterlogged=false] replace minecraft:barrier
execute unless score #count bm_timer matches 1 run scoreboard players set #valid bm_status 0

# --- Final Check ---
execute if score #valid bm_status matches 1 if score #already_complete bm_status matches 0 run function buildmart:structure_7_done
