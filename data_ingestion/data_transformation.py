#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 31

@author: chelsemet
"""

def covariance(input_path, output_path, **kwargs): 
    from sklearn import preprocessing
    import pandas as pd
    import numpy as np
    df = pd.read_csv(input_path)
    
    #Encoding data
    labelDict = {}
    for feature in df:
        le = preprocessing.LabelEncoder()
        le.fit(df[feature])
        le_name_mapping = dict(zip(le.classes_, le.transform(le.classes_)))
        df[feature] = le.transform(df[feature])
        # Get labels
        labelKey = 'label_' + feature
        labelValue = [*le_name_mapping]
        labelDict[labelKey] =labelValue

    corr_matrix = df.corr()
    # Reshape for BigQuery
    #treatment correlation matrix
    k = 10 #number of variables for heatmap
    cols = corr_matrix.nlargest(k, 'treatment')['treatment'].index
    new_corr_matrix = np.corrcoef(df[cols].values.T)
    treatment_corr_df = pd.DataFrame(new_corr_matrix,index=cols,columns=cols).stack().reset_index()
    treatment_corr_df.columns = ['variable1', 'variable2', 'correlation']

    treatment_corr_df.to_csv(output_path, index=False)

def transforms(input_path, output_path, **kwargs):
    from pyspark.sql import SparkSession
    from pyspark.sql.functions import col, when, udf, array, struct, explode
    from pyspark.sql.types import StringType, ArrayType, StructType, StructField
    from pyspark.ml.feature import StringIndexer, OneHotEncoder, VectorAssembler, PCA
    from pyspark.sql.functions import udf
    from pyspark.sql.types import DoubleType
    from pyspark.ml.linalg import Vector

    # Initialize Spark
    spark = SparkSession.builder.appName("Mental Health Transformations").getOrCreate()

    # read data
    df_clean = spark.read.csv(input_path, header=True, inferSchema=True)
    df = df_clean

    # compute risk factors based on the correlation result
    df_clean = df_clean.withColumn("risk_factors", 
        (when(col("work_interfere").isin("Often", "Sometimes"), 1).otherwise(0) + 
        when(col("family_history") == "Yes", 1).otherwise(0) + 
        when(col("care_options") == "No", 1).otherwise(0) + 
        when(col("benefits") == "No", 1).otherwise(0) + 
        when(col("obs_consequence") == "Yes", 1).otherwise(0) + 
        when(col("anonymity") == "No", 1).otherwise(0) +
        when(col("wellness_program") == "No", 1).otherwise(0) +
        when(col("seek_help") == "No", 1).otherwise(0)
    ))

    # normalize result by age
    avg_by_age = df_clean.groupBy("age_range").agg({"risk_factors": "avg"})
    df_clean = df_clean.join(avg_by_age, on="age_range")
    df_clean = df_clean.withColumn("normalized_risk", col("risk_factors") / col("avg(risk_factors)"))

    # create embeddings for categorical variables
    categorical_cols = df.columns[1:]
    indexers = [StringIndexer(inputCol=c, outputCol=f"{c}_idx") for c in categorical_cols]
    encoders = [OneHotEncoder(inputCol=f"{c}_idx", outputCol=f"{c}_vec") for c in categorical_cols]

    # run PCA on encoded features
    assembler = VectorAssembler(inputCols=[f"{c}_vec" for c in categorical_cols], outputCol="features")
    pca = PCA(k=2, inputCol="features", outputCol="pca_features")

    # apply the transformations
    for indexer in indexers:
        df_clean = indexer.fit(df_clean).transform(df_clean)
    for encoder in encoders:
        df_clean = encoder.fit(df_clean).transform(df_clean)
    df_clean = assembler.transform(df_clean)
    df_pca = pca.fit(df_clean).transform(df_clean)

    # extract PCA components into separate columns
    # Create UDFs to extract each component
    get_pc1 = udf(lambda v: float(v[0]), DoubleType())
    get_pc2 = udf(lambda v: float(v[1]), DoubleType())

    # apply the UDFs
    viz_df = df_pca.withColumn("pc1", get_pc1("pca_features"))\
                .withColumn("pc2", get_pc2("pca_features"))

    # get data for visualization
    result = viz_df.select("Age", "gender_clean", "Country", "treatment", "risk_factors", "normalized_risk", "pc1", "pc2")

    # convert to pandas dataframe
    result_pandas = result.toPandas()

    result_pandas.to_csv(output_path, index=False)