import string

# Generate combinations and append to a list
combinations = []
for char1 in string.ascii_lowercase:
    for char2 in string.ascii_lowercase:
        combination = f"{char1}-{char2}"
        combinations.append(combination)

# Sort the list alphabetically
combinations.sort()

# Write the sorted list to a txt file
file_name = "combinations.txt"
with open(file_name, "w") as file:
    for combo in combinations:
        file.write(combo + "\n")

print(f"Combinations saved to {file_name}")
