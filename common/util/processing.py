import sqlite3

import pandas as pd

from database import DATABASE_PATH

if __name__ == '__main__':
    query = 'SELECT * FROM Email;'

    conn = sqlite3.connect(DATABASE_PATH)
    with conn:
        df = pd.read_sql(sql=query, con=conn, index_col='id')

    print(df.iloc[1]['content'])