# file: check_structure_4.mcfunction

# Silent structure checking - runs every tick from timer.mcfunction
# Command block is 1 block under platform, so build area is ~-3 ~1 ~-3 to ~3 ~15 ~3

# Initialize check
scoreboard players set #valid bm_status 1

# Count iron_block (need exactly 12)
execute store result score #iron_block bm_timer run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:barrier replace minecraft:iron_block
execute run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:iron_block replace minecraft:barrier
execute unless score #iron_block bm_timer matches 12 run scoreboard players set #valid bm_status 0

# POWERED TRAPDOORS - Keep exact orientations (for redstone circuit)
# Count iron_trapdoor [facing=south,half=bottom,open=true,powered=true,waterlogged=false] (need exactly 1)
execute store result score #trapdoor_s_open bm_timer run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:barrier replace minecraft:iron_trapdoor[facing=south,half=bottom,open=true,powered=true,waterlogged=false]
execute run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:iron_trapdoor[facing=south,half=bottom,open=true,powered=true,waterlogged=false] replace minecraft:barrier
execute unless score #trapdoor_s_open bm_timer matches 1 run scoreboard players set #valid bm_status 0

# Count iron_trapdoor [facing=east,half=bottom,open=true,powered=true,waterlogged=false] (need exactly 4)
execute store result score #trapdoor_e_open bm_timer run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:barrier replace minecraft:iron_trapdoor[facing=east,half=bottom,open=true,powered=true,waterlogged=false]
execute run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:iron_trapdoor[facing=east,half=bottom,open=true,powered=true,waterlogged=false] replace minecraft:barrier
execute unless score #trapdoor_e_open bm_timer matches 4 run scoreboard players set #valid bm_status 0

# Count iron_trapdoor [facing=west,half=bottom,open=true,powered=true,waterlogged=false] (need exactly 4)
execute store result score #trapdoor_w_open bm_timer run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:barrier replace minecraft:iron_trapdoor[facing=west,half=bottom,open=true,powered=true,waterlogged=false]
execute run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:iron_trapdoor[facing=west,half=bottom,open=true,powered=true,waterlogged=false] replace minecraft:barrier
execute unless score #trapdoor_w_open bm_timer matches 4 run scoreboard players set #valid bm_status 0

# Count redstone_torch [lit=true] (need exactly 4)
execute store result score #redstone_torch bm_timer run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:barrier replace minecraft:redstone_torch[lit=true]
execute run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:redstone_torch[lit=true] replace minecraft:barrier
execute unless score #redstone_torch bm_timer matches 4 run scoreboard players set #valid bm_status 0

# Count iron_door (check only lower half - need exactly 1 door total)
execute store result score #iron_door bm_timer run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:barrier replace minecraft:iron_door[facing=north,half=lower,hinge=right,open=true,powered=true]
execute run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:iron_door[facing=north,half=lower,hinge=right,open=true,powered=true] replace minecraft:barrier
execute unless score #iron_door bm_timer matches 1 run scoreboard players set #valid bm_status 0

# Count orange_concrete (need exactly 19)
execute store result score #orange_concrete bm_timer run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:barrier replace minecraft:orange_concrete
execute run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:orange_concrete replace minecraft:barrier
execute unless score #orange_concrete bm_timer matches 19 run scoreboard players set #valid bm_status 0

# FLEXIBLE: Count UNPOWERED trapdoors in all orientations (need exactly 18 total: 6+12 from original)
# Count north-facing unpowered trapdoors
execute store result score #trapdoor_n_unpowered bm_timer run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:barrier replace minecraft:iron_trapdoor[facing=north,half=bottom,open=false,powered=false,waterlogged=false]
execute run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:iron_trapdoor[facing=north,half=bottom,open=false,powered=false,waterlogged=false] replace minecraft:barrier

# Count south-facing unpowered trapdoors
execute store result score #trapdoor_s_unpowered bm_timer run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:barrier replace minecraft:iron_trapdoor[facing=south,half=bottom,open=false,powered=false,waterlogged=false]
execute run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:iron_trapdoor[facing=south,half=bottom,open=false,powered=false,waterlogged=false] replace minecraft:barrier

# Count east-facing unpowered trapdoors
execute store result score #trapdoor_e_unpowered bm_timer run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:barrier replace minecraft:iron_trapdoor[facing=east,half=bottom,open=false,powered=false,waterlogged=false]
execute run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:iron_trapdoor[facing=east,half=bottom,open=false,powered=false,waterlogged=false] replace minecraft:barrier

# Count west-facing unpowered trapdoors
execute store result score #trapdoor_w_unpowered bm_timer run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:barrier replace minecraft:iron_trapdoor[facing=west,half=bottom,open=false,powered=false,waterlogged=false]
execute run fill ~-3 ~1 ~-3 ~3 ~15 ~3 minecraft:iron_trapdoor[facing=west,half=bottom,open=false,powered=false,waterlogged=false] replace minecraft:barrier

# Sum all unpowered trapdoor orientations
scoreboard players operation #trapdoor_unpowered_total bm_timer = #trapdoor_n_unpowered bm_timer
scoreboard players operation #trapdoor_unpowered_total bm_timer += #trapdoor_s_unpowered bm_timer
scoreboard players operation #trapdoor_unpowered_total bm_timer += #trapdoor_e_unpowered bm_timer
scoreboard players operation #trapdoor_unpowered_total bm_timer += #trapdoor_w_unpowered bm_timer

# Check total unpowered trapdoors equals 18 (original: 6 east + 12 north)
execute unless score #trapdoor_unpowered_total bm_timer matches 18 run scoreboard players set #valid bm_status 0

# Check if structure is complete
execute if score #valid bm_status matches 1 if score #already_complete bm_status matches 0 run function buildmart:structure_4_done