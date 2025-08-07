# Only run if active
execute if score active bm_active matches 1 run scoreboard players add ticks bm_timer 1

# Convert ticks to seconds
execute if score active bm_active matches 1 if score ticks bm_timer matches 20.. run scoreboard players add seconds bm_timer 1
execute if score active bm_active matches 1 if score ticks bm_timer matches 20.. run scoreboard players set ticks bm_timer 0

# Convert seconds to minutes
execute if score active bm_active matches 1 if score seconds bm_timer matches 60.. run scoreboard players add minutes bm_timer 1
execute if score active bm_active matches 1 if score seconds bm_timer matches 60.. run scoreboard players set seconds bm_timer 0

# Update timer display
execute if score active bm_active matches 1 run scoreboard players operation §9Timer§r bm_display = seconds bm_timer
execute if score active bm_active matches 1 if score minutes bm_timer matches 1.. run scoreboard players operation §9Timer§r bm_display = minutes bm_timer

# Check structures
execute if score active bm_active matches 1 if score s1_done bm_s1_done matches 0 run function buildmart:check_structure1
```