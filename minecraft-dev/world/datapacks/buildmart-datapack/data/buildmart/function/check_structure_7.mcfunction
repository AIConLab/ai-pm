# file: check_structure_7.mcfunction

# Silent structure checking - runs every tick from timer.mcfunction
# Command block is 1 block under platform, so build area is ~-3 ~1 ~-3 to ~3 ~7 ~3

# Initialize check
scoreboard players set #valid bm_status 1

# --- BLOCKS WITH NO STATES or SIMPLE STATES ---

# Check peony at the four corners (need 4)
scoreboard players set #peony_count bm_timer 0
execute if block ~-3 ~1 ~-3 minecraft:peony[half=lower] run scoreboard players add #peony_count bm_timer 1
execute if block ~3 ~1 ~-3 minecraft:peony[half=lower] run scoreboard players add #peony_count bm_timer 1
execute if block ~3 ~1 ~3 minecraft:peony[half=lower] run scoreboard players add #peony_count bm_timer 1
execute if block ~-3 ~1 ~3 minecraft:peony[half=lower] run scoreboard players add #peony_count bm_timer 1
execute unless score #peony_count bm_timer matches 4 run scoreboard players set #valid bm_status 0

# Count oak_planks (need 8) - No states to preserve
execute store result score #oak_planks bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:oak_planks
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:oak_planks replace minecraft:barrier
execute unless score #oak_planks bm_timer matches 8 run scoreboard players set #valid bm_status 0

# Count total oak_fence blocks (need 44) - Connection states are automatic, total count is most reliable
execute store result score #oak_fence bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:oak_fence
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:oak_fence replace minecraft:barrier
execute unless score #oak_fence bm_timer matches 44 run scoreboard players set #valid bm_status 0

# Count stripped_oak_wood [axis=y] (need 20)
execute store result score #stripped_wood_y bm_timer run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:barrier replace minecraft:stripped_oak_wood[axis=y]
execute run fill ~-3 ~1 ~-3 ~3 ~7 ~3 minecraft:stripped_oak_wood[axis=y] replace minecraft:barrier
execute unless score #stripped_wood_y bm_timer matches 20 run scoreboard players set #valid bm_status 0
