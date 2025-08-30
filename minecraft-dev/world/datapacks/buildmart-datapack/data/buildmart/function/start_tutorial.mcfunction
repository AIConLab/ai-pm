# file: start_tutorial.mcfunction
# Sets up and starts the tutorial round.

# Check if a round is already active to prevent overlap
execute if score #round_active bm_status matches 1 run tellraw @s {"text":"A round or tutorial is already active!","color":"red"}
execute if score #round_active bm_status matches 1 run return fail

# Set the specific round number to 10 for the tutorial
scoreboard players set #current current_round 10

# Set round as active and reset completion flag so the tutorial structure can be checked
scoreboard players set #round_active bm_status 1
scoreboard players set #already_complete bm_status 0

# Show tutorial-specific title
title @a times 5 60 20
title @a title {"text":"GO!","color":"green","bold":true}
title @a subtitle {"text":"Tutorial Round","color":"yellow","bold":true}

# Start sounds
playsound minecraft:entity.player.levelup master @a ~ ~ ~ 1 0.5
playsound minecraft:block.bell.use master @a ~ ~ ~ 1 1

# Notification that the tutorial has started
tellraw @a ["",{"text":"[","color":"dark_gray"},{"text":"BUILD MART","color":"gold","bold":true},{"text":"] ","color":"dark_gray"},{"text":"Tutorial Round Started!","color":"green"}]