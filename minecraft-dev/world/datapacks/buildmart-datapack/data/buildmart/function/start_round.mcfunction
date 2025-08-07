# Start the round timer
execute if score #round_active bm_status matches 1 run tellraw @s {"text":"Round already active! Use /function buildmart:end_round first","color":"red"}
execute if score #round_active bm_status matches 1 run return fail

# Set round as active
scoreboard players set #round_active bm_status 1

# Record start time
execute store result score #start_time bm_start run time query gametime

# === ENHANCED VISUAL START SEQUENCE ===

# Clear any existing titles
title @a clear
title @a reset

# Countdown effect
title @a times 10 40 10

# "READY" message
title @a title {"text":"READY","color":"yellow","bold":true}
title @a subtitle {"text":"Prepare to build...","color":"gray"}
playsound minecraft:block.note_block.bit master @a ~ ~ ~ 1 0.5

# Wait 1 second (schedule next part)
schedule function buildmart:start_countdown_3 1s

# Show particles at spawn
execute at @a run particle minecraft:flame ~ ~1 ~ 0.5 0.5 0.5 0.01 20

title @a title {"text":"3","color":"red","bold":true}
title @a subtitle {"text":"Get ready...","color":"gray"}
playsound minecraft:block.note_block.bit master @a ~ ~ ~ 1 0.7
execute at @a run particle minecraft:smoke ~ ~1 ~ 0.5 0.5 0.5 0.01 10
schedule function buildmart:start_countdown_2 1s

title @a title {"text":"2","color":"gold","bold":true}
title @a subtitle {"text":"Get set...","color":"gray"}
playsound minecraft:block.note_block.bit master @a ~ ~ ~ 1 0.9
execute at @a run particle minecraft:smoke ~ ~1 ~ 0.5 0.5 0.5 0.01 10
schedule function buildmart:start_countdown_1 1s

title @a title {"text":"1","color":"yellow","bold":true}
title @a subtitle {"text":"Almost there...","color":"gray"}
playsound minecraft:block.note_block.bit master @a ~ ~ ~ 1 1.1
execute at @a run particle minecraft:smoke ~ ~1 ~ 0.5 0.5 0.5 0.01 10
schedule function buildmart:start_go 1s

# Big GO message
title @a times 5 60 20
title @a title {"text":"GO!","color":"green","bold":true,"underlined":true}
title @a subtitle {"text":"Build Structure 1!","color":"white"}

# Epic start sounds
playsound minecraft:entity.ender_dragon.growl master @a ~ ~ ~ 0.3 1.5
playsound minecraft:entity.player.levelup master @a ~ ~ ~ 1 0.5
playsound minecraft:block.bell.use master @a ~ ~ ~ 1 1

# Particle explosion
execute at @a run particle minecraft:firework ~ ~1 ~ 1 1 1 0.1 50
execute at @a run particle minecraft:happy_villager ~ ~1 ~ 1 1 1 0.1 30

# Action bar message
title @a actionbar {"text":"ROUND ACTIVE - BUILD NOW!","color":"green","bold":true}

# Single clean notification (no spam)
tellraw @a ["",{"text":"[","color":"dark_gray"},{"text":"BUILD MART","color":"gold","bold":true},{"text":"] ","color":"dark_gray"},{"text":"Round Started! ","color":"green"},{"text":"Timer is running!","color":"yellow"}]