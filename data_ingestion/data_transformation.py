#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 31

@author: chelsemet
"""

def covariance(df, **kwargs): 
    import sklearn
    import pandas as pd

    DATA_DIR = '/opt/airflow/data'

    #Encoding data
    labelDict = {}
    for feature in df:
        le = sklearn.preprocessing.LabelEncoder()
        le.fit(df[feature])
        le_name_mapping = dict(zip(le.classes_, le.transform(le.classes_)))
        df[feature] = le.transform(df[feature])
        # Get labels
        labelKey = 'label_' + feature
        labelValue = [*le_name_mapping]
        labelDict[labelKey] =labelValue

    #Get rid of 'Country'
    df = df.drop(['Country'], axis= 1)

    cov_matrix = df.cov()
    # Reshape for BigQuery
    cov_df = cov_matrix.stack().reset_index()
    cov_df.columns = ['variable1', 'variable2', 'covariance']

    return cov_df