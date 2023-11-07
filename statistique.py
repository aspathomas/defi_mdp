# Open the file for reading
with open('Ashley-Madison.txt', 'r') as file:
    line_number = 0

    # Iterate through each line in the file
    for line in file:
        line_number += 1
        # Count the number of characters in the line
        num_chars = len(line.strip())
        print(f"Line {line_number}: {num_chars} characters")

# Close the file
file.close()