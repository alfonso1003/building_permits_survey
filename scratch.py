import sqlite3

import matplotlib.pyplot as plt
import pandas as pd
from statsmodels.tsa.stattools import acf
from statsmodels.graphics.tsaplots import plot_acf


conn = sqlite3.connect('./db/realestate.db')
query = "SELECT name, date, total from building_permits where lower(name) like '%new york%'"

df = pd.read_sql_query(query, conn)
conn.close()

print(df['name'].unique())

df['date'] = pd.to_datetime(df['date'])
df.set_index('date', inplace=True)

monthly_diff = df['total'].resample(rule='M').last() #.pct_change().diff()
print(monthly_diff.autocorr())


# Compute the acf array of HRB
acf_array = acf(monthly_diff)
print(acf_array)

# Plot the acf function
plot_acf(acf_array, alpha=1)
plt.show()