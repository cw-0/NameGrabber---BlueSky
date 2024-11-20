import re


names = []

# Read names from the file
with open("handles.txt", "r") as file:
    for name in file:
        # Strip whitespace from left and right, then replace all spaces with a newline
        names.append(name.strip().replace(" ", "\n"))

names = [name for name in names if len(name) >= 3 ]


valid_names = []



for name in names:
    if re.match("^[a-zA-Z0-9-]+$", name):
        valid_names.append(name)
    else:
        print(f"{name} Removed")





with open("handles.txt", "w") as file:
    for name in valid_names:
        file.write(name + "\n")  # Write each name followed by a newline
