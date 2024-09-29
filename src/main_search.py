import klayout.db as db

# Load your GDS file
layout = db.Layout()
gds_file_path = "C:/Users/32232/Documents/OEDS/OEDS/src/input/Full_layout_0720_V3.gds"
try:
    layout.read(gds_file_path)  # Replace with your GDS file path
    print(f"Successfully loaded GDS file: {gds_file_path}")
except Exception as e:
    print(f"Error loading GDS file: {e}")
    exit(1)

# Define the device name you're searching for
device_name = "BP_M1M2_80_60"  # Replace with the actual device name
device_found = False  # Flag to track if the device is found

def search_instances(cell):
    """Recursive function to search through all instances of a given cell."""
    global device_found
    for inst in cell.each_inst():
        cell_name = inst.cell.name
        print(f"Checking instance in cell '{cell.name}': {cell_name}")

        if cell_name == device_name:
            device_found = True
            # Get the bounding box of the instance
            bbox = inst.bbox()

            # Calculate position and size
            x_min = bbox.left
            y_min = bbox.bottom
            x_max = bbox.right
            y_max = bbox.top

            width = x_max - x_min
            height = y_max - y_min

            # Get the transformation (position) of the instance
            transformation = inst.trans

            print(f"Device '{device_name}' found at position: ({transformation.disp.x}, {transformation.disp.y})")
            print(f"Size: {width} x {height}")
            return  # Exit the search once the device is found

        # Recursively search in the instance's cell (subcells)
        search_instances(inst.cell)

# Start searching from the top cell
top_cell = layout.top_cell()
if top_cell:
    print(f"Top cell found: {top_cell.name}")
    search_instances(top_cell)
else:
    print("No top cell found in the layout. Exiting.")
    exit(1)

if not device_found:
    print(f"Device '{device_name}' not found in the layout.")
