def render_horizontal_table(column_names, data_rows, max_column_length):
    column_lengths = []
    
    table_header_top_border = ""
    table_header_bottom_border = "|"
    table_footer = "|"
    table_column_format = "|"
    for column_name in column_names:
        name_lenght = len(column_name)
        if name_lenght <= max_column_length: 
            column_lengths.append(name_lenght)
        else:
            column_lengths.append(max_column_length)
    table_header_top_border += "\n"

    for index, value in enumerate(column_names):
        column_name_length = len(value)
        if column_name_length >= max_column_length:
            column_names[index] = value[:max_column_length-3] + "..."

    for row in data_rows:
        for index, value in enumerate(column_lengths):
            row_column_length = len(f"{row[index]}")
            if row_column_length >= max_column_length:
                row_column_length = max_column_length
                row[index] = row[index][:max_column_length-3] + "..."
            column_lengths[index] = (column_lengths[index] if column_lengths[index] >= row_column_length else row_column_length) + 1
    
    for column_length in column_lengths:
        table_column_format += " {:^" + f"{column_length}" + "} |"
        table_header_top_border += "_"*column_length
        table_header_bottom_border += "-"*(column_length+2) + "|" 
        table_footer += "_"*(column_length+2) + "|" 
    table_header_top_border += "___" * len(column_lengths)+"\n"
    table_column_format +="\n"
    table_header_bottom_border += "\n"
    table_footer += "\n"

    table_header = (table_column_format.format(*column_names))

    table_str = table_header_top_border
    table_str += table_header
    table_str += table_header_bottom_border
    for row in data_rows:
        table_str += (table_column_format.format(*row))
    table_str += table_footer
    return table_str

def render_vertical_table(row_names, data_column):
    header_column_length = 0
    data_column_length = 0
    data_rows = []

    for index, value in enumerate(row_names):
        name_column_len = len(value)
        data_column_len = len(str(data_column[index]))
        header_column_length = name_column_len if name_column_len > header_column_length else header_column_length
        data_column_length = data_column_len if data_column_len > data_column_length else data_column_length

    table_str = ""
    table_header_top_border = "_"*(header_column_length + 2) + "_" + "_"*(data_column_length + 2) + "_\n"
    table_str += table_header_top_border
        
    row_format = ("|" + " {:^" + f"{header_column_length}" + "} | {:^" + f"{data_column_length}" + "} |\n")
    for index, value in enumerate(row_names):
        table_str += row_format.format(*[f"{value}", f"{data_column[index]}"])

    table_footer = "|_"+ "_"*(header_column_length) + "_|_" + "_"*(data_column_length) + "_|\n"
    table_str += table_footer

    return table_str