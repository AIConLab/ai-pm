# file: check_structure_9.mcfunction

# Silent structure checking - runs every tick from timer.mcfunction
# Command block is 1 block under platform, so build area is ~-3 ~1 ~-3 to ~3 ~15 ~3

# Initialize check
scoreboard players set #valid bm_status 1

# --- Block Checks for Structure 9 ---

# Count total iron_bars (need exactly 18)
execute store result score #iron_bars bm_timer run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:barrier replace minecraft:iron_bars
execute run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:iron_bars replace minecraft:barrier
execute unless score #iron_bars bm_timer matches 18 run scoreboard players set #valid bm_status 0

# Count smooth_stone_slab [type=bottom] (need exactly 19)
execute store result score #slab_bottom bm_timer run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:barrier replace minecraft:smooth_stone_slab[type=bottom,waterlogged=false]
execute run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:smooth_stone_slab[type=bottom,waterlogged=false] replace minecraft:barrier
execute unless score #slab_bottom bm_timer matches 19 run scoreboard players set #valid bm_status 0

# FLEXIBLE: Count iron trapdoors in all orientations (need exactly 16 total)
# Count west-facing trapdoors
execute store result score #trapdoor_w bm_timer run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:barrier replace minecraft:iron_trapdoor[facing=west,half=bottom,open=false,powered=false,waterlogged=false]
execute run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:iron_trapdoor[facing=west,half=bottom,open=false,powered=false,waterlogged=false] replace minecraft:barrier

# Count east-facing trapdoors
execute store result score #trapdoor_e bm_timer run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:barrier replace minecraft:iron_trapdoor[facing=east,half=bottom,open=false,powered=false,waterlogged=false]
execute run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:iron_trapdoor[facing=east,half=bottom,open=false,powered=false,waterlogged=false] replace minecraft:barrier

# Count south-facing trapdoors
execute store result score #trapdoor_s bm_timer run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:barrier replace minecraft:iron_trapdoor[facing=south,half=bottom,open=false,powered=false,waterlogged=false]
execute run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:iron_trapdoor[facing=south,half=bottom,open=false,powered=false,waterlogged=false] replace minecraft:barrier

# Count north-facing trapdoors
execute store result score #trapdoor_n bm_timer run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:barrier replace minecraft:iron_trapdoor[facing=north,half=bottom,open=false,powered=false,waterlogged=false]
execute run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:iron_trapdoor[facing=north,half=bottom,open=false,powered=false,waterlogged=false] replace minecraft:barrier

# Sum all trapdoor orientations
scoreboard players operation #trapdoor_total bm_timer = #trapdoor_w bm_timer
scoreboard players operation #trapdoor_total bm_timer += #trapdoor_e bm_timer
scoreboard players operation #trapdoor_total bm_timer += #trapdoor_s bm_timer
scoreboard players operation #trapdoor_total bm_timer += #trapdoor_n bm_timer

# Check total trapdoors equals 16 (8+2+1+5 from original)
execute unless score #trapdoor_total bm_timer matches 16 run scoreboard players set #valid bm_status 0

# --- Final Check ---
execute if score #valid bm_status matches 1 if score #already_complete bm_status matches 0 run function buildmart:structure_9_done