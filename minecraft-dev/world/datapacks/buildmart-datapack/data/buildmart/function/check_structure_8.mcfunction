# file: check_structure_8.mcfunction

# Silent structure checking - runs every tick from timer.mcfunction
# Command block is 1 block under platform, so build area is ~-3 ~1 ~-3 to ~3 ~15 ~3

# Initialize check
scoreboard players set #valid bm_status 1

# --- Block Checks for Structure 8 ---

# Count chiseled_stone_bricks (need exactly 24)
execute store result score #chiseled_stone bm_timer run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:barrier replace minecraft:chiseled_stone_bricks
execute run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:chiseled_stone_bricks replace minecraft:barrier
execute unless score #chiseled_stone bm_timer matches 24 run scoreboard players set #valid bm_status 0

# Count smooth_stone_slab [type=bottom] (need exactly 32)
execute store result score #slab_bottom bm_timer run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:barrier replace minecraft:smooth_stone_slab[type=bottom,waterlogged=false]
execute run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:smooth_stone_slab[type=bottom,waterlogged=false] replace minecraft:barrier
execute unless score #slab_bottom bm_timer matches 32 run scoreboard players set #valid bm_status 0

# Count smooth_stone_slab [type=top] (need exactly 13)
execute store result score #slab_top bm_timer run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:barrier replace minecraft:smooth_stone_slab[type=top,waterlogged=false]
execute run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:smooth_stone_slab[type=top,waterlogged=false] replace minecraft:barrier
execute unless score #slab_top bm_timer matches 13 run scoreboard players set #valid bm_status 0

# Count total stone_brick_wall blocks (need exactly 14)
execute store result score #stone_brick_wall bm_timer run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:barrier replace minecraft:stone_brick_wall
execute run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:stone_brick_wall replace minecraft:barrier
execute unless score #stone_brick_wall bm_timer matches 14 run scoreboard players set #valid bm_status 0

# Count end_rod [facing=down] 
execute store result score #end_rod_down bm_timer run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:barrier replace minecraft:end_rod[facing=down]
execute run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:end_rod[facing=down] replace minecraft:barrier

# Count end_rod [facing=up]
execute store result score #end_rod_up bm_timer run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:barrier replace minecraft:end_rod[facing=up]
execute run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:end_rod[facing=up] replace minecraft:barrier

# Count end_rod [facing=north]
execute store result score #end_rod_north bm_timer run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:barrier replace minecraft:end_rod[facing=north]
execute run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:end_rod[facing=north] replace minecraft:barrier

# Count end_rod [facing=south]
execute store result score #end_rod_south bm_timer run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:barrier replace minecraft:end_rod[facing=south]
execute run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:end_rod[facing=south] replace minecraft:barrier

# Count end_rod [facing=east]
execute store result score #end_rod_east bm_timer run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:barrier replace minecraft:end_rod[facing=east]
execute run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:end_rod[facing=east] replace minecraft:barrier

# Count end_rod [facing=west]
execute store result score #end_rod_west bm_timer run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:barrier replace minecraft:end_rod[facing=west]
execute run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:end_rod[facing=west] replace minecraft:barrier

# Sum all end rod orientations
scoreboard players operation #end_rods_total bm_timer = #end_rod_down bm_timer
scoreboard players operation #end_rods_total bm_timer += #end_rod_up bm_timer
scoreboard players operation #end_rods_total bm_timer += #end_rod_north bm_timer
scoreboard players operation #end_rods_total bm_timer += #end_rod_south bm_timer
scoreboard players operation #end_rods_total bm_timer += #end_rod_east bm_timer
scoreboard players operation #end_rods_total bm_timer += #end_rod_west bm_timer

# Check total end rods equals 5 (4 down + 1 up from original)
execute unless score #end_rods_total bm_timer matches 5 run scoreboard players set #valid bm_status 0


# --- Final Check ---
execute if score #valid bm_status matches 1 if score #already_complete bm_status matches 0 run function buildmart:structure_8_done