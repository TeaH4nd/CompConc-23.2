def printDict(d):
    print()
    print()
    # Get unique file names
    file_names = sorted(set(file_name for files in d.values() for file_name in files))

    # Initialize max_widths with keys from the dictionary
    max_widths = {key: len(str(key)) for key in d.keys()}
    max_widths['Arquivos'] = max(len(max(file_names, key=len)), len('Arquivos'))  # Set the width of the first column

    # Find the maximum width for each column
    for file_name in file_names:
        max_widths[file_name] = max(
            max(len(str(file_data.get(file_name, ''))) for file_data in d.values()),
            len(file_name)  # Consider the length of the file name itself
        )

    # Calculate the length of the header
    header_length = len("| " + " | ".join(f"{column:<{max_widths[column]}}" for column in ['Arquivos'] + list(d.keys())) + " |")

    # Print top border
    top_border = "+" + "-" * (header_length - 2) + "+"
    print(top_border)

    # Print header
    header = "| " + " | ".join(f"{column:<{max_widths[column]}}" for column in ['Arquivos'] + list(d.keys())) + " |"
    print(header)

    # Print separator
    separator = "+" + "+".join("-" * (max_widths[column] + 2) for column in ['Arquivos'] + list(d.keys())) + "+"
    print(separator)

    # Print data rows
    for file_name in file_names:
        row = "| " + f"{file_name:<{max_widths['Arquivos']}}"
        for item in d.keys():
            row += f" | {str(d[item].get(file_name, '')):<{max_widths[item]}}"
        row += " |"
        print(row)

    # Print bottom border
    bottom_border = "+" + "-" * (header_length - 2) + "+"
    print(bottom_border)

    print()
    print()