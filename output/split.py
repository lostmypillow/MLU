input_file = "output.txt"

with open(input_file, 'r', encoding='utf-8') as input_f:
    above_lines = []  
    below_lines = [] 
    file_counter = 0

    for line in input_f:
        if line.startswith("0"):
            file_counter += 1
            file_name = f"{line[:5]}.txt"  # Use the first 5 characters as the filename
            
            below_lines = [line]
            

            with open(file_name, 'w', encoding='utf-8') as output_file:
                output_file.writelines(above_lines)

            above_lines = []
        else:
            above_lines.append(line)
            below_lines.append(line)

# Create the last output file (if there are any remaining lines)
if above_lines:
    file_counter += 1
    file_name = f"output_{file_counter}.txt"
    

    with open(file_name, 'w', encoding='utf-8') as output_file:
        output_file.writelines(above_lines)
        

    with open(file_name, 'a', encoding='utf-8') as output_file:
        output_file.writelines(below_lines)

print(f"Split into {file_counter} files named after the lines starting with '0', with '0' at the end of each file.")
