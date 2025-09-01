# file: check_structure_2.mcfunction

# Silent structure checking - runs every tick from timer.mcfunction
# Command block is 1 block under platform, so build area is ~-3 ~1 ~-3 to ~3 ~7 ~3

# Initialize check
scoreboard players set #valid bm_status 1

# Count total oak_fence blocks (need exactly 77 total - sum of all fence variants)
execute store result score #oak_fence bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:oak_fence
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:oak_fence replace minecraft:barrier
execute unless score #oak_fence bm_timer matches 77 run scoreboard players set #valid bm_status 0

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