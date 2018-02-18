'''
df_ops.py
Mohsin Rizvi and Emerson Wenzel

contains functions that perform operations on a dataframe containing TCU Senate textbook data
'''
import pandas as pd
import numpy as np

###
import query
#def get_class_data(df, dept_num):
def get_class_data():
    df = query.scan_table("INVENTORY")
    dept_num = "CHEM 1"
    
    dept_array   = ['Dept_1', 'Dept_2']
    class_dict = {'Dept_1' : ['Class_1-1', 'Class_1-2', 'Class_1-3', 'Class_1-4',\
                              'Class_1-5', 'Class_1-6'],
                  'Dept_2' : ['Class_2-1', 'Class_2-2']
    }
    class_array    = ['Class_1-1', 'Class_1-2', 'Class_1-3', 'Class_1-4',\
               'Class_1-5', 'Class_1-6',
               'Class_2-1', 'Class_2-2']



    # Get the department and class number
    res = pd.DataFrame()

    vals = dept_num.split(' ')
    q_dept = vals[0]
    q_class  = vals[1]

    new_df = pd.DataFrame(columns=df.columns)
    print("new_df")
    print(new_df)
    for dept_col_header in dept_array:
        
        #grab all the books that are in the proper department
        df_dept =  df.loc[df[dept_col_header] == q_dept]
        if (df_dept.empty == True):
            continue
        
        wanted_indices = np.zeros((df_dept.shape[0], 1), dtype=bool)[:,0]

        print(df_dept)
        
        #Check the columns for the proper department (e.g)
        for class_col_header in class_dict[dept_col_header]:
            if class_col_header in df_dept.columns:
                new_indices = df_dept[class_col_header] == q_class
                wanted_indices = np.bitwise_or(wanted_indices, new_indices)
                print(wanted_indices)
                
        new_df = pd.concat([new_df, df_dept[wanted_indices]])

    return new_df


# get_master_list
#     parameters - a dataframe containing various textbook entries
#     return value - A set of all classes in the dataframe (e.g. "CHEM 1", "HIST 53", etc.)

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
    df = get_class_data()
    print("finished function\n")
    print(df)




    '''                
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
    '''
