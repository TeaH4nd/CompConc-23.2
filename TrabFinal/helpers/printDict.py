d = {'Concorrente': {'fileAaa': 1.43244324, 'fileBb': 13, 'fileCcccc': 323}, 'Sequencial': {'fileAaa': 3, 'fileBb': 132, 'fileC': 10}}

def printDict(d):
    # Get unique file names
    file_names = sorted(set(file_name for files in d.values() for file_name in files))

    # Find the maximum width for each column
    max_widths = {'Item': max(len(item) for item in d)}
    for file_name in file_names:
        max_widths[file_name] = max(
            max(len(str(file_data.get(file_name, ''))) for file_data in d.values()),
            len(file_name)  # Consider the length of the file name itself
        )

    # Calculate total width of the table
    table_width = sum(max_widths.values()) + len(max_widths) * 3 + 1  # 3 accounts for the spaces and separators between columns

    # Print top border
    top_border = "+" + "-" * (table_width - 2) + "+"
    print(top_border)

    # Print header
    header = "| " + " | ".join(f"{column:<{max_widths[column]}}" for column in ['Item'] + file_names) + " |"
    print(header)

    # Print separator
    separator = "+-" + "-+-".join("-" * (max_widths[column]) for column in ['Item'] + file_names) + "-+"
    print(separator)

    # Print data rows
    for item in d.keys():
        row = "| " + f"{item:<{max_widths['Item']}}"
        for file_name in file_names:
            row += f" | {str(d[item].get(file_name, '')):<{max_widths[file_name]}}"
        row += " |"
        print(row)

    # Print bottom border
    bottom_border = "+" + "-" * (table_width - 2) + "+"
    print(bottom_border)

printDict(d)