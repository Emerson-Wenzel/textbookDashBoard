'''

rowdata.py
Contains interface to retrieve textbook data from dataframe for a given class.

'''

import pandas as pd

def get_class_data(df, dept_num):
    depts   = ['Dept_1', 'Dept_2']
    nums    = ['Class_1-1', 'Class_1-2', 'Class_1-3', 'Class_1-4',\
               'Class_1-5', 'Class_1-6',
               'Class_2-1', 'Class_2-2']

    # Get the department and class number
    res = pd.DataFrame()
    vals = dept_num.split(' ')
    q_dept = vals[0]
    q_num  = vals[1]

    # Loop through rows
    for i, row in df.iterrows():
        # Loop through departments
        for dept in depts:
            if dept in df.columns:
                # Check that the sought department is found
                if df.get_value(i, dept) == q_dept:
                    for num in nums:
                        if num in df.columns:
                            # Check that the sought number is found
                            if df.get_value(i, num) == q_num:
                                res.append(df[i])
    return res