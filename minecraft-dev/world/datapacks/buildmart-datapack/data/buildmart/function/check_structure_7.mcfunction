# file: check_structure_7.mcfunction

# Silent structure checking - runs every tick from timer.mcfunction
# Command block is 1 block under platform, so build area is ~-3 ~1 ~-3 to ~3 ~7 ~3

# --- FINAL VERSION ---

# Initialize check
scoreboard players set #valid bm_status 1

# --- Simple Block Checks (Confirmed) ---
# Peony check using fill command (need 4)
execute store result score #peony_lower bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:peony[half=lower]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:peony[half=lower] replace minecraft:barrier
execute unless score #peony_lower bm_timer matches 4 run scoreboard players set #valid bm_status 0

# Count oak_planks (need 8)
execute store result score #oak_planks bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:oak_planks
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:oak_planks replace minecraft:barrier
execute unless score #oak_planks bm_timer matches 8 run scoreboard players set #valid bm_status 0

# Count total oak_fence blocks (need 44)
execute store result score #oak_fence bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:oak_fence
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:oak_fence replace minecraft:barrier
execute unless score #oak_fence bm_timer matches 44 run scoreboard players set #valid bm_status 0

# Count stripped_oak_wood [axis=y] (need 20)
execute store result score #stripped_wood_y bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:stripped_oak_wood[axis=y]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:stripped_oak_wood[axis=y] replace minecraft:barrier
execute unless score #stripped_wood_y bm_timer matches 20 run scoreboard players set #valid bm_status 0

# --- Specific State Checks ---
# Oak Trapdoor checks (5 types, 17 total)
execute store result score #trapdoor_e_open bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:oak_trapdoor[facing=east,half=bottom,open=true,powered=false,waterlogged=false]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:oak_trapdoor[facing=east,half=bottom,open=true,powered=false,waterlogged=false] replace minecraft:barrier
execute unless score #trapdoor_e_open bm_timer matches 4 run scoreboard players set #valid bm_status 0

execute store result score #trapdoor_w_open bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:oak_trapdoor[facing=west,half=bottom,open=true,powered=false,waterlogged=false]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:oak_trapdoor[facing=west,half=bottom,open=true,powered=false,waterlogged=false] replace minecraft:barrier
execute unless score #trapdoor_w_open bm_timer matches 4 run scoreboard players set #valid bm_status 0

execute store result score #trapdoor_s_open bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:oak_trapdoor[facing=south,half=bottom,open=true,powered=false,waterlogged=false]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:oak_trapdoor[facing=south,half=bottom,open=true,powered=false,waterlogged=false] replace minecraft:barrier
execute unless score #trapdoor_s_open bm_timer matches 4 run scoreboard players set #valid bm_status 0

execute store result score #trapdoor_n_open bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:oak_trapdoor[facing=north,half=bottom,open=true,powered=false,waterlogged=false]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:oak_trapdoor[facing=north,half=bottom,open=true,powered=false,waterlogged=false] replace minecraft:barrier
execute unless score #trapdoor_n_open bm_timer matches 4 run scoreboard players set #valid bm_status 0

execute store result score #trapdoor_w_top bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:oak_trapdoor[facing=west,half=top,open=false,powered=false,waterlogged=false]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:oak_trapdoor[facing=west,half=top,open=false,powered=false,waterlogged=false] replace minecraft:barrier
execute unless score #trapdoor_w_top bm_timer matches 1 run scoreboard players set #valid bm_status 0

# Lantern check (need 12)
execute store result score #lantern_hanging bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:lantern[hanging=true,waterlogged=false]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:lantern[hanging=true,waterlogged=false] replace minecraft:barrier
execute unless score #lantern_hanging bm_timer matches 12 run scoreboard players set #valid bm_status 0

# Oak Fence Gate checks (3 types, 4 total)
execute store result score #gate_n bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:oak_fence_gate[facing=north,in_wall=false,open=false,powered=false]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:oak_fence_gate[facing=north,in_wall=false,open=false,powered=false] replace minecraft:barrier
execute unless score #gate_n bm_timer matches 2 run scoreboard players set #valid bm_status 0

execute store result score #gate_w bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:oak_fence_gate[facing=west,in_wall=false,open=false,powered=false]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:oak_fence_gate[facing=west,in_wall=false,open=false,powered=false] replace minecraft:barrier
execute unless score #gate_w bm_timer matches 1 run scoreboard players set #valid bm_status 0

execute store result score #gate_e bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:oak_fence_gate[facing=east,in_wall=false,open=false,powered=false]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:oak_fence_gate[facing=east,in_wall=false,open=false,powered=false] replace minecraft:barrier
execute unless score #gate_e bm_timer matches 1 run scoreboard players set #valid bm_status 0

# Nether Brick Stairs checks (4 types, 48 total - grouped by facing, ignoring shape)
execute store result score #stairs_e bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:nether_brick_stairs[facing=east,half=bottom,waterlogged=false]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:nether_brick_stairs[facing=east,half=bottom,waterlogged=false] replace minecraft:barrier
execute unless score #stairs_e bm_timer matches 13 run scoreboard players set #valid bm_status 0

execute store result score #stairs_s bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:nether_brick_stairs[facing=south,half=bottom,waterlogged=false]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:nether_brick_stairs[facing=south,half=bottom,waterlogged=false] replace minecraft:barrier
execute unless score #stairs_s bm_timer matches 10 run scoreboard players set #valid bm_status 0

execute store result score #stairs_w bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:nether_brick_stairs[facing=west,half=bottom,waterlogged=false]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:nether_brick_stairs[facing=west,half=bottom,waterlogged=false] replace minecraft:barrier
execute unless score #stairs_w bm_timer matches 14 run scoreboard players set #valid bm_status 0

execute store result score #stairs_n bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:nether_brick_stairs[facing=north,half=bottom,waterlogged=false]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:nether_brick_stairs[facing=north,half=bottom,waterlogged=false] replace minecraft:barrier
execute unless score #stairs_n bm_timer matches 11 run scoreboard players set #valid bm_status 0

# --- Final Check ---
execute if score #valid bm_status matches 1 if score #already_complete bm_status matches 0 run function buildmart:structure_7_done

