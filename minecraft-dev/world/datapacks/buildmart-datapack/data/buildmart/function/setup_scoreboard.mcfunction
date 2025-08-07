# Remove old objectives
scoreboard objectives remove bm_timer
scoreboard objectives remove bm_active
scoreboard objectives remove bm_display
scoreboard objectives remove bm_s1_done
scoreboard objectives remove bm_s2_done
scoreboard objectives remove bm_s3_done

# Create objectives
scoreboard objectives add bm_timer dummy
scoreboard objectives add bm_active dummy
scoreboard objectives add bm_s1_done dummy
scoreboard objectives add bm_s2_done dummy
scoreboard objectives add bm_s3_done dummy

# Create display
scoreboard objectives add bm_display dummy "§6§lBUILD MART TIMER"
scoreboard objectives setdisplay sidebar bm_display

# Initialize
scoreboard players set active bm_active 0
scoreboard players set ticks bm_timer 0
scoreboard players set seconds bm_timer 0
scoreboard players set minutes bm_timer 0

# Display setup
scoreboard players set §9Timer§r bm_display 100
scoreboard players set §aStructure_1§r bm_display 95
scoreboard players set §eStructure_2§r bm_display 90
scoreboard players set §cStructure_3§r bm_display 85

# Structure completion flags
scoreboard players set s1_done bm_s1_done 0
scoreboard players set s2_done bm_s2_done 0
scoreboard players set s3_done bm_s3_done 0

tellraw @a {"text":"Build Mart Timer Initialized!","color":"green","bold":true}