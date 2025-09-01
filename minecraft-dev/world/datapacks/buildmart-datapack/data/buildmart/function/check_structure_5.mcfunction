# file: check_structure_5.mcfunction

# Silent structure checking - runs every tick from timer.mcfunction
# Command block is 1 block under platform, so build area is ~-3 ~1 ~-3 to ~3 ~7 ~3

# Initialize check
scoreboard players set #valid bm_status 1

# Count light_gray_concrete (need exactly 16)
execute store result score #light_concrete bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:light_gray_concrete
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:light_gray_concrete replace minecraft:barrier
execute unless score #light_concrete bm_timer matches 16 run scoreboard players set #valid bm_status 0

# Count iron_block (need exactly 49)
execute store result score #iron_block bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:iron_block
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:iron_block replace minecraft:barrier
execute unless score #iron_block bm_timer matches 49 run scoreboard players set #valid bm_status 0

# Count iron_door (check only lower half - need exactly 1 door total)
# When a door is placed, both upper and lower halves are created automatically
execute store result score #iron_door bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:iron_door[facing=west,half=lower,hinge=left,open=false,powered=false]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:iron_door[facing=west,half=lower,hinge=left,open=false,powered=false] replace minecraft:barrier
execute unless score #iron_door bm_timer matches 1 run scoreboard players set #valid bm_status 0

# Count pale_oak_trapdoor [facing=north,half=bottom,open=true,powered=false,waterlogged=false] (need exactly 18)
execute store result score #trapdoor_n bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:pale_oak_trapdoor[facing=north,half=bottom,open=true,powered=false,waterlogged=false]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:pale_oak_trapdoor[facing=north,half=bottom,open=true,powered=false,waterlogged=false] replace minecraft:barrier
execute unless score #trapdoor_n bm_timer matches 18 run scoreboard players set #valid bm_status 0

# Count stone_button [face=wall,facing=east,powered=false] (need exactly 1)
execute store result score #button_e bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:stone_button[face=wall,facing=east,powered=false]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:stone_button[face=wall,facing=east,powered=false] replace minecraft:barrier
execute unless score #button_e bm_timer matches 1 run scoreboard players set #valid bm_status 0

# Count stone_button [face=wall,facing=west,powered=false] (need exactly 1)
execute store result score #button_w bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:stone_button[face=wall,facing=west,powered=false]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:stone_button[face=wall,facing=west,powered=false] replace minecraft:barrier
execute unless score #button_w bm_timer matches 1 run scoreboard players set #valid bm_status 0

# Count glass (need exactly 1)
execute store result score #glass bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:glass
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:glass replace minecraft:barrier
execute unless score #glass bm_timer matches 1 run scoreboard players set #valid bm_status 0

# Count deepslate_tile_stairs [facing=east,half=bottom,shape=straight,waterlogged=false] (need exactly 18)
execute store result score #stairs_e bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:deepslate_tile_stairs[facing=east,half=bottom,shape=straight,waterlogged=false]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:deepslate_tile_stairs[facing=east,half=bottom,shape=straight,waterlogged=false] replace minecraft:barrier
execute unless score #stairs_e bm_timer matches 18 run scoreboard players set #valid bm_status 0

# Count deepslate_tile_stairs [facing=west,half=bottom,shape=straight,waterlogged=false] (need exactly 18)
execute store result score #stairs_w bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:deepslate_tile_stairs[facing=west,half=bottom,shape=straight,waterlogged=false]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:deepslate_tile_stairs[facing=west,half=bottom,shape=straight,waterlogged=false] replace minecraft:barrier
execute unless score #stairs_w bm_timer matches 18 run scoreboard players set #valid bm_status 0

# Count end_rod [facing=east] (need exactly 2)
execute store result score #end_rod_e bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:end_rod[facing=east]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:end_rod[facing=east] replace minecraft:barrier
execute unless score #end_rod_e bm_timer matches 2 run scoreboard players set #valid bm_status 0

# Count end_rod [facing=west] (need exactly 2)
execute store result score #end_rod_w bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:end_rod[facing=west]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:end_rod[facing=west] replace minecraft:barrier
execute unless score #end_rod_w bm_timer matches 2 run scoreboard players set #valid bm_status 0

# Count pale_oak_trapdoor [facing=south,half=bottom,open=true,powered=false,waterlogged=false] (need exactly 2)
execute store result score #trapdoor_s bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:pale_oak_trapdoor[facing=south,half=bottom,open=true,powered=false,waterlogged=false]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:pale_oak_trapdoor[facing=south,half=bottom,open=true,powered=false,waterlogged=false] replace minecraft:barrier
execute unless score #trapdoor_s bm_timer matches 2 run scoreboard players set #valid bm_status 0

# Check if structure is complete
execute if score #valid bm_status matches 1 if score #already_complete bm_status matches 0 run function buildmart:structure_5_done