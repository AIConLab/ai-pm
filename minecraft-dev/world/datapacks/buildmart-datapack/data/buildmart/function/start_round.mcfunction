# file: start_round.mcfunction

# Start the round timer
execute if score #round_active bm_status matches 1 run tellraw @s {"text":"Round already active! Use /function buildmart:end_round first","color":"red"}
execute if score #round_active bm_status matches 1 run return fail

# Set round as active
scoreboard players set #round_active bm_status 1

# Reset completion flag
scoreboard players set #already_complete bm_status 0

# Record start time
execute store result score #start_time bm_start run time query gametime

# Clear any existing titles
title @a clear
title @a reset

# Big GO message immediately
title @a times 5 60 20
title @a title {"text":"GO!","color":"green","bold":true,"underlined":true}
title @a subtitle {"text":"Build Structure 1!","color":"white"}

# Start sounds
playsound minecraft:entity.ender_dragon.growl master @a ~ ~ ~ 0.3 1.5
playsound minecraft:entity.player.levelup master @a ~ ~ ~ 1 0.5
playsound minecraft:block.bell.use master @a ~ ~ ~ 1 1

# Particle explosion
execute at @a run particle minecraft:firework ~ ~1 ~ 1 1 1 0.1 50
execute at @a run particle minecraft:happy_villager ~ ~1 ~ 1 1 1 0.1 30

# Notification
tellraw @a ["",{"text":"[","color":"dark_gray"},{"text":"BUILD MART","color":"gold","bold":true},{"text":"] ","color":"dark_gray"},{"text":"Round Started! ","color":"green"},{"text":"Timer is running!","color":"yellow"}]
