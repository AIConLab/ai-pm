# file: check_structure_7.mcfunction

# Silent structure checking - runs every tick from timer.mcfunction
# Command block is 1 block under platform, so build area is ~-3 ~1 ~-3 to ~3 ~7 ~3

# Initialize check
scoreboard players set #valid bm_status 1

# Count total peony blocks (need exactly 8 total - 4 flowers = 4 lower + 4 upper halves)
# Count all peony blocks together to avoid breaking the tall plant connection
execute store result score #peony bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:peony
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:peony replace minecraft:barrier
execute unless score #peony bm_timer matches 8 run scoreboard players set #valid bm_status 0

# Count oak_planks (need exactly 8)
execute store result score #oak_planks bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:oak_planks
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:oak_planks replace minecraft:barrier
execute unless score #oak_planks bm_timer matches 8 run scoreboard players set #valid bm_status 0

# Count total oak_fence blocks (need exactly 44 total - sum of all fence variants)
# Fence blocks automatically connect, so we count total rather than specific connection states
execute store result score #oak_fence bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:oak_fence
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:oak_fence replace minecraft:barrier
execute unless score #oak_fence bm_timer matches 44 run scoreboard players set #valid bm_status 0

# Count oak_fence_gate [facing=north,in_wall=false,open=false,powered=false] (need exactly 2)
execute store result score #gate_north bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:oak_fence_gate[facing=north,in_wall=false,open=false,powered=false]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:oak_fence_gate[facing=north,in_wall=false,open=false,powered=false] replace minecraft:barrier
execute unless score #gate_north bm_timer matches 2 run scoreboard players set #valid bm_status 0

# Count stripped_oak_wood [axis=y] (need exactly 20)
execute store result score #stripped_wood bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:stripped_oak_wood[axis=y]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:stripped_oak_wood[axis=y] replace minecraft:barrier
execute unless score #stripped_wood bm_timer matches 20 run scoreboard players set #valid bm_status 0

# Count oak_trapdoor [facing=east,half=bottom,open=true,powered=false,waterlogged=false] (need exactly 4)
execute store result score #trapdoor_e bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:oak_trapdoor[facing=east,half=bottom,open=true,powered=false,waterlogged=false]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:oak_trapdoor[facing=east,half=bottom,open=true,powered=false,waterlogged=false] replace minecraft:barrier
execute unless score #trapdoor_e bm_timer matches 4 run scoreboard players set #valid bm_status 0

# Count oak_trapdoor [facing=west,half=bottom,open=true,powered=false,waterlogged=false] (need exactly 4)
execute store result score #trapdoor_w bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:oak_trapdoor[facing=west,half=bottom,open=true,powered=false,waterlogged=false]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:oak_trapdoor[facing=west,half=bottom,open=true,powered=false,waterlogged=false] replace minecraft:barrier
execute unless score #trapdoor_w bm_timer matches 4 run scoreboard players set #valid bm_status 0

# Count oak_trapdoor [facing=south,half=bottom,open=true,powered=false,waterlogged=false] (need exactly 4)
execute store result score #trapdoor_s bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:oak_trapdoor[facing=south,half=bottom,open=true,powered=false,waterlogged=false]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:oak_trapdoor[facing=south,half=bottom,open=true,powered=false,waterlogged=false] replace minecraft:barrier
execute unless score #trapdoor_s bm_timer matches 4 run scoreboard players set #valid bm_status 0

# Count oak_fence_gate [facing=west,in_wall=false,open=false,powered=false] (need exactly 1)
execute store result score #gate_west bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:oak_fence_gate[facing=west,in_wall=false,open=false,powered=false]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:oak_fence_gate[facing=west,in_wall=false,open=false,powered=false] replace minecraft:barrier
execute unless score #gate_west bm_timer matches 1 run scoreboard players set #valid bm_status 0

# Count oak_fence_gate [facing=east,in_wall=false,open=false,powered=false] (need exactly 1)
execute store result score #gate_east bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:oak_fence_gate[facing=east,in_wall=false,open=false,powered=false]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:oak_fence_gate[facing=east,in_wall=false,open=false,powered=false] replace minecraft:barrier
execute unless score #gate_east bm_timer matches 1 run scoreboard players set #valid bm_status 0

# Count oak_trapdoor [facing=north,half=bottom,open=true,powered=false,waterlogged=false] (need exactly 4)
execute store result score #trapdoor_n bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:oak_trapdoor[facing=north,half=bottom,open=true,powered=false,waterlogged=false]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:oak_trapdoor[facing=north,half=bottom,open=true,powered=false,waterlogged=false] replace minecraft:barrier
execute unless score #trapdoor_n bm_timer matches 4 run scoreboard players set #valid bm_status 0

# Count lantern [hanging=true,waterlogged=false] (need exactly 12)
execute store result score #lantern bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:lantern[hanging=true,waterlogged=false]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:lantern[hanging=true,waterlogged=false] replace minecraft:barrier
execute unless score #lantern bm_timer matches 12 run scoreboard players set #valid bm_status 0

# Count total nether_brick_stairs blocks (need exactly 48 total)
execute store result score #nether_stairs bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:nether_brick_stairs
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:nether_brick_stairs replace minecraft:barrier
execute unless score #nether_stairs bm_timer matches 48 run scoreboard players set #valid bm_status 0

# Count oak_trapdoor [facing=west,half=top,open=false,powered=false,waterlogged=false] (need exactly 1)
execute store result score #trapdoor_w_top bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:oak_trapdoor[facing=west,half=top,open=false,powered=false,waterlogged=false]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:oak_trapdoor[facing=west,half=top,open=false,powered=false,waterlogged=false] replace minecraft:barrier
execute unless score #trapdoor_w_top bm_timer matches 1 run scoreboard players set #valid bm_status 0

# Check if structure is complete
execute if score #valid bm_status matches 1 if score #already_complete bm_status matches 0 run function buildmart:structure_7_done