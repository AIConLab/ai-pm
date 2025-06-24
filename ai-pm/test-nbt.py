#!/usr/bin/env python3
import nbtlib
from pathlib import Path
import json

# Quick and dirty NBT test
playerdata = Path("/mc-data/world/playerdata")
player_files = list(playerdata.glob("*.dat"))

if player_files:
    print(f"Found {len(player_files)} player files:")
    
    # Show all player files and names
    for i, pf in enumerate(player_files):
        try:
            temp_data = nbtlib.load(pf)
            name = "Unknown"
            if 'bukkit' in temp_data and 'lastKnownName' in temp_data['bukkit']:
                name = str(temp_data['bukkit']['lastKnownName'])
            print(f"  {i}: {pf.name} -> {name}")
        except:
            print(f"  {i}: {pf.name} -> (error reading)")
    
    # Read first player
    nbt_data = nbtlib.load(player_files[0])
    
    player_name = "Unknown"
    if 'bukkit' in nbt_data and 'lastKnownName' in nbt_data['bukkit']:
        player_name = str(nbt_data['bukkit']['lastKnownName'])
    print(f"\nAnalyzing player: {player_name}")
    
    # Show inventory items
    inventory = nbt_data.get('Inventory', [])
    print(f"Player has {len(inventory)} items")
    
    for item in inventory[:3]:  # Just first 3 items
        slot = int(item.get('Slot', -1))
        item_id = str(item.get('id', 'unknown'))
        count = int(item.get('count', 0))
        print(f"Slot {slot}: {item_id} x{count}")
    
    # Show sample JSON structure
    print("\nSample inventory item:")
    if inventory:
        print(json.dumps(dict(inventory[0]), indent=2, default=str))
    
    print("\nPlayer info keys:")
    for key in sorted(nbt_data.keys())[:10]:  # First 10 keys
        print(f"  {key}: {type(nbt_data[key]).__name__}")
else:
    print("No player data found - have players joined the server?")