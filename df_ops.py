
'''
additional.py
Emerson Wenzel

'''
import pandas as pd

def get_class_data(df, dept_num):
    depts   = ['Dept_1', 'Dept_2']
    nums    = ['Class_1-1', 'Class_1-2', 'Class_1-3', 'Class_1-4',\
               'Class_1-5', 'Class_1-6',
               'Class_2-1', 'Class_2-2']

    # Get the department and class number
    res = pd.DataFrame()
    print("df_ops------")
    print(dept_num)
    print(type(dept_num))
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




def get_master_list(df):
    #Currently, there are only Dept_1 and Dept_2
    #So only have a list of 1 and 2
    master_list = []
    
    dept_array = ['Dept_1', 'Dept_2']
    class_dict = {'Dept_1' : ['Class_1-1', 'Class_1-2', 'Class_1-3', 'Class_1-4',\
                              'Class_1-5', 'Class_1-6'],
                  'Dept_2' : ['Class_2-1', 'Class_2-2']
    }

    
    classes = ['Class_1-1', 'Class_1-2', 'Class_1-3', 'Class_1-4',\
               'Class_1-5', 'Class_1-6',
               'Class_2-1', 'Class_2-2']

    #Make a set of all departments available.
    departments = set(list(df['Dept_1']) + list(df['Dept_2']))
    masterlist = []
    for dept_name in departments:

        avail_classes = []
        #For "Dept_1", "Dept_2", etc.
        for dept_col_header in dept_array:
            df_dept =  df.loc[df[dept_col_header] == dept_name]

            aggregate_list = []
            #Check the columns for the proper department (e.g)
            for class_col_header in class_dict[dept_col_header]:
                if class_col_header in df_dept.columns:
                    aggregate_list = aggregate_list + list(df_dept[class_col_header])

            aggregate_list = [x for x in aggregate_list if str(x) != 'nan']

            avail_classes = avail_classes + aggregate_list
            
            
        #Add the class numbers (with dept concatenated) to the master list
        masterlist = masterlist + [dept_name + " " + str(x) for x in avail_classes]

    #Turn the master list into a set to remove duplicates
    return sorted(set(masterlist))
        


if __name__ == '__main__':
    df = query.scan_table("INVENTORY")
    print(df)
    print('start')
    masterset = get_master_list(df)
    print(masterset)
    print(len(masterset))
