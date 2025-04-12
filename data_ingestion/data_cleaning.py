#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 31

@author: chelsemet
"""

def data_cleaning(input_path, output_path, **kwargs):
    import pandas as pd

    df = pd.read_csv(input_path)

    # Data cleaning
    df = df.drop(['comments','state','Timestamp'], axis = 1)

    # NaN cleaning
    stringFeature = df.columns[1:]
    df[stringFeature] = df[stringFeature].fillna('NaN')

    #Feature cleaning
    ##gender
    gender = df['Gender'].str.lower()
    gender = gender.unique()

    female_str = ['female','cis female','f','woman','femake','female ','cis-female/femme','female (cis)','femail']
    nonbinary_str = ['trans-female','something kinda male?','queer/she/they','non-binary','nah','all','enby','fluid','genderqueer','androgyne','agender','guy (-ish) ^_^','male leaning androgynous','trans woman','neuter','female (trans)','queer','a little about you','p','ostensibly male, unsure what that really means']       
    male_str = ['m','male','male-ish','maile','cis male','mal','male (cis)','make','male ','man','msle','mail','malr','cis man']

    def categorize_gender(gender):
        if gender in female_str:
            return 'female'
        elif gender in nonbinary_str:
            return 'non-binary'
        elif gender in male_str:
            return 'male'
        else:
            return 'non-binary'
        
    df['gender_clean'] = df['Gender'].apply(categorize_gender)
    df = df.drop(['Gender'], axis = 1)

    ##age
    #fill missing age with median
    median_value = df['Age'].median()
    df['Age'].fillna(median_value, inplace = True)

    #fill unreasonble ages with median
    #assume legal workers
    df['Age'] = df['Age'].mask(df['Age'] <= 14, median_value)
    df['Age'] = df['Age'].mask(df['Age'] > 100, median_value)

    df['age_range'] = pd.cut(df['Age'], [14,30,40,50,65,100], labels=["14-30", "30-40", "40-50", "50-65","65 and above"], include_lowest=True)

    ##others
    df['work_interfere'] = df['work_interfere'].fillna('Don\'t know')
    df['self_employed'] = df['self_employed'].fillna('Don\'t know')

    df.to_csv(output_path, index=False)