import json
from db import get_db_conn

URL_LIST_FILE = './data/links.json'
URL_DETAIL_FILE = './data/data.json'

def insert_to_pg():
    q = '''
    CREATE TABLE IF NOT EXISTS events (
        url TEXT PRIMARY KEY,
        title TEXT,
        date TIMESTAMP WITH TIME ZONE,
        venue TEXT,
        category TEXT,
        location TEXT
    );
    '''
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute(q)
    
    urls = json.load(open(URL_LIST_FILE, 'r'))
    data = json.load(open(URL_DETAIL_FILE, 'r'))
    for url, row in zip(urls, data):
        q = '''
        INSERT INTO events (url, title, date, venue, category, location)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (url) DO NOTHING;
        '''
        cur.execute(q, (url, row['title'], row['date'], row['venue'], row['category'], row['location']))
     
    print("Database creation and data insertion completed successfully.")
if __name__ == '__main__':
    insert_to_pg()
