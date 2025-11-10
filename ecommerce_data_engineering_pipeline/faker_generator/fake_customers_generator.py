import pyspark
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName('test') \
    .config("spark.executor.memory", "2g") \
    .config("spark.executor.cores", "1") \
    .config("spark.driver.memory", "1g") \
    .getOrCreate()

sample_csv = "gs://ecomm_bucket001/csv_files/customers_info.csv"
output = "gs://ecomm_bucket001/output_files"

df_sample = spark.read.csv(sample_csv, header=True, inferSchema=True)

# Write distributed in Parquet format
df_sample.write.parquet(output, mode='overwrite')
