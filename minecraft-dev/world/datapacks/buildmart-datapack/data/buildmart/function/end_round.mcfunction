# ===========================================
# File: data/buildmart/function/end_round.mcfunction
# ===========================================

# End the round and calculate time
execute if score #round_active bm_status matches 0 run tellraw @s {"text":"No round currently active!","color":"red"}
execute if score #round_active bm_status matches 0 run return fail

# Set round as inactive
scoreboard players set #round_active bm_status 0

# Record end time
execute store result score #end_time bm_end run time query gametime

# Calculate total time in ticks
scoreboard players operation #total_ticks bm_timer = #end_time bm_end
scoreboard players operation #total_ticks bm_timer -= #start_time bm_start

# Convert to seconds
scoreboard players operation #total_seconds bm_final = #total_ticks bm_timer
scoreboard players operation #total_seconds bm_final /= #20 bm_timer

# Announce results
title @a title {"text":"ROUND ENDED","color":"gold","bold":true}
title @a subtitle [{"text":"Total Time: ","color":"green"},{"score":{"name":"#total_seconds","objective":"bm_final"},"color":"yellow"},{"text":" seconds","color":"green"}]

# Debug: Show the completion time
tellraw @a [{"text":"[DEBUG] Completion time: ","color":"gray"},{"score":{"name":"#total_seconds","objective":"bm_final"},"color":"white"},{"text":" seconds","color":"gray"}]

# Update team scoreboard - simplified approach
# Just set the time directly instead of using operations
scoreboard players operation AI_Project_Manager teams = #total_seconds bm_final
scoreboard players operation Human_Project_Manager teams = #total_seconds bm_final  
scoreboard players operation No_Project_Manager teams = #total_seconds bm_final

# Debug: Show what we set
tellraw @a [{"text":"[DEBUG] Updated all team scores to: ","color":"gray"},{"score":{"name":"#total_seconds","objective":"bm_final"},"color":"white"}]

playsound minecraft:ui.toast.challenge_complete master @a ~ ~ ~ 1 1

tellraw @a [{"text":"[BUILD MART] Round completed in ","color":"green"},{"score":{"name":"#total_seconds","objective":"bm_final"},"color":"yellow"},{"text":" seconds!","color":"green"}]
