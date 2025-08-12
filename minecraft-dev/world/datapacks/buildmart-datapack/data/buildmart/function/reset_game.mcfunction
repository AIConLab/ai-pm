# file: reset_game.mcfunction
# Reset all rounds back to 0 and start over
scoreboard players set Round_1 round_times 0
scoreboard players set Round_2 round_times 0
scoreboard players set Round_3 round_times 0
scoreboard players set Round_4 round_times 0
scoreboard players set Round_5 round_times 0
scoreboard players set Round_6 round_times 0
scoreboard players set Round_7 round_times 0
scoreboard players set Round_8 round_times 0
scoreboard players set Round_9 round_times 0

# Reset to round 1
scoreboard players set #current current_round 1

# Stop any active round
scoreboard players set #round_active bm_status 0

tellraw @a ["",{"text":"[","color":"dark_gray"},{"text":"BUILD MART","color":"gold","bold":true},{"text":"] ","color":"dark_gray"},{"text":"Game Reset - Ready for Round 1","color":"green"}]