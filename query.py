'''
query.py
1/11/2018
Emerson Wenzel

A small library of functions to act as an interface to dynamoDB
'''


from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr
import pandas as pd
import numpy as np
from aws import *

#queries a table and returns the items for a specific class (in a department)
def query_class(department, class_num = -1, table_name="INVENTORY"):
    classes = ['Class_1-1', 'Class_1-2', 'Class_1-3', 'Class_1-4',\
               'Class_1-5', 'Class_1-6',
               'Class_2-1', 'Class_2-2']
    dynamodb = boto3.resource('dynamodb', region_name='us-east-2', \
                          aws_access_key_id = aws_key_id,\
                              aws_secret_access_key = aws_key_secret)

    table = dynamodb.Table(table_name)

    # Query Table using searching via department
    # (Search via Dept_1 and Dept_2 for cross listed classes)
    response_Dept_1 = table.query(
        IndexName = 'Dept_1-index',
        KeyConditionExpression = Key('Dept_1').eq(department)
    )
    response_Dept_2 = table.query(
        IndexName = 'Dept_2-index',
        KeyConditionExpression = Key('Dept_2').eq(department)
    )

    # Convert query responses into a dataframe
    df = pd.DataFrame.from_dict(response_Dept_1['Items'] + \
                                response_Dept_2['Items'])

    # Reduce size of df to only include items for specific class
    # If no class number is specified, return all of the items for the department
    if class_num != -1:
        wanted_indices = np.zeros([df.shape[0], 1], dtype = bool)[0]
        for col_name in classes:
            if col_name in df.columns:
                wanted_indices = np.logical_or(wanted_indices,\
                                               (df[col_name] == class_num))

        return df.loc[wanted_indices]
    else:
        return df


#scans and returns a dynamoDB table inside of a pandas dataframe
def scan_table(table_name):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-2', \
                          aws_access_key_id = aws_key_id,\
                              aws_secret_access_key = aws_key_secret)

    table = dynamodb.Table(table_name)
    response = table.scan()
    item_ray = response['Items']


    #Continues querying table if data > 1 MB.
    #Have not actually had the chance to test if this works or not
    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        item_ray = item_ray + response['Items']

    df = pd.DataFrame.from_dict(item_ray)

    return df






# Helper class to convert a DynamoDB item to JSON.
# Currently unused (found in tutorial)
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


