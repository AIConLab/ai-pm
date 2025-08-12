# file: setup_scoreboard.mcfunction
# Create round-based scoreboard system
scoreboard objectives add round_times dummy "Round Completion Times (seconds)"
scoreboard objectives add current_round dummy "Current Round"
scoreboard objectives setdisplay sidebar round_times

# Initialize all rounds to 0 (not completed yet)
scoreboard players set Round_1 round_times 0
scoreboard players set Round_2 round_times 0
scoreboard players set Round_3 round_times 0
scoreboard players set Round_4 round_times 0
scoreboard players set Round_5 round_times 0
scoreboard players set Round_6 round_times 0
scoreboard players set Round_7 round_times 0
scoreboard players set Round_8 round_times 0
scoreboard players set Round_9 round_times 0

# Set starting round to 1
scoreboard players set #current current_round 1

# Timer scoreboards for calculations
scoreboard objectives add bm_timer dummy "Build Timer"
scoreboard objectives add bm_status dummy "Round Status" 
scoreboard objectives add bm_start dummy "Start Time"
scoreboard objectives add bm_end dummy "End Time"
scoreboard objectives add bm_final dummy "Final Time"

# Initialize values
scoreboard players set #20 bm_timer 20
scoreboard players set #round_active bm_status 0

# Setup confirmation
tellraw @a ["",{"text":"[","color":"dark_gray"},{"text":"BUILD MART","color":"gold","bold":true},{"text":"] ","color":"dark_gray"},{"text":"Scoreboard Ready - Round 1","color":"green"}]
playsound minecraft:block.note_block.pling master @a ~ ~ ~ 0.5 2