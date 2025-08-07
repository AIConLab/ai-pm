# Stop the round
scoreboard players set #round round_active 0

# Calculate final time
scoreboard players operation #final_seconds timer_seconds = #timer timer
scoreboard players operation #final_seconds timer_seconds /= #20 timer
scoreboard players operation #final_minutes timer_minutes = #final_seconds timer_seconds
scoreboard players operation #final_minutes timer_minutes /= #60 timer
scoreboard players operation #final_seconds timer_seconds %= #60 timer

# Announce
title @a title {"text":"Round Complete!","color":"gold"}
execute if score #final_minutes timer_minutes matches 0 run title @a subtitle ["",{"text":"Time: ","color":"yellow"},{"score":{"name":"#final_seconds","objective":"timer_seconds"},"color":"white"},{"text":" seconds","color":"yellow"}]
execute unless score #final_minutes timer_minutes matches 0 run title @a subtitle ["",{"text":"Time: ","color":"yellow"},{"score":{"name":"#final_minutes","objective":"timer_minutes"},"color":"white"},{"text":"m ","color":"yellow"},{"score":{"name":"#final_seconds","objective":"timer_seconds"},"color":"white"},{"text":"s","color":"yellow"}]

playsound minecraft:ui.toast.challenge_complete master @a ~ ~ ~ 1 1

say §6[Build Mart] Round complete! All structures built.