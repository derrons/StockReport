import os
import sqlite3
from tqdm import tqdm

def create_table(db):
    #Remove existing database if present
    if os.path.exists(db):
        try:
            os.remove(db)
        except:
            print('Could not delete existing database')
            return False
    try:
        conn = sqlite3.connect(db)
    except Exception as e:
        print(f'Cannot connect to database {e}')
        return False
    #create table
    if conn:
        conn.execute("CREATE TABLE stocks (Symbol TEXT, Date TEXT, Open TEXT, High TEXT, Low TEXT, \
                     Close FLOAT, Volume INTEGER)")
        conn.commit()
        conn.close()
        return True


def insert_table(db,data):
    try:
        conn = sqlite3.connect(db)
    except Exception as e:
        print(f'Cannot connect to database {e}')
        return

    if conn:
        cursor = conn.cursor()
        #validate table is in database
        table_exists = cursor.execute("SELECT name FROM sqlite_master WHERE type='table' \
                                     AND name='stocks';").fetchall()
        if table_exists[0][0] != 'stocks':
            print('The stocks table cannot be found in database')
            return
        
        with tqdm(total=len(data), desc='Adding stock info to database', unit='Record') as pbar:
            for ind_date , row in data.iterrows():
                try:
                    cursor.execute("INSERT INTO stocks VALUES (?, ?, ?, ?, ?, ?, ?)", ( \
                                    row['Symbol'], ind_date.strftime('%Y-%m-%d'), row['Open'], \
                                    row['High'], row['Low'],row['Close'], \
                                    row['Volume']))
                    conn.commit()
                except Exception as e:
                    print('Error:  could not add data to database')
                    print (str(e))
                    print(ind_date, row)
                pbar.update()
        conn.close()
        
