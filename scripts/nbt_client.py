# file: nbt_client.py
# desc: read nbt files

import nbtlib
from typing import Dict, List, Any, Optional
import os
from collections import Counter

class SchematicReader:
    """
    Simple reader for Sponge Schematic (.schem) files using nbtlib
    """
    
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.schematic_data = None
    
    def load(self) -> Dict[str, Any]:
        """Load and parse the schematic file"""
        with open(self.filepath, 'rb') as f:
            nbt_file = nbtlib.load(f, gzipped=True)
        
        # Extract schematic data from root["Schematic"]
        self.schematic_data = dict(nbt_file["Schematic"])
        return self.schematic_data
    
    def get_info(self) -> Dict[str, Any]:
        """Get basic information about the schematic"""
        return {
            'version': int(self.schematic_data['Version']),
            'data_version': int(self.schematic_data['DataVersion']),
            'width': int(self.schematic_data['Width']),
            'height': int(self.schematic_data['Height']),
            'length': int(self.schematic_data['Length']),
            'offset': list(self.schematic_data.get('Offset', [0, 0, 0]))
        }
    
    def get_block_palette(self) -> Dict[str, int]:
        """Get the block palette mapping block states to indices"""
        palette = self.schematic_data['Blocks']['Palette']
        return {str(block): int(index) for block, index in palette.items()}
    
    def get_block_data(self) -> List[int]:
        """Get the block data array (decoded from varint)"""
        raw_data = self.schematic_data['Blocks']['Data']
        return self._decode_varint_array(list(raw_data))
    
    def get_block_at_position(self, x: int, y: int, z: int) -> Optional[str]:
        """Get the block state at a specific position"""
        info = self.get_info()
        width, height, length = info['width'], info['height'], info['length']
        
        if not (0 <= x < width and 0 <= y < height and 0 <= z < length):
            return None
        
        # Calculate index: x + z * Width + y * Width * Length
        index = x + z * width + y * width * length
        
        block_data = self.get_block_data()
        palette_index = block_data[index]
        
        # Find block state by palette index
        palette = self.get_block_palette()
        for block_state, idx in palette.items():
            if idx == palette_index:
                return block_state
        
        return None
    
    def get_block_entities(self) -> List[Dict[str, Any]]:
        """Get all block entities in the schematic"""
        block_entities = self.schematic_data['Blocks'].get('BlockEntities', [])
        result = []
        
        for be in block_entities:
            entity = {
                'position': list(be['Pos']),
                'id': str(be['Id']),
                'data': dict(be.get('Data', {}))
            }
            result.append(entity)
        
        return result
    
    def get_entities(self) -> List[Dict[str, Any]]:
        """Get all entities in the schematic"""
        entities = self.schematic_data.get('Entities', [])
        result = []
        
        for entity in entities:
            entity_data = {
                'position': list(entity['Pos']),
                'id': str(entity['Id']),
                'data': dict(entity.get('Data', {}))
            }
            result.append(entity_data)
        
        return result
    
    def _decode_varint_array(self, byte_array: List[int]) -> List[int]:
        """Decode varint array from bytes"""
        result = []
        pos = 0
        
        while pos < len(byte_array):
            value = 0
            shift = 0
            
            while True:
                if pos >= len(byte_array):
                    break
                
                byte = byte_array[pos]
                pos += 1
                
                value |= (byte & 0x7F) << shift
                
                if (byte & 0x80) == 0:
                    break
                
                shift += 7
            
            result.append(value)
        
        return result

def main():
    """Main function to read and analyze the schematic"""
    
    # Hardcoded schematic file path
    schematic_file = "/mc-data/plugins/WorldEdit/schematics/12_eq.schem"
    
    # Load the schematic
    reader = SchematicReader(schematic_file)
    schematic_data = reader.load()
    
    # Get basic info
    info = reader.get_info()
    
    print("=== SCHEMATIC INFO ===")
    print(f"Version: {info['version']}")
    print(f"Data Version: {info['data_version']}")
    print(f"Dimensions: {info['width']} x {info['height']} x {info['length']}")
    print(f"Offset: {info['offset']}")
    
    # Get block information
    palette = reader.get_block_palette()
    block_data = reader.get_block_data()
    
    print(f"\n=== BLOCKS ===")
    print(f"Unique block types: {len(palette)}")
    print(f"Total blocks: {len(block_data)}")
    
    # Show block palette
    print("\nBlock Palette:")
    for block, index in sorted(palette.items(), key=lambda x: x[1]):
        print(f"  {index}: {block}")
    
    # Count blocks of each type
    index_to_block = {v: k for k, v in palette.items()}
    block_names = [index_to_block[idx] for idx in block_data]
    block_counts = Counter(block_names)
    
    print(f"\nMost common blocks:")
    for block, count in block_counts.most_common():
        print(f"  {block}: {count}")
    
    # Sample some blocks
    print(f"\n=== SAMPLE BLOCKS ===")
    for y in range(min(2, info['height'])):
        for z in range(min(3, info['length'])):
            for x in range(min(3, info['width'])):
                block = reader.get_block_at_position(x, y, z)
                if block and block != 'minecraft:air':
                    print(f"  Block at ({x}, {y}, {z}): {block}")
    
    # Block entities and regular entities
    block_entities = reader.get_block_entities()
    entities = reader.get_entities()
    
    if block_entities:
        print(f"\n=== BLOCK ENTITIES ===")
        for be in block_entities:
            print(f"  {be['id']} at {be['position']}")
    
    if entities:
        print(f"\n=== ENTITIES ===")
        for entity in entities:
            print(f"  {entity['id']} at {entity['position']}")

if __name__ == "__main__":
    main()