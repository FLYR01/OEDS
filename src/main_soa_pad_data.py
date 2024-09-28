import re

# Function to replace cell names sequentially
def rename_cells_sequentially(data):
    cell_counter = [1]  # Initialize a counter

    def replace_match(m):
        result = f"{m.group(1)}SOA_pad_{cell_counter[0]}{m.group(3)}"
        cell_counter[0] += 1
        return result

    # Regex pattern to find the "Cell Name"
    pattern = r"(Cell Name: )(PCELL_50)( \(Parent: None\))"
    
    # Replace each match with the sequentially incremented cell name
    renamed_data = re.sub(pattern, replace_match, data)
    return renamed_data

# Read the original data from the file
with open("src/output/summary_SOA_pad.txt", "r") as file:
    data = file.read()

# Apply the renaming function
renamed_data_sequential = rename_cells_sequentially(data)

# Write the renamed data into a new file
with open("src/output/renamed_summary_SOA_pad.txt", "w") as output_file:
    output_file.write(renamed_data_sequential)

print("Cell names have been successfully renamed and saved to renamed_summary.txt.")
