scoreboard objectives add bm_timer dummy "Build Timer"
scoreboard objectives add bm_status dummy "Round Status" 
scoreboard objectives add bm_start dummy "Start Time"
scoreboard objectives add bm_end dummy "End Time"
scoreboard objectives add bm_final dummy "Final Time"

# Set constants
scoreboard players set #20 bm_timer 20
scoreboard players set #round_active bm_status 0

say [BUILD MART] Simple system initialized
say Use: /function buildmart:start_round to begin
say Use: /function buildmart:check_structure from command block under build area