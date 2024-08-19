import sqlite3

#convert tuple [135] to dict with key and values {"portid": "135"}
def dictConvert(rows, cursor):
    columns = [description[0] for description in cursor.description]
    dictresult = [dict(zip(columns, row)) for row in rows]
    return dictresult

def row_delete(id):
    conn = sqlite3.connect('data\\map_scan.db')
    cursor = conn.cursor()

    try:
        for i in id:
            cursor.execute('select id from scan_info where id=?', (i, ))
            row = cursor.fetchone()
            if row is None:
                return "Failed"
            else:
                for i in id:
                    print(i)
                    cursor.execute('DELETE FROM scan_info WHERE id=?', (i, ))
                    cursor.execute('DELETE FROM host WHERE scan_info_id=?', (i, ))
                    cursor.execute('DELETE FROM port WHERE host_id=?', (i, ))
                    cursor.execute('DELETE FROM script WHERE host_id=?', (i, ))
                    conn.commit()
                return "Success"
    except sqlite3.Error as e:
        conn.rollback()
        print(e)
        return "Failed"

def history_table_display():
    conn = sqlite3.connect('data\\map_scan.db')
    cursor = conn.cursor()
    cursor.execute('''
                    SELECT scan_info.*, host.addr
                    FROM scan_info
                    JOIN host ON scan_info.id = host.scan_info_id
                    ''')
    rows = cursor.fetchall()
    return dictConvert(rows, cursor)

def provideData(scan_id, port_number = []):
    conn = sqlite3.connect('data\\map_scan.db')
    cursor = conn.cursor()
    get_scan_info_id(scan_id)
    #scan_info
    cursor.execute('''
                    SELECT * 
                    FROM scan_info
                    JOIN host ON scan_info.id = host.scan_info_id
                    WHERE scan_info.id = ?
                    ''', (scan_id, ))
    rows = cursor.fetchall()
    dbinforesult = dictConvert(rows, cursor)

    # #script table
    cursor.execute('''
                    SELECT script.*
                    FROM scan_info
                    JOIN host ON scan_info.id = host.scan_info_id
                    JOIN port ON host.id = port.host_id
                    JOIN script ON port.id = script.port_id
                    WHERE scan_info.id = ?
                ''', (scan_id, ))
    rowscript = cursor.fetchall()
    dbscriptresult = dictConvert(rowscript, cursor)

    #port table
    cursor.execute('''
                        SELECT port.*
                        FROM scan_info
                        JOIN host ON scan_info.id = host.scan_info_id
                        JOIN port ON host.id = port.host_id
                        WHERE scan_info.id = ?
                       ''', (scan_id, ))
    rowstest = cursor.fetchall()

    if len(port_number) > 0:
        dbportresult = dictConvert(rowstest, cursor)
        for i in range(len(port_number)):
            dbportresult.append({
             "portid": port_number[i],
             "state": "closed",
             "service_name": "Unknown"
        })
        port_number.clear()
        return [dbinforesult,dbportresult, dbscriptresult]
    else:
        dbportresult = dictConvert(rowstest, cursor)
        return [dbinforesult,dbportresult, dbscriptresult]
    
    


def get_scan_info_id(scan_id):
    conn = sqlite3.connect('data/map_scan.db')
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM scan_info ORDER BY id DESC LIMIT 1;')
        row = cursor.fetchone()
        if row is None:
            print("did not return row")
        else:
            dblastid = row[0]
            print(f"functon id {dblastid} >> lastrowid {scan_id}")
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        print("error")
    finally:
        conn.close()

def main():
    return history_table_display()
