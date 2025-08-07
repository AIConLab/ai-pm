# ===========================================
# File: data/buildmart/function/setup_clean.mcfunction
# ===========================================

# Recreate your original team setup
team add AIPM "AI Project Manager"
team add HumanPM "Human Project Manager"
team add NoPM "No Project Manager"
team add Admin "Admin Team"
team modify AIPM color blue
team modify AIPM friendlyFire false
team modify AIPM prefix "[AI-PM] "
team modify HumanPM color green
team modify HumanPM friendlyFire false
team modify HumanPM prefix "[Human-PM] "
team modify NoPM color red
team modify NoPM friendlyFire false
team modify NoPM prefix "[No-PM] "
team modify Admin color gold
team modify Admin friendlyFire false
team modify Admin prefix "[Admin] "

# Recreate your original scoreboard
scoreboard objectives add teams dummy "Team Overview"
scoreboard objectives setdisplay sidebar teams
scoreboard players set AI_Project_Manager teams 0
scoreboard players set Human_Project_Manager teams 0
scoreboard players set No_Project_Manager teams 0
scoreboard players set Admin_Team teams 0

# Add Build Mart scoreboards
scoreboard objectives add bm_timer dummy "Build Timer"
scoreboard objectives add bm_status dummy "Round Status" 
scoreboard objectives add bm_start dummy "Start Time"
scoreboard objectives add bm_end dummy "End Time"
scoreboard objectives add bm_final dummy "Final Time"

# Initialize values
scoreboard players set #20 bm_timer 20
scoreboard players set #round_active bm_status 0
scoreboard players set #total_required bm_timer 50

say [BUILD MART] Clean system initialized successfully!
say [BUILD MART] Teams and scoreboard recreated
say [BUILD MART] Round status: INACTIVE
say [BUILD MART] Ready to use /function buildmart:start_round
