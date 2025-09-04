# file: check_structure_6.mcfunction

# Silent structure checking - runs every tick from timer.mcfunction
# Command block is 1 block under platform, so build area is ~-3 ~1 ~-3 to ~3 ~15 ~3

# Initialize chek
scoreboard players set #valid bm_status 1

# Count light_gray_concrete (need exactly 15)
execute store result score #light_concrete bm_timer run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:barrier replace minecraft:light_gray_concrete
execute run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:light_gray_concrete replace minecraft:barrier
execute unless score #light_concrete bm_timer matches 15 run scoreboard players set #valid bm_status 0

# Count total brick_wall blocks (need exactly 41 total - sum of all wall variants)
# Wall blocks automatically connect, so we count total rather than specific connection states
execute store result score #brick_walls bm_timer run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:barrier replace minecraft:brick_wall
execute run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:brick_wall replace minecraft:barrier
execute unless score #brick_walls bm_timer matches 41 run scoreboard players set #valid bm_status 0

# Count waxed_oxidized_cut_copper_stairs [facing=north,half=bottom,shape=straight,waterlogged=false] (need exactly 3)
execute store result score #copper_stairs bm_timer run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:barrier replace minecraft:waxed_oxidized_cut_copper_stairs[facing=north,half=bottom,shape=straight,waterlogged=false]
execute run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:waxed_oxidized_cut_copper_stairs[facing=north,half=bottom,shape=straight,waterlogged=false] replace minecraft:barrier
execute unless score #copper_stairs bm_timer matches 3 run scoreboard players set #valid bm_status 0

# Count polished_diorite_stairs [facing=south,half=bottom,shape=straight,waterlogged=false] (need exactly 7)
execute store result score #diorite_stairs bm_timer run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:barrier replace minecraft:polished_diorite_stairs[facing=south,half=bottom,shape=straight,waterlogged=false]
execute run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:polished_diorite_stairs[facing=south,half=bottom,shape=straight,waterlogged=false] replace minecraft:barrier
execute unless score #diorite_stairs bm_timer matches 7 run scoreboard players set #valid bm_status 0

# Count dark_oak_hanging_sign [attached=false,rotation=0,waterlogged=false] (need exactly 1)
execute store result score #hanging_sign bm_timer run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:barrier replace minecraft:dark_oak_hanging_sign[attached=false,rotation=0,waterlogged=false]
execute run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:dark_oak_hanging_sign[attached=false,rotation=0,waterlogged=false] replace minecraft:barrier
execute unless score #hanging_sign bm_timer matches 1 run scoreboard players set #valid bm_status 0

# FLEXIBLE: Count iron trapdoors in all orientations (need exactly 21 total: 7+8+6 from original)
# Count north-facing trapdoors
execute store result score #trapdoor_n bm_timer run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:barrier replace minecraft:iron_trapdoor[facing=north,half=bottom,open=false,powered=false,waterlogged=false]
execute run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:iron_trapdoor[facing=north,half=bottom,open=false,powered=false,waterlogged=false] replace minecraft:barrier

# Count south-facing trapdoors  
execute store result score #trapdoor_s bm_timer run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:barrier replace minecraft:iron_trapdoor[facing=south,half=bottom,open=false,powered=false,waterlogged=false]
execute run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:iron_trapdoor[facing=south,half=bottom,open=false,powered=false,waterlogged=false] replace minecraft:barrier

# Count east-facing trapdoors
execute store result score #trapdoor_e bm_timer run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:barrier replace minecraft:iron_trapdoor[facing=east,half=bottom,open=false,powered=false,waterlogged=false]
execute run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:iron_trapdoor[facing=east,half=bottom,open=false,powered=false,waterlogged=false] replace minecraft:barrier

# Count west-facing trapdoors (allows players to use this orientation too)
execute store result score #trapdoor_w bm_timer run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:barrier replace minecraft:iron_trapdoor[facing=west,half=bottom,open=false,powered=false,waterlogged=false]
execute run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:iron_trapdoor[facing=west,half=bottom,open=false,powered=false,waterlogged=false] replace minecraft:barrier

# Sum all trapdoor orientations
scoreboard players operation #trapdoor_total bm_timer = #trapdoor_n bm_timer
scoreboard players operation #trapdoor_total bm_timer += #trapdoor_s bm_timer
scoreboard players operation #trapdoor_total bm_timer += #trapdoor_e bm_timer
scoreboard players operation #trapdoor_total bm_timer += #trapdoor_w bm_timer

# Check total trapdoors equals 21 (original: 7 north + 8 south + 6 east)
execute unless score #trapdoor_total bm_timer matches 21 run scoreboard players set #valid bm_status 0

# Check if structure is complete
execute if score #valid bm_status matches 1 if score #already_complete bm_status matches 0 run function buildmart:structure_6_done