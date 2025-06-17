team add AIPM "AI Project Manager"
team add HumanPM "Human Project Manager"
team add NoPM "No Project Manager"
team add Admin "Admin Team"
team modify AIPM color blue
team modify AIPM friendlyFire false
team modify AIPM prefix {"text":"[AI-PM] ","color":"blue"}
team modify HumanPM color green
team modify HumanPM friendlyFire false
team modify HumanPM prefix {"text":"[Human-PM] ","color":"green"}
team modify NoPM color red
team modify NoPM friendlyFire false
team modify NoPM prefix {"text":"[No-PM] ","color":"red"}
team modify Admin color gold
team modify Admin friendlyFire false
team modify Admin prefix {"text":"[Admin] ","color":"gold"}
scoreboard objectives add teams dummy "Team Overview"
scoreboard objectives setdisplay sidebar teams
scoreboard players set "AI Project Manager" teams 0
scoreboard players set "Human Project Manager" teams 0
scoreboard players set "No Project Manager" teams 0
scoreboard players set "Admin Team" teams 0