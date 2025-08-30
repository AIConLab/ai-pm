# file: timer.mcfunction
# Silent tick that runs every game tick from command block
# Call the appropriate structure check based on current round
execute if score #round_active bm_status matches 1 if score #current current_round matches 1 run function buildmart:check_structure_1
execute if score #round_active bm_status matches 1 if score #current current_round matches 2 run function buildmart:check_structure_2
execute if score #round_active bm_status matches 1 if score #current current_round matches 3 run function buildmart:check_structure_3
execute if score #round_active bm_status matches 1 if score #current current_round matches 4 run function buildmart:check_structure_4
execute if score #round_active bm_status matches 1 if score #current current_round matches 5 run function buildmart:check_structure_5
execute if score #round_active bm_status matches 1 if score #current current_round matches 6 run function buildmart:check_structure_6
execute if score #round_active bm_status matches 1 if score #current current_round matches 7 run function buildmart:check_structure_7
execute if score #round_active bm_status matches 1 if score #current current_round matches 8 run function buildmart:check_structure_8
execute if score #round_active bm_status matches 1 if score #current current_round matches 9 run function buildmart:check_structure_9
execute if score #round_active bm_status matches 1 if score #current current_round matches 10 run function buildmart:check_structure_10


# Update timer display in action bar
execute if score #round_active bm_status matches 1 store result score #elapsed bm_timer run time query gametime
execute if score #round_active bm_status matches 1 run scoreboard players operation #elapsed bm_timer -= #start_time bm_start
execute if score #round_active bm_status matches 1 run scoreboard players operation #elapsed_sec bm_timer = #elapsed bm_timer
execute if score #round_active bm_status matches 1 run scoreboard players operation #elapsed_sec bm_timer /= #20 bm_timer
execute if score #round_active bm_status matches 1 run title @a actionbar [{"text":"⏱ Round ","color":"yellow"},{"score":{"name":"#current","objective":"current_round"},"color":"white","bold":true},{"text":" - Time: ","color":"yellow"},{"score":{"name":"#elapsed_sec","objective":"bm_timer"},"color":"white","bold":true},{"text":"s","color":"yellow"}]
