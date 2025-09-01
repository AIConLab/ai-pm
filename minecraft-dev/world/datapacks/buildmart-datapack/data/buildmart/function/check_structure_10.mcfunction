# file: check_structure_10.mcfunction

# Silent structure checking - runs every tick from timer.mcfunction
# Command block is 1 block under platform, so build area is ~-3 ~1 ~-3 to ~3 ~15 ~3

# Initialize check
scoreboard players set #valid bm_status 1

# --- Block Checks for Structure 10 ---

# Count iron_block (need exactly 7)
execute store result score #iron_block bm_timer run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:barrier replace minecraft:iron_block
execute run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:iron_block replace minecraft:barrier
execute unless score #iron_block bm_timer matches 7 run scoreboard players set #valid bm_status 0

# Count total iron_bars (need exactly 6)
execute store result score #iron_bars bm_timer run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:barrier replace minecraft:iron_bars
execute run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:iron_bars replace minecraft:barrier
execute unless score #iron_bars bm_timer matches 6 run scoreboard players set #valid bm_status 0

# Count iron_trapdoor [facing=east] (need exactly 4)
execute store result score #trapdoor_e bm_timer run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:barrier replace minecraft:iron_trapdoor[facing=east,half=bottom,open=false,powered=false,waterlogged=false]
execute run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:iron_trapdoor[facing=east,half=bottom,open=false,powered=false,waterlogged=false] replace minecraft:barrier
execute unless score #trapdoor_e bm_timer matches 4 run scoreboard players set #valid bm_status 0

# Count iron_trapdoor [facing=north] (need exactly 1)
execute store result score #trapdoor_n bm_timer run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:barrier replace minecraft:iron_trapdoor[facing=north,half=bottom,open=false,powered=false,waterlogged=false]
execute run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:iron_trapdoor[facing=north,half=bottom,open=false,powered=false,waterlogged=false] replace minecraft:barrier
execute unless score #trapdoor_n bm_timer matches 1 run scoreboard players set #valid bm_status 0

# Count iron_trapdoor [facing=south] (need exactly 1)
execute store result score #trapdoor_s bm_timer run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:barrier replace minecraft:iron_trapdoor[facing=south,half=bottom,open=false,powered=false,waterlogged=false]
execute run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:iron_trapdoor[facing=south,half=bottom,open=false,powered=false,waterlogged=false] replace minecraft:barrier
execute unless score #trapdoor_s bm_timer matches 1 run scoreboard players set #valid bm_status 0

# Count red_wall_banner [facing=north] (need exactly 2)
execute store result score #banner_n bm_timer run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:barrier replace minecraft:red_wall_banner[facing=north]
execute run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:red_wall_banner[facing=north] replace minecraft:barrier
execute unless score #banner_n bm_timer matches 2 run scoreboard players set #valid bm_status 0

# Count red_wall_banner [facing=west] (need exactly 2)
execute store result score #banner_w bm_timer run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:barrier replace minecraft:red_wall_banner[facing=west]
execute run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:red_wall_banner[facing=west] replace minecraft:barrier
execute unless score #banner_w bm_timer matches 2 run scoreboard players set #valid bm_status 0

# Count red_wall_banner [facing=east] (need exactly 2)
execute store result score #banner_e bm_timer run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:barrier replace minecraft:red_wall_banner[facing=east]
execute run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:red_wall_banner[facing=east] replace minecraft:barrier
execute unless score #banner_e bm_timer matches 2 run scoreboard players set #valid bm_status 0

# Count red_wall_banner [facing=south] (need exactly 2)
execute store result score #banner_s bm_timer run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:barrier replace minecraft:red_wall_banner[facing=south]
execute run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:red_wall_banner[facing=south] replace minecraft:barrier
execute unless score #banner_s bm_timer matches 2 run scoreboard players set #valid bm_status 0

# --- Final Check ---
execute if score #valid bm_status matches 1 if score #already_complete bm_status matches 0 run function buildmart:structure_10_done