'''
app.py


'''

from query import *
import pandas as pd



df = scan_table("SOLD_INVENTORY")
print(df)
