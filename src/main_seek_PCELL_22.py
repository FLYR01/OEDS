import klayout.db as db

# Load your GDS file
layout = db.Layout()
gds_file_path = "src/input/Full_layout_0720_V3.gds"
output_file_path = "src/output/results_PCELL_22_labels.txt"  # Output file for detailed results
summary_file_path = "src/output/summary_PCELL_22_labels.txt"  # Output file for summary only

try:
    layout.read(gds_file_path)  # Replace with your GDS file path
    print(f"Successfully loaded GDS file: {gds_file_path}")
except Exception as e:
    print(f"Error loading GDS file: {e}")
    exit(1)

# Define the device name and target parent cell you're searching for
device_name = "BP_M1M2_80_60"  # Replace with the actual device name
target_parent_cell_name = "PCELL_22"  # The parent cell you want to search under
device_instances = []  # List to store the position and size of each found device
total_cells_checked = 0  # Counter for the number of cells checked
max_depth = 0  # Variable to track the maximum search depth

# Open files to write the results
with open(output_file_path, "w") as output_file, open(summary_file_path, "w") as summary_file:
    
    output_file.write(f"Search results for GDS file: {gds_file_path}\n\n")

    def search_instances(cell, parent_cell_name, parent_transformation=db.Trans(), depth=0):
        """Recursive function to search through all instances of a given cell."""
        global total_cells_checked, max_depth
        indent = "  " * depth  # Indentation for subcell depth visualization
        total_cells_checked += 1  # Increment cell counter
        max_depth = max(max_depth, depth)  # Update maximum depth

        print(f"{indent}Entering cell: {cell.name} (Parent: {parent_cell_name})")
        output_file.write(f"{indent}Entering cell: {cell.name} (Parent: {parent_cell_name})\n")
        
        for inst in cell.each_inst():
            cell_name = inst.cell.name
            print(f"{indent}Checking instance: {cell_name} in cell '{cell.name}' (Parent: {parent_cell_name})")
            output_file.write(f"{indent}Checking instance: {cell_name} in cell '{cell.name}' (Parent: {parent_cell_name})\n")

            # Accumulate transformations by combining parent and current instance transformations
            current_transformation = parent_transformation * inst.trans

            # Check if the current instance's cell name matches the target device name and is within the PCELL24 hierarchy
            if cell_name == device_name and target_parent_cell_name in parent_cell_name:
                # Get the bounding box of the instance
                bbox = inst.bbox()

                # Calculate size
                width = bbox.width()
                height = bbox.height()

                # Get the transformation (position) relative to the top cell
                top_position_x = current_transformation.disp.x
                top_position_y = current_transformation.disp.y

                # Store the instance details including the parent cell name
                device_instances.append({
                    "cell_name": cell.name,
                    "parent_cell_name": parent_cell_name,
                    "position": (top_position_x, top_position_y),
                    "size": (width, height)
                })

                result_str = (f"\n{indent}Device '{device_name}' found in cell '{cell.name}' (Parent: {parent_cell_name})!\n"
                              f"{indent}Position in top cell: ({top_position_x}, {top_position_y})\n"
                              f"{indent}Size: {width} x {height}\n")
                
                print(result_str)
                output_file.write(result_str)

            # Recursively search in the instance's cell (subcells), passing the current cell name as the parent
            search_instances(inst.cell, cell.name, current_transformation, depth + 1)

        print(f"{indent}Finished checking cell: {cell.name} (Parent: {parent_cell_name})")
        output_file.write(f"{indent}Finished checking cell: {cell.name} (Parent: {parent_cell_name})\n")

    # Start searching from the top cell
    top_cell = layout.top_cell()
    if top_cell:
        print(f"Top cell found: {top_cell.name}")
        output_file.write(f"Top cell found: {top_cell.name}\n\n")
        search_instances(top_cell, "None")  # No parent for the top cell
    else:
        print("No top cell found in the layout. Exiting.")
        output_file.write("No top cell found in the layout. Exiting.\n")
        exit(1)

    # Generate a summary of all found instances
    summary = f"\nSummary of Found '{device_name}' Devices under '{target_parent_cell_name}':\n"
    if device_instances:
        for i, device in enumerate(device_instances, 1):
            label = "Ring heater"  # Default label
            if (i - 1) % 13 == 0 and (i - 1) // 13 <= 63:  # (1 + N * 13)-th instance
                label = "No connection"
            elif (i - 2) % 13 == 0 and (i - 2) // 13 <= 63:  # (2 + N * 13)-th instance
                label = "No connection"
            elif (i - 9) % 13 == 0 and (i - 9) // 13 <= 63:  # (9 + N * 13)-th instance
                label = "GND"
            elif (i - 7) % 13 == 0 and (i - 7) // 13 <= 63:  # (7 + N * 13)-th instance
                label = "Thermal phase shifter"
            elif (i - 8) % 13 == 0 and (i - 8) // 13 <= 63:  # (8 + N * 13)-th instance
                label = "Thermal phase shifter"
            
            summary += (f"Device Instance {i} [{label}]:\n"
                        f"  Cell Name: {device['cell_name']}_{i} (Parent: {device['parent_cell_name']})\n"
                        f"  Position in Top Cell: {device['position']}\n"
                        f"  Size: {device['size'][0]} x {device['size'][1]}\n")
    else:
        summary += f"No instances of device '{device_name}' were found under parent cell '{target_parent_cell_name}'.\n"

    summary += f"\nTotal cells checked: {total_cells_checked}\n"
    summary += f"Maximum search depth: {max_depth}\n"

    # Print and write the summary to both the detailed file and summary file
    print(summary)
    output_file.write(summary)
    summary_file.write(summary)
