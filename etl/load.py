from os import listdir
from os.path import isfile, join
import sqlite3

import pandas as pd

data_dir = "./data/clean"
data_files = sorted([join(data_dir, f) for f in listdir(data_dir) if isfile(join(data_dir, f))])

conn = sqlite3.connect('./db/realestate.db')

cursor = conn.cursor()
cursor.execute("DROP TABLE IF EXISTS building_permits")
conn.commit()

cursor.execute(
    """
    CREATE TABLE building_permits
    (
        id                                     INTEGER PRIMARY KEY,
        date                                   TEXT,
        csa                                    INTEGER,
        cbsa                                   INTEGER,
        name                                   VARCHAR(255),
        total                                  INTEGER,
        one_unit                               INTEGER,
        two_units                              INTEGER,
        three_and_four_units                   INTEGER,
        five_units_or_more                     INTEGER,
        num_of_structures_with_5_units_or_more INTEGER,
        monthly_coverage_percent               INTEGER
    ); 
    """
)
conn.commit()

for data_file in data_files:
    df = pd.read_csv(data_file, index_col=None)
    df.to_sql("building_permits", con=conn, if_exists="append", index=None)

conn.close()
