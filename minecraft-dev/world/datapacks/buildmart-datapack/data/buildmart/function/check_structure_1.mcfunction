# file: check_structure_1.mcfunction

# Silent structure checking - runs every tick from timer.mcfunction
# Command block is 1 block under platform, so build area is ~-3 ~1 ~-3 to ~3 ~7 ~3

# Initialize check
scoreboard players set #valid bm_status 1

# Count light_gray_concrete (need exactly 25)
execute store result score #concrete bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:light_gray_concrete
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:light_gray_concrete replace minecraft:barrier
execute unless score #concrete bm_timer matches 25 run scoreboard players set #valid bm_status 0

# Count oak_stairs facing south (need exactly 5)
execute store result score #stairs_s bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:oak_stairs[facing=south]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:oak_stairs[facing=south] replace minecraft:barrier
execute unless score #stairs_s bm_timer matches 5 run scoreboard players set #valid bm_status 0

# Count oak_stairs facing east (need exactly 5)
execute store result score #stairs_e bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:oak_stairs[facing=east]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:oak_stairs[facing=east] replace minecraft:barrier
execute unless score #stairs_e bm_timer matches 5 run scoreboard players set #valid bm_status 0

# Count oak_stairs facing west (need exactly 5)
execute store result score #stairs_w bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:oak_stairs[facing=west]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:oak_stairs[facing=west] replace minecraft:barrier
execute unless score #stairs_w bm_timer matches 5 run scoreboard players set #valid bm_status 0

# Count oak_stairs facing north (need exactly 5)
execute store result score #stairs_n bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:oak_stairs[facing=north]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:oak_stairs[facing=north] replace minecraft:barrier
execute unless score #stairs_n bm_timer matches 5 run scoreboard players set #valid bm_status 0

# Count iron_bars (need exactly 5)
execute store result score #iron_bars bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:iron_bars
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:iron_bars replace minecraft:barrier
execute unless score #iron_bars bm_timer matches 5 run scoreboard players set #valid bm_status 0

# Check if structure is complete
execute if score #valid bm_status matches 1 if score #already_complete bm_status matches 0 run function buildmart:structure_1_done
