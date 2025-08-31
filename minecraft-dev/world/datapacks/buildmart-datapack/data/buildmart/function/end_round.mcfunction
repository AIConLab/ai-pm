# file: end_round.mcfunction
# Check if round is active
execute if score #round_active bm_status matches 0 run tellraw @s {"text":"No round currently active!","color":"red"}
execute if score #round_active bm_status matches 0 run return fail

# Set round as inactive
scoreboard players set #round_active bm_status 0

# Record end time and calculate duration
execute store result score #end_time bm_end run time query gametime
scoreboard players operation #total_ticks bm_timer = #end_time bm_end
scoreboard players operation #total_ticks bm_timer -= #start_time bm_start

# Convert to seconds
scoreboard players operation #total_seconds bm_final = #total_ticks bm_timer
scoreboard players operation #total_seconds bm_final /= #20 bm_timer

# Store completion time for current round
execute if score #current current_round matches 1 run scoreboard players operation Round_1 round_times = #total_seconds bm_final
execute if score #current current_round matches 2 run scoreboard players operation Round_2 round_times = #total_seconds bm_final
execute if score #current current_round matches 3 run scoreboard players operation Round_3 round_times = #total_seconds bm_final
execute if score #current current_round matches 4 run scoreboard players operation Round_4 round_times = #total_seconds bm_final
execute if score #current current_round matches 5 run scoreboard players operation Round_5 round_times = #total_seconds bm_final
execute if score #current current_round matches 6 run scoreboard players operation Round_6 round_times = #total_seconds bm_final
execute if score #current current_round matches 7 run scoreboard players operation Round_7 round_times = #total_seconds bm_final
execute if score #current current_round matches 8 run scoreboard players operation Round_8 round_times = #total_seconds bm_final
execute if score #current current_round matches 9 run scoreboard players operation Round_9 round_times = #total_seconds bm_final

# Teleport all players to the break area
tp @a -55.39 65 96.847

# End sequence
title @a title {"text":"COMPLETE!","color":"green","bold":true}
title @a subtitle [{"text":"Round ","color":"white"},{"score":{"name":"#current","objective":"current_round"},"color":"yellow","bold":true},{"text":" - ","color":"white"},{"score":{"name":"#total_seconds","objective":"bm_final"},"color":"green","bold":true},{"text":" seconds","color":"white"}]

playsound minecraft:ui.toast.challenge_complete master @a ~ ~ ~ 1 1

# Notification
tellraw @a ["",{"text":"Round ","color":"green"},{"score":{"name":"#current","objective":"current_round"},"color":"yellow","bold":true},{"text":" Complete: ","color":"green"},{"score":{"name":"#total_seconds","objective":"bm_final"},"color":"green","bold":true},{"text":" seconds","color":"white"}]

# Advance to next round
scoreboard players add #current current_round 1
