# ===========================================
# File: data/buildmart/function/start_round.mcfunction
# ===========================================

# Start the round timer
execute if score #round_active bm_status matches 1 run tellraw @s {"text":"Round already active! Use /function buildmart:end_round first","color":"red"}
execute if score #round_active bm_status matches 1 run return fail

# Set round as active
scoreboard players set #round_active bm_status 1

# Record start time
execute store result score #start_time bm_start run time query gametime

# Announce start
title @a title {"text":"ROUND STARTED","color":"gold","bold":true}
title @a subtitle {"text":"Build Structure 1 as fast as possible!","color":"yellow"}
playsound minecraft:block.note_block.chime master @a ~ ~ ~ 1 2

say [BUILD MART] Round timer started! Build Structure 1 now.
