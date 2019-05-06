# -*- coding: utf-8 -*-
"""robi-datathon-19-easy-04

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1HxZl9gYFVs4Nc6EQDOG4aUXq7bXaa5up

#Step 01. Install All Dependencies

This installs Apache Spark 2.3.3, Java 8, Findspark library that makes it easy for Python to work on the given Big Data.
"""

import os
#OpenJDK Dependencies for Spark
os.system('apt-get install openjdk-8-jdk-headless -qq > /dev/null')

#Download Apache Spark
os.system('wget -q http://apache.osuosl.org/spark/spark-2.3.3/spark-2.3.3-bin-hadoop2.7.tgz') 

#Apache Spark and Hadoop Unzip
os.system('tar xf spark-2.3.3-bin-hadoop2.7.tgz')

#FindSpark Install
os.system('pip install -q findspark')

"""# Step 02. Set Environment Variables
Set the locations where Spark and Java are installed based on your installation configuration. Double check before you proceed.
"""

import os
os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-8-openjdk-amd64"
os.environ["SPARK_HOME"] = "/content/spark-2.3.3-bin-hadoop2.7"

"""# Step 03. ELT - Load the Data: Mega Cloud Access
This is an alternative approach to load datasets from already stored in [**Mega Cloud**](https://mega.nz) cloud repository. You need to install the necessary packages and put the link URL of cloud to load the file from cloud directly.
"""

import os
os.system('git clone https://github.com/jeroenmeulenaar/python3-mega.git')
os.chdir('python3-mega')
os.system('pip install -r requirements.txt')

"""# Step 04. ELT - Load the Data: Read Uploaded Dataset
In this approach you can directly load the uploaded dataset downloaded fro Mega Cloud Infrastructure
"""

from mega import Mega
os.chdir('../')
m_revenue = Mega.from_ephemeral()
m_revenue.download_from_url('https://mega.nz/#!1lJH3Q4K!N94-KRSyn22FPb0yxiVJgndjxUStdlfC2_prWDYI2f0')

"""# Step 05. Start a Spark Session
This basic code will prepare to start a Spark session.
"""

import findspark
findspark.init()
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName('ml-datathon19-easy04').master("local[*]").getOrCreate()

"""# Step 06. Exploration - Data Schema View
Now let's load the DataFrame and see the schema view of the Spark dataset
"""

df = spark.read.csv('revenue.csv', header = True, inferSchema = True)
df.printSchema()

"""# Step 07. Exploration - More Statistical Insights from Data
Now we'll grab total number of entries and other statistical analysis of the Spark dataset to have an overview of data
"""

df.describe().show()

"""# Step 08. Exploration - Total Unique Row Count
Now we'll grab total number of unique entries or unique row count of the Spark dataset to have an overview of duplicate data
"""

print("Unique Rows: ")
df.distinct().count()

"""# Step 09. Exploration - Reviewing the NULL values in each column
Since the total row count and unique row count are same, it means there is no duplicate rows in the table. Now we'll grab the count of NULL values per column to check whether any missing values is there or not.
"""

import pyspark.sql.functions as F
df_agg = df.agg(*[F.count(F.when(F.isnull(c), c)).alias(c) for c in df.columns])
df_agg.show()

"""# Step 10. Exploration - Filtering the NULL values rows of Model entries
As there remains no `NULL` values, we can straightly apply the filter scheme to select only `revenue_usd` for `week_number = 34`
"""

df2 = df.filter(df.week_number==34)

"""# Step 11. Implementation - Run the SQL Command
Now on the filtered dataset, we can apply `approxQuantile()` function to get the desired Qunatiles
"""

print("Quantile 0.10:")
print(df2.approxQuantile("revenue_usd", [0.1], 0))
print("Quantile 0.25:")
print(df2.approxQuantile("revenue_usd", [0.25], 0))
print("Quantile 0.75:")
print(df2.approxQuantile("revenue_usd", [0.75], 0))