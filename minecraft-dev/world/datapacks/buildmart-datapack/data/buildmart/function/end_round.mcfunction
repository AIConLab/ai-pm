#file: end_round.mcfunction
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

# === ENHANCED VISUAL END SEQUENCE ===

# Clear titles
title @a clear

# Time's up effect
title @a times 10 80 20
title @a title {"text":"TIME'S UP!","color":"red","bold":true}
title @a subtitle [{"text":"Completed in ","color":"yellow"},{"score":{"name":"#total_seconds","objective":"bm_final"},"color":"green","bold":true},{"text":" seconds","color":"yellow"}]

# Victory sounds
playsound minecraft:ui.toast.challenge_complete master @a ~ ~ ~ 1 1
playsound minecraft:entity.firework_rocket.blast master @a ~ ~ ~ 1 1
playsound minecraft:entity.player.levelup master @a ~ ~ ~ 1 1.5

# Particle celebration
execute at @a run particle minecraft:totem_of_undying ~ ~2 ~ 0 0 0 1 100
execute at @a run particle minecraft:firework ~ ~1 ~ 2 2 2 0.1 100

# Update team scoreboard
scoreboard players operation AI_Project_Manager teams = #total_seconds bm_final
scoreboard players operation Human_Project_Manager teams = #total_seconds bm_final  
scoreboard players operation No_Project_Manager teams = #total_seconds bm_final

# Single clean completion message
tellraw @a ""
tellraw @a ["",{"text":"▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬","color":"gold"}]
tellraw @a ["",{"text":"       BUILD MART RESULTS","color":"gold","bold":true}]
tellraw @a ["",{"text":"  Round Completed in: ","color":"white"},{"score":{"name":"#total_seconds","objective":"bm_final"},"color":"green","bold":true},{"text":" seconds","color":"white"}]
tellraw @a ["",{"text":"▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬","color":"gold"}]
tellraw @a ""