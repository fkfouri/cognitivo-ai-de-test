import json

from pyspark.sql import SparkSession
from pyspark.sql import SQLContext
from pyspark.sql.types import *
from pyspark.sql import functions as f

# type_mapping

TYPE_MAPPING_SPARK = {
    'integer': IntegerType(),
    'timestamp': TimestampType(),
}

# init pyspark
spark = SparkSession.builder.appName("de-test").getOrCreate()
sc = spark.sparkContext

sqlContext = SQLContext(sc)

# read csv and convert to parquet
df = spark.read.csv("data/input/users/load.csv",  header = True)
df.write.mode('overwrite').parquet('tmp/pyspark_users_data')
df = spark.read.parquet('tmp/pyspark_users_data')

# convert using the type_mapping
with open('config/types_mapping.json') as json_file:

    types_mapping = json.load(json_file)

for type in types_mapping:

    df = df.withColumn(type, df[type].cast(TYPE_MAPPING_SPARK[types_mapping[type]]))

# Remove duplicates rows based on max update_date
df_max_date = df.alias('df1').join(
    df.groupBy("id").agg(
        f.max(f.col("update_date")).alias("r_timestamp")
    ).withColumnRenamed(
        "id", "r_id"
    ).alias('df2'),
    f.col('df1.id') == f.col('df2.r_id')
).drop("r_id").drop("update_date").withColumnRenamed('r_timestamp', 'update_date')

df_dedup = df_max_date.dropDuplicates(['id', 'update_date'])

#write deduplicate data to parquet in output dir
df_dedup.write.mode('overwrite').parquet('data/output/users_data')

print('Read output parquet file')

df_dedup_test = spark.read.parquet('data/output/users_data')

print(df_dedup_test.show())
