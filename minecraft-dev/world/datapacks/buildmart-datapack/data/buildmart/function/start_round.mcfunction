# Start round
scoreboard players set active bm_active 1
scoreboard players set ticks bm_timer 0
scoreboard players set seconds bm_timer 0
scoreboard players set minutes bm_timer 0

# Reset structures
scoreboard players set s1_done bm_s1_done 0
scoreboard players set s2_done bm_s2_done 0
scoreboard players set s3_done bm_s3_done 0

# Reset display
scoreboard players set §aStructure_1§r bm_display 95
scoreboard players set §eStructure_2§r bm_display 90
scoreboard players set §cStructure_3§r bm_display 85

tellraw @a {"text":"Round Started!","color":"green","bold":true}
playsound minecraft:block.note_block.pling master @a ~ ~ ~ 1 2