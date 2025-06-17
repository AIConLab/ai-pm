team add AIPM "AI Project Manager"
team add HumanPM "Human Project Manager"
team add NoPM "No Project Manager"
team add Admin "Admin Team"

team modify AIPM color blue
team modify AIPM friendlyFire false
team modify AIPM prefix "§9[AI-PM] §r"

team modify HumanPM color green
team modify HumanPM friendlyFire false
team modify HumanPM prefix "§a[Human-PM] §r"

team modify NoPM color red
team modify NoPM friendlyFire false
team modify NoPM prefix "§c[No-PM] §r"

team modify Admin color gold
team modify Admin friendlyFire false
team modify Admin prefix "§6[Admin] §r"

scoreboard objectives add teams dummy "Team Overview"
scoreboard objectives setdisplay sidebar teams
scoreboard players set "§9AI Project Manager" teams 0
scoreboard players set "§aHuman Project Manager" teams 0
scoreboard players set "§cNo Project Manager" teams 0
scoreboard players set "§6Admin Team" teams 0