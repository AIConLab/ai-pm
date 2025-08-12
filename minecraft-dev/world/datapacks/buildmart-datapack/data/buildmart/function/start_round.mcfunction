# file: start_round.mcfunction
# Check if round is already active
execute if score #round_active bm_status matches 1 run tellraw @s {"text":"Round already active!","color":"red"}
execute if score #round_active bm_status matches 1 run return fail

# Check if all rounds completed
execute if score #current current_round matches 10.. run tellraw @s {"text":"All 9 rounds completed!","color":"gold"}
execute if score #current current_round matches 10.. run return fail

# Set round as active
scoreboard players set #round_active bm_status 1

# Record start time
execute store result score #start_time bm_start run time query gametime

# Show current round in title
title @a times 5 60 20
title @a title {"text":"GO!","color":"green","bold":true}
title @a subtitle [{"text":"Round ","color":"white"},{"score":{"name":"#current","objective":"current_round"},"color":"yellow","bold":true}]

# Start sounds
playsound minecraft:entity.player.levelup master @a ~ ~ ~ 1 0.5
playsound minecraft:block.bell.use master @a ~ ~ ~ 1 1

# Notification
tellraw @a ["",{"text":"[","color":"dark_gray"},{"text":"BUILD MART","color":"gold","bold":true},{"text":"] ","color":"dark_gray"},{"text":"Round ","color":"green"},{"score":{"name":"#current","objective":"current_round"},"color":"yellow","bold":true},{"text":" Started!","color":"green"}]
