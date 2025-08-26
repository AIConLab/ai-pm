# file: check_structure_2.mcfunction

# Silent structure checking - runs every tick from timer.mcfunction
# Command block is 1 block under platform, so build area is ~-3 ~1 ~-3 to ~3 ~7 ~3

# Initialize check
scoreboard players set #valid bm_status 1

# Count oak_fence [east=true,north=false,south=true,waterlogged=false,west=false] (need exactly 5)
execute store result score #fence_1 bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:oak_fence[east=true,north=false,south=true,waterlogged=false,west=false]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:oak_fence[east=true,north=false,south=true,waterlogged=false,west=false] replace minecraft:barrier
execute unless score #fence_1 bm_timer matches 5 run scoreboard players set #valid bm_status 0

# Count oak_fence [east=true,north=false,south=false,waterlogged=false,west=true] (need exactly 3)
execute store result score #fence_2 bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:oak_fence[east=true,north=false,south=false,waterlogged=false,west=true]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:oak_fence[east=true,north=false,south=false,waterlogged=false,west=true] replace minecraft:barrier
execute unless score #fence_2 bm_timer matches 3 run scoreboard players set #valid bm_status 0

# Count oak_fence [east=false,north=false,south=true,waterlogged=false,west=true] (need exactly 5)
execute store result score #fence_3 bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:oak_fence[east=false,north=false,south=true,waterlogged=false,west=true]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:oak_fence[east=false,north=false,south=true,waterlogged=false,west=true] replace minecraft:barrier
execute unless score #fence_3 bm_timer matches 5 run scoreboard players set #valid bm_status 0

# Count oak_fence [east=false,north=true,south=true,waterlogged=false,west=false] (need exactly 6)
execute store result score #fence_4 bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:oak_fence[east=false,north=true,south=true,waterlogged=false,west=false]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:oak_fence[east=false,north=true,south=true,waterlogged=false,west=false] replace minecraft:barrier
execute unless score #fence_4 bm_timer matches 6 run scoreboard players set #valid bm_status 0

# Count oak_fence [east=true,north=true,south=false,waterlogged=false,west=false] (need exactly 5)
execute store result score #fence_5 bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:oak_fence[east=true,north=true,south=false,waterlogged=false,west=false]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:oak_fence[east=true,north=true,south=false,waterlogged=false,west=false] replace minecraft:barrier
execute unless score #fence_5 bm_timer matches 5 run scoreboard players set #valid bm_status 0

# Count oak_fence [east=false,north=false,south=false,waterlogged=false,west=true] (need exactly 3)
execute store result score #fence_6 bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:oak_fence[east=false,north=false,south=false,waterlogged=false,west=true]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:oak_fence[east=false,north=false,south=false,waterlogged=false,west=true] replace minecraft:barrier
execute unless score #fence_6 bm_timer matches 3 run scoreboard players set #valid bm_status 0

# Count oak_fence [east=true,north=false,south=false,waterlogged=false,west=false] (need exactly 3)
execute store result score #fence_7 bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:oak_fence[east=true,north=false,south=false,waterlogged=false,west=false]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:oak_fence[east=true,north=false,south=false,waterlogged=false,west=false] replace minecraft:barrier
execute unless score #fence_7 bm_timer matches 3 run scoreboard players set #valid bm_status 0

# Count oak_fence [east=false,north=true,south=false,waterlogged=false,west=true] (need exactly 5)
execute store result score #fence_8 bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:oak_fence[east=false,north=true,south=false,waterlogged=false,west=true]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:oak_fence[east=false,north=true,south=false,waterlogged=false,west=true] replace minecraft:barrier
execute unless score #fence_8 bm_timer matches 5 run scoreboard players set #valid bm_status 0

# Count oak_fence [east=false,north=true,south=false,waterlogged=false,west=false] (need exactly 2)
execute store result score #fence_9 bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:oak_fence[east=false,north=true,south=false,waterlogged=false,west=false]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:oak_fence[east=false,north=true,south=false,waterlogged=false,west=false] replace minecraft:barrier
execute unless score #fence_9 bm_timer matches 2 run scoreboard players set #valid bm_status 0

# Count oak_fence [east=false,north=false,south=true,waterlogged=false,west=false] (need exactly 2)
execute store result score #fence_10 bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:oak_fence[east=false,north=false,south=true,waterlogged=false,west=false]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:oak_fence[east=false,north=false,south=true,waterlogged=false,west=false] replace minecraft:barrier
execute unless score #fence_10 bm_timer matches 2 run scoreboard players set #valid bm_status 0

# Count oak_fence [east=true,north=false,south=true,waterlogged=false,west=true] (need exactly 8)
execute store result score #fence_11 bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:oak_fence[east=true,north=false,south=true,waterlogged=false,west=true]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:oak_fence[east=true,north=false,south=true,waterlogged=false,west=true] replace minecraft:barrier
execute unless score #fence_11 bm_timer matches 8 run scoreboard players set #valid bm_status 0

# Count oak_fence [east=true,north=true,south=true,waterlogged=false,west=false] (need exactly 9)
execute store result score #fence_12 bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:oak_fence[east=true,north=true,south=true,waterlogged=false,west=false]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:oak_fence[east=true,north=true,south=true,waterlogged=false,west=false] replace minecraft:barrier
execute unless score #fence_12 bm_timer matches 9 run scoreboard players set #valid bm_status 0

# Count oak_fence [east=true,north=true,south=true,waterlogged=false,west=true] (need exactly 4)
execute store result score #fence_13 bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:oak_fence[east=true,north=true,south=true,waterlogged=false,west=true]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:oak_fence[east=true,north=true,south=true,waterlogged=false,west=true] replace minecraft:barrier
execute unless score #fence_13 bm_timer matches 4 run scoreboard players set #valid bm_status 0

# Count oak_fence [east=true,north=true,south=false,waterlogged=false,west=true] (need exactly 8)
execute store result score #fence_14 bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:oak_fence[east=true,north=true,south=false,waterlogged=false,west=true]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:oak_fence[east=true,north=true,south=false,waterlogged=false,west=true] replace minecraft:barrier
execute unless score #fence_14 bm_timer matches 8 run scoreboard players set #valid bm_status 0

# Count oak_fence [east=false,north=true,south=true,waterlogged=false,west=true] (need exactly 9)
execute store result score #fence_15 bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:oak_fence[east=false,north=true,south=true,waterlogged=false,west=true]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:oak_fence[east=false,north=true,south=true,waterlogged=false,west=true] replace minecraft:barrier
execute unless score #fence_15 bm_timer matches 9 run scoreboard players set #valid bm_status 0

# Count stripped_oak_wood [axis=y] (need exactly 1)
execute store result score #wood_y bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:stripped_oak_wood[axis=y]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:stripped_oak_wood[axis=y] replace minecraft:barrier
execute unless score #wood_y bm_timer matches 1 run scoreboard players set #valid bm_status 0

# Count stripped_oak_wood [axis=x] (need exactly 6)
execute store result score #wood_x bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:stripped_oak_wood[axis=x]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:stripped_oak_wood[axis=x] replace minecraft:barrier
execute unless score #wood_x bm_timer matches 6 run scoreboard players set #valid bm_status 0

# Count stripped_oak_wood [axis=z] (need exactly 4)
execute store result score #wood_z bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:stripped_oak_wood[axis=z]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:stripped_oak_wood[axis=z] replace minecraft:barrier
execute unless score #wood_z bm_timer matches 4 run scoreboard players set #valid bm_status 0

# Check if structure is complete
execute if score #valid bm_status matches 1 if score #already_complete bm_status matches 0 run function buildmart:structure_2_done