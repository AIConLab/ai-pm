# file: structure_10_done.mcfunction
# Structure 10 (Tutorial) is complete!

# Mark as complete FIRST to prevent re-triggering
scoreboard players set #already_complete bm_status 1

# Clear previous titles
title @a clear

# Big success message
title @a times 10 60 20
title @a title {"text":"✓ TUTORIAL COMPLETE!","color":"green","bold":true}
title @a subtitle {"text":"Great job! Let's move on.","color":"yellow"}

# Success sounds
playsound minecraft:ui.toast.challenge_complete master @a ~ ~ ~ 1 1
playsound minecraft:entity.player.levelup master @a ~ ~ ~ 1 1.2

# Celebration particles at command block location
particle minecraft:totem_of_undying ~ ~3 ~ 0 0 0 0.5 50
particle minecraft:happy_villager ~ ~2 ~ 1 1 1 0.1 100

# Announce and teleport
tellraw @a ["",{"text":"[","color":"dark_gray"},{"text":"BUILD MART","color":"gold","bold":true},{"text":"] ","color":"dark_gray"},{"text":"Tutorial structure validated! ","color":"green"},{"text":"Teleporting to the next area...","color":"yellow"}]

# Teleport all players to the break area
tp @a -55.39 65 96.847