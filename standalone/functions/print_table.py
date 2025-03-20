from standalone.global_vars import cursor

def print_table(table_query: str):
    """
    Enter the select query for the first argument. NO SEMICOLON SYMBOLS
    """

    # checks if table is empty
    query = cursor.execute(table_query)
    if len(list(query)) == 0:
        print("There's nothing to show.")

    query = cursor.execute(table_query)
    col_list = [desc[0] for desc in query.description] #removed the [:1] cuz it removes the emp_id and etc

    # get the max length of each column for proper printing
    col_ljust_vals = []
    for col in range(len(col_list)):
        query_to_perform = f'SELECT MAX(LENGTH("{col_list[col]}")) FROM ({table_query})'
        max_char_length = cursor.execute(query_to_perform).fetchone()[0]
        col_ljust_vals.append(
            max_char_length
            if (max_char_length if max_char_length != None else 0) > len(col_list[col])
            else len(col_list[col])
    )

    # create a horizontal line to separate the columns and rows
    print("_",end="")
    for i in range(len(col_list)):
        print(str("_")*(col_ljust_vals[i]+2)+"_", end="")
    print()

    # print the columns in the first row
    print("|",end="")
    for i in range(len(col_list)):
        print(
            str(col_list[i])
            .replace("_"," ")
            .ljust(col_ljust_vals[i]+2)
            .title()
            +"|"
            , end=""
        )
    print()

    # create a horizontal line to separate the columns and rows
    print("|",end="")
    for i in range(len(col_list)):
        print(str("_")*(col_ljust_vals[i]+2)+"|", end="")
    print()
    
    # print the rows properly now
    query = cursor.execute(table_query)
    for row in query:
        print("|",end="")
        for i in range(len(col_list)):
            print(
                str(row[i])
                .replace("_"," ")
                .ljust(col_ljust_vals[i]+2)
                .title()
                +"|"
                , end=""
            )
        print()
    
    # create a horizontal line to separate the columns and rows
    print("|",end="")
    for i in range(len(col_list)):
        print(str("_")*(col_ljust_vals[i]+2)+"|", end="")
    print()