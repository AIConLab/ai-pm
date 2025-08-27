# file: check_structure_3.mcfunction

# Silent structure checking - runs every tick from timer.mcfunction
# Command block is 1 block under platform, so build area is ~-3 ~1 ~-3 to ~3 ~7 ~3

# Initialize check
scoreboard players set #valid bm_status 1

# Count bricks (need exactly 13)
execute store result score #bricks bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:bricks
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:bricks replace minecraft:barrier
execute unless score #bricks bm_timer matches 13 run scoreboard players set #valid bm_status 0

# Count heavy_weighted_pressure_plate (need exactly 2)
execute store result score #pressure_plate bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:heavy_weighted_pressure_plate
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:heavy_weighted_pressure_plate replace minecraft:barrier
execute unless score #pressure_plate bm_timer matches 2 run scoreboard players set #valid bm_status 0

# Only check door when all other blocks are correct - prevents constant door destruction
execute if score #bricks bm_timer matches 13 if score #pressure_plate bm_timer matches 2 if score #pale_planks bm_timer matches 15 if score #glass bm_timer matches 14 if score #slab_double bm_timer matches 4 if score #slab_bottom bm_timer matches 24 run function buildmart:check_door_structure_3

# Count pale_oak_planks (need exactly 15)
execute store result score #pale_planks bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:pale_oak_planks
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:pale_oak_planks replace minecraft:barrier
execute unless score #pale_planks bm_timer matches 15 run scoreboard players set #valid bm_status 0

# Count glass (need exactly 14)
execute store result score #glass bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:glass
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:glass replace minecraft:barrier
execute unless score #glass bm_timer matches 14 run scoreboard players set #valid bm_status 0

# Count pale_oak_slab[type=double] (need exactly 4)
execute store result score #slab_double bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:pale_oak_slab[type=double]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:pale_oak_slab[type=double] replace minecraft:barrier
execute unless score #slab_double bm_timer matches 4 run scoreboard players set #valid bm_status 0

# Count pale_oak_slab[type=bottom] (need exactly 24)
execute store result score #slab_bottom bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:pale_oak_slab[type=bottom]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:pale_oak_slab[type=bottom] replace minecraft:barrier
execute unless score #slab_bottom bm_timer matches 24 run scoreboard players set #valid bm_status 0

# Structure completion is handled by door check function when all blocks are correct