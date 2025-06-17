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
scoreboard objectives add teams dummy "Team Overview"
scoreboard objectives setdisplay sidebar teams
scoreboard players set AI_Project_Manager teams 0
scoreboard players set Human_Project_Manager teams 0
scoreboard players set No_Project_Manager teams 0
scoreboard players set Admin_Team teams 0