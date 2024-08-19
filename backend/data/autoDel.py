import sqlite3

def deleteRow(id):
    conn = sqlite3.connect('data\\map_scan.db')
    cursor = conn.cursor()

    try:
        cursor.execute('DELETE FROM scan_info WHERE id=?',(id, ))
        cursor.execute('DELETE FROM host WHERE scan_info_id=?',(id, ))
        cursor.execute('DELETE FROM port WHERE host_id=?',(id, ))
        cursor.execute('DELETE FROM script WHERE host_id=?',(id, ))

        conn.commit()
    except sqlite3.Error as e:
        print(e)
        conn.rollback()

def main(latestdbID):
    deleteRow(latestdbID)