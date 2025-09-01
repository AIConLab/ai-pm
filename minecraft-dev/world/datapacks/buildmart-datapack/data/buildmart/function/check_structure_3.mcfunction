# file: check_structure_3.mcfunction

# Silent structure checking - runs every tick from timer.mcfunction
# Command block is 1 block under platform, so build area is ~-3 ~1 ~-3 to ~3 ~7 ~3

# Initialize check
scoreboard players set #valid bm_status 1

# Count bricks (need exactly 13)
execute store result score #bricks bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:bricks
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:bricks replace minecraft:barrier
execute unless score #bricks bm_timer matches 13 run scoreboard players set #valid bm_status 0

# Count heavy_weighted_pressure_plate [power=0] (need exactly 2)
execute store result score #pressure_plate bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:heavy_weighted_pressure_plate[power=0]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:heavy_weighted_pressure_plate[power=0] replace minecraft:barrier
execute unless score #pressure_plate bm_timer matches 2 run scoreboard players set #valid bm_status 0

# Count iron_door (check only lower half - need exactly 1 door total)
# When a door is placed, both upper and lower halves are created automatically
execute store result score #iron_door bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:iron_door[facing=north,half=lower,hinge=left,open=false,powered=false]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:iron_door[facing=north,half=lower,hinge=left,open=false,powered=false] replace minecraft:barrier
execute unless score #iron_door bm_timer matches 1 run scoreboard players set #valid bm_status 0

# Count pale_oak_planks (need exactly 15)
execute store result score #pale_planks bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:pale_oak_planks
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:pale_oak_planks replace minecraft:barrier
execute unless score #pale_planks bm_timer matches 15 run scoreboard players set #valid bm_status 0

# Count glass (need exactly 14)
execute store result score #glass bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:glass
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:glass replace minecraft:barrier
execute unless score #glass bm_timer matches 14 run scoreboard players set #valid bm_status 0

# Count pale_oak_slab [type=double,waterlogged=false] (need exactly 4)
execute store result score #pale_slab_double bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:pale_oak_slab[type=double,waterlogged=false]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:pale_oak_slab[type=double,waterlogged=false] replace minecraft:barrier
execute unless score #pale_slab_double bm_timer matches 4 run scoreboard players set #valid bm_status 0

# Count pale_oak_slab [type=bottom,waterlogged=false] (need exactly 24)
execute store result score #pale_slab_bottom bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:pale_oak_slab[type=bottom,waterlogged=false]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:pale_oak_slab[type=bottom,waterlogged=false] replace minecraft:barrier
execute unless score #pale_slab_bottom bm_timer matches 24 run scoreboard players set #valid bm_status 0

# Check if structure is complete
execute if score #valid bm_status matches 1 if score #already_complete bm_status matches 0 run function buildmart:structure_3_done