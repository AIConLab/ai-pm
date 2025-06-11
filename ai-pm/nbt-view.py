import nbtlib
import sys

# Load an NBT file
nbt_file = nbtlib.load(sys.argv[1])
# Access data
data = nbt_file.root
