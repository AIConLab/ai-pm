# file: check_structure_4.mcfunction

# Silent structure checking - runs every tick from timer.mcfunction
# Command block is 1 block under platform, so build area is ~-3 ~1 ~-3 to ~3 ~7 ~3

# Initialize check
scoreboard players set #valid bm_status 1

# Count iron_block (need exactly 12)
execute store result score #iron_block bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:iron_block
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:iron_block replace minecraft:barrier
execute unless score #iron_block bm_timer matches 12 run scoreboard players set #valid bm_status 0

# Count iron_trapdoor [facing=south,half=bottom,open=true,powered=true,waterlogged=false] (need exactly 1)
execute store result score #trapdoor_s_open bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:iron_trapdoor[facing=south,half=bottom,open=true,powered=true,waterlogged=false]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:iron_trapdoor[facing=south,half=bottom,open=true,powered=true,waterlogged=false] replace minecraft:barrier
execute unless score #trapdoor_s_open bm_timer matches 1 run scoreboard players set #valid bm_status 0

# Count iron_trapdoor [facing=east,half=bottom,open=true,powered=true,waterlogged=false] (need exactly 4)
execute store result score #trapdoor_e_open bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:iron_trapdoor[facing=east,half=bottom,open=true,powered=true,waterlogged=false]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:iron_trapdoor[facing=east,half=bottom,open=true,powered=true,waterlogged=false] replace minecraft:barrier
execute unless score #trapdoor_e_open bm_timer matches 4 run scoreboard players set #valid bm_status 0

# Count redstone_torch [lit=true] (need exactly 4)
execute store result score #redstone_torch bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:redstone_torch[lit=true]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:redstone_torch[lit=true] replace minecraft:barrier
execute unless score #redstone_torch bm_timer matches 4 run scoreboard players set #valid bm_status 0

# Count iron_trapdoor [facing=west,half=bottom,open=true,powered=true,waterlogged=false] (need exactly 4)
execute store result score #trapdoor_w_open bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:iron_trapdoor[facing=west,half=bottom,open=true,powered=true,waterlogged=false]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:iron_trapdoor[facing=west,half=bottom,open=true,powered=true,waterlogged=false] replace minecraft:barrier
execute unless score #trapdoor_w_open bm_timer matches 4 run scoreboard players set #valid bm_status 0

# Count iron_door (check only lower half - need exactly 1 door total)
# When a door is placed, both upper and lower halves are created automatically
execute store result score #iron_door bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:iron_door[facing=north,half=lower,hinge=right,open=true,powered=true]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:iron_door[facing=north,half=lower,hinge=right,open=true,powered=true] replace minecraft:barrier
execute unless score #iron_door bm_timer matches 1 run scoreboard players set #valid bm_status 0

# Count orange_concrete (need exactly 19)
execute store result score #orange_concrete bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:orange_concrete
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:orange_concrete replace minecraft:barrier
execute unless score #orange_concrete bm_timer matches 19 run scoreboard players set #valid bm_status 0

# Count iron_trapdoor [facing=east,half=bottom,open=false,powered=false,waterlogged=false] (need exactly 6)
execute store result score #trapdoor_e_closed bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:iron_trapdoor[facing=east,half=bottom,open=false,powered=false,waterlogged=false]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:iron_trapdoor[facing=east,half=bottom,open=false,powered=false,waterlogged=false] replace minecraft:barrier
execute unless score #trapdoor_e_closed bm_timer matches 6 run scoreboard players set #valid bm_status 0

# Count iron_trapdoor [facing=north,half=bottom,open=false,powered=false,waterlogged=false] (need exactly 12)
execute store result score #trapdoor_n_closed bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:iron_trapdoor[facing=north,half=bottom,open=false,powered=false,waterlogged=false]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:iron_trapdoor[facing=north,half=bottom,open=false,powered=false,waterlogged=false] replace minecraft:barrier
execute unless score #trapdoor_n_closed bm_timer matches 12 run scoreboard players set #valid bm_status 0

# Check if structure is complete
execute if score #valid bm_status matches 1 if score #already_complete bm_status matches 0 run function buildmart:structure_4_done