from standalone.global_vars import cursor

def exist_check(table, table_column, data):  #checks if one data exists in a table, usually if supplier_id is in table or if employee_id in table
    query = f"SELECT COUNT(*) FROM {table} WHERE {table_column} = ?"
    cursor.execute(query, (data,))
    return 1 if cursor.fetchone()[0] else 0