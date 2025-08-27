# file: structure_3_done.mcfunction
# Structure 3 is complete!
# Mark as complete FIRST to prevent re-triggering
scoreboard players set #already_complete bm_status 1

# Clear previous titles
title @a clear

# Big success message
title @a times 10 60 20
title @a title {"text":"✓ STRUCTURE COMPLETE!","color":"green","bold":true}
title @a subtitle {"text":"Perfect build detected!","color":"yellow"}

# Success sounds
playsound minecraft:ui.toast.challenge_complete master @a ~ ~ ~ 1 1
playsound minecraft:entity.player.levelup master @a ~ ~ ~ 1 1.2
playsound minecraft:block.bell.resonate master @a ~ ~ ~ 1 1

# Celebration particles at command block location
particle minecraft:totem_of_undying ~ ~3 ~ 0 0 0 0.5 50
particle minecraft:happy_villager ~ ~2 ~ 1 1 1 0.1 100
particle minecraft:firework ~ ~4 ~ 2 2 2 0.1 50

# Announce and end round
tellraw @a ["",{"text":"[","color":"dark_gray"},{"text":"BUILD MART","color":"gold","bold":true},{"text":"] ","color":"dark_gray"},{"text":"Structure 3 validated! ","color":"green"},{"text":"Ending round...","color":"yellow"}]

# End round immediately (no schedule needed)
function buildmart:end_round