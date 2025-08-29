# file: check_structure_7.mcfunction

# Silent structure checking - runs every tick from timer.mcfunction
# Command block is 1 block under platform, so build area is ~-3 ~1 ~-3 to ~3 ~7 ~3

# Initialize check
scoreboard players set #valid bm_status 1

# Check peony at the four corners (need 4)
scoreboard players set #peony_count bm_timer 0
execute if block ~-3 ~1 ~-3 minecraft:peony[half=lower] run scoreboard players add #peony_count bm_timer 1
execute if block ~3 ~1 ~-3 minecraft:peony[half=lower] run scoreboard players add #peony_count bm_timer 1
execute if block ~3 ~1 ~3 minecraft:peony[half=lower] run scoreboard players add #peony_count bm_timer 1
execute if block ~-3 ~1 ~3 minecraft:peony[half=lower] run scoreboard players add #peony_count bm_timer 1
execute unless score #peony_count bm_timer matches 4 run scoreboard players set #valid bm_status 0

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

# Count oak_trapdoor [facing=east,half=bottom,open=true] (need 4)
execute store result score #trapdoor_e_open bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:oak_trapdoor[facing=east,half=bottom,open=true,powered=false,waterlogged=false]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:oak_trapdoor[facing=east,half=bottom,open=true,powered=false,waterlogged=false] replace minecraft:barrier
execute unless score #trapdoor_e_open bm_timer matches 4 run scoreboard players set #valid bm_status 0

# Count oak_trapdoor [facing=west,half=bottom,open=true] (need 4)
execute store result score #trapdoor_w_open bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:oak_trapdoor[facing=west,half=bottom,open=true,powered=false,waterlogged=false]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:oak_trapdoor[facing=west,half=bottom,open=true,powered=false,waterlogged=false] replace minecraft:barrier
execute unless score #trapdoor_w_open bm_timer matches 4 run scoreboard players set #valid bm_status 0

# Count oak_trapdoor [facing=south,half=bottom,open=true] (need 4)
execute store result score #trapdoor_s_open bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:oak_trapdoor[facing=south,half=bottom,open=true,powered=false,waterlogged=false]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:oak_trapdoor[facing=south,half=bottom,open=true,powered=false,waterlogged=false] replace minecraft:barrier
execute unless score #trapdoor_s_open bm_timer matches 4 run scoreboard players set #valid bm_status 0

# Count oak_trapdoor [facing=north,half=bottom,open=true] (need 4)
execute store result score #trapdoor_n_open bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:oak_trapdoor[facing=north,half=bottom,open=true,powered=false,waterlogged=false]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:oak_trapdoor[facing=north,half=bottom,open=true,powered=false,waterlogged=false] replace minecraft:barrier
execute unless score #trapdoor_n_open bm_timer matches 4 run scoreboard players set #valid bm_status 0

# Count oak_trapdoor [facing=west,half=top,open=false] (need 1)
execute store result score #trapdoor_w_top bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:oak_trapdoor[facing=west,half=top,open=false,powered=false,waterlogged=false]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:oak_trapdoor[facing=west,half=top,open=false,powered=false,waterlogged=false] replace minecraft:barrier
execute unless score #trapdoor_w_top bm_timer matches 1 run scoreboard players set #valid bm_status 0

# Count lantern [hanging=true] (need 12)
execute store result score #lantern_hanging bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:lantern[hanging=true,waterlogged=false]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:lantern[hanging=true,waterlogged=false] replace minecraft:barrier
execute unless score #lantern_hanging bm_timer matches 12 run scoreboard players set #valid bm_status 0

# Count oak_fence_gate [facing=north,in_wall=false,open=false] (need 2)
execute store result score #gate_n bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:oak_fence_gate[facing=north,in_wall=false,open=false,powered=false]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:oak_fence_gate[facing=north,in_wall=false,open=false,powered=false] replace minecraft:barrier
execute unless score #gate_n bm_timer matches 2 run scoreboard players set #valid bm_status 0

# Count oak_fence_gate [facing=west,in_wall=false,open=false] (need 1)
execute store result score #gate_w bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:oak_fence_gate[facing=west,in_wall=false,open=false,powered=false]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:oak_fence_gate[facing=west,in_wall=false,open=false,powered=false] replace minecraft:barrier
execute unless score #gate_w bm_timer matches 1 run scoreboard players set #valid bm_status 0

# Count oak_fence_gate [facing=east,in_wall=false,open=false] (need 1)
execute store result score #gate_e bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:oak_fence_gate[facing=east,in_wall=false,open=false,powered=false]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:oak_fence_gate[facing=east,in_wall=false,open=false,powered=false] replace minecraft:barrier
execute unless score #gate_e bm_timer matches 1 run scoreboard players set #valid bm_status 0

# --- Specific Nether Brick Stairs Checks ---
execute store result score #stairs_e_or bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:nether_brick_stairs[facing=east,half=bottom,shape=outer_right,waterlogged=false]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:nether_brick_stairs[facing=east,half=bottom,shape=outer_right,waterlogged=false] replace minecraft:barrier
execute unless score #stairs_e_or bm_timer matches 2 run scoreboard players set #valid bm_status 0

execute store result score #stairs_s_s bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:nether_brick_stairs[facing=south,half=bottom,shape=straight,waterlogged=false]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:nether_brick_stairs[facing=south,half=bottom,shape=straight,waterlogged=false] replace minecraft:barrier
execute unless score #stairs_s_s bm_timer matches 9 run scoreboard players set #valid bm_status 0

execute store result score #stairs_w_ol bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:nether_brick_stairs[facing=west,half=bottom,shape=outer_left,waterlogged=false]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:nether_brick_stairs[facing=west,half=bottom,shape=outer_left,waterlogged=false] replace minecraft:barrier
execute unless score #stairs_w_ol bm_timer matches 3 run scoreboard players set #valid bm_status 0

execute store result score #stairs_e_s bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:nether_brick_stairs[facing=east,half=bottom,shape=straight,waterlogged=false]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:nether_brick_stairs[facing=east,half=bottom,shape=straight,waterlogged=false] replace minecraft:barrier
execute unless score #stairs_e_s bm_timer matches 9 run scoreboard players set #valid bm_status 0

execute store result score #stairs_w_s bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:nether_brick_stairs[facing=west,half=bottom,shape=straight,waterlogged=false]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:nether_brick_stairs[facing=west,half=bottom,shape=straight,waterlogged=false] replace minecraft:barrier
execute unless score #stairs_w_s bm_timer matches 9 run scoreboard players set #valid bm_status 0

execute store result score #stairs_e_ol bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:nether_brick_stairs[facing=east,half=bottom,shape=outer_left,waterlogged=false]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:nether_brick_stairs[facing=east,half=bottom,shape=outer_left,waterlogged=false] replace minecraft:barrier
execute unless score #stairs_e_ol bm_timer matches 2 run scoreboard players set #valid bm_status 0

execute store result score #stairs_n_s bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:nether_brick_stairs[facing=north,half=bottom,shape=straight,waterlogged=false]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:nether_brick_stairs[facing=north,half=bottom,shape=straight,waterlogged=false] replace minecraft:barrier
execute unless score #stairs_n_s bm_timer matches 9 run scoreboard players set #valid bm_status 0

execute store result score #stairs_w_or bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:nether_brick_stairs[facing=west,half=bottom,shape=outer_right,waterlogged=false]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:nether_brick_stairs[facing=west,half=bottom,shape=outer_right,waterlogged=false] replace minecraft:barrier
execute unless score #stairs_w_or bm_timer matches 2 run scoreboard players set #valid bm_status 0

execute store result score #stairs_s_ol bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:nether_brick_stairs[facing=south,half=bottom,shape=outer_left,waterlogged=false]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:nether_brick_stairs[facing=south,half=bottom,shape=outer_left,waterlogged=false] replace minecraft:barrier
execute unless score #stairs_s_ol bm_timer matches 1 run scoreboard players set #valid bm_status 0

execute store result score #stairs_n_or bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:nether_brick_stairs[facing=north,half=bottom,shape=outer_right,waterlogged=false]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:nether_brick_stairs[facing=north,half=bottom,shape=outer_right,waterlogged=false] replace minecraft:barrier
execute unless score #stairs_n_or bm_timer matches 1 run scoreboard players set #valid bm_status 0

execute store result score #stairs_n_ol bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:nether_brick_stairs[facing=north,half=bottom,shape=outer_left,waterlogged=false]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:nether_brick_stairs[facing=north,half=bottom,shape=outer_left,waterlogged=false] replace minecraft:barrier
execute unless score #stairs_n_ol bm_timer matches 1 run scoreboard players set #valid bm_status 0

# --- Final Check ---
execute if score #valid bm_status matches 1 if score #already_complete bm_status matches 0 run function buildmart:structure_7_done

