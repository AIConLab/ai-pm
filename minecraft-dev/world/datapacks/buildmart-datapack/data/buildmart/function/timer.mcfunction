# file: timer.mcfunction
# Silent tick that runs every game tick from command block
execute if score #round_active bm_status matches 1 run function buildmart:check_structure_silent

# Update timer display in action bar
execute if score #round_active bm_status matches 1 store result score #elapsed bm_timer run time query gametime
execute if score #round_active bm_status matches 1 run scoreboard players operation #elapsed bm_timer -= #start_time bm_start
execute if score #round_active bm_status matches 1 run scoreboard players operation #elapsed_sec bm_timer = #elapsed bm_timer
execute if score #round_active bm_status matches 1 run scoreboard players operation #elapsed_sec bm_timer /= #20 bm_timer
execute if score #round_active bm_status matches 1 run title @a actionbar [{"text":"⏱ Round ","color":"yellow"},{"score":{"name":"#current","objective":"current_round"},"color":"white","bold":true},{"text":" - Time: ","color":"yellow"},{"score":{"name":"#elapsed_sec","objective":"bm_timer"},"color":"white","bold":true},{"text":"s","color":"yellow"}]
