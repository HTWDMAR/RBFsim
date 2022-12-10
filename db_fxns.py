import sqlite3
conn = sqlite3.connect("data.db", check_same_thread=False)
c = conn.cursor()


#Database
#Table
#Field/Columns
#DataType

def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS datatable(well_id INT, pump_rate INT, x_coo INT, y_coo INT)')

def add_data(well_id, pump_rate, x_coo, y_coo):
    c.execute('INSERT INTO datatable(well_id, pump_rate, x_coo, y_coo) VALUES (?,?,?,?)', (well_id, pump_rate, x_coo, y_coo))
    conn.commit()

def view_all_data():
    c.execute('SELECT * FROM datatable')
    data = c.fetchall()
    return data

def view_unique_data():
    c.execute('SELECT DISTINCT well_id FROM datatable')
    data = c.fetchall()
    return data

def get_id(well_id):
    c.execute('SELECT * FROM datatable WHERE well_id="{}"'.format(well_id))
    data = c.fetchall()
    return data

def edit_well_id(new_well_id, new_pump_rate, new_x_coo, new_y_coo, well_id, pump_rate, x_coo, y_coo):
    c.execute("UPDATE datatable SET well_id=?, pump_rate=?, x_coo=?, y_coo=? WHERE well_id=? and pump_rate=? and x_coo=? and y_coo=?", (new_well_id, new_pump_rate, new_x_coo, new_y_coo, well_id, pump_rate, x_coo, y_coo) )
    conn.commit()
    data = c.fetchall()
    return data

def delete_id(well_id):
    c.execute('DELETE FROM datatable WHERE well_id="{}"'.format(well_id))
    conn.commit()


#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

