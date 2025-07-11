from pyspark.sql import SparkSession
from pyspark.sql.functions import col, regexp_replace, trim
from pyspark.sql.types import DoubleType, IntegerType

# PostgreSQL config
pg_url = "jdbc:postgresql://postgres_main:5432/nrbproperties"
pg_properties = {
    "user": "postgres",
    "password": "postgres",
    "driver": "org.postgresql.Driver"
}

# Initialize Spark session
spark = SparkSession.builder \
    .appName("Property24 Batch Processor") \
    .config("spark.jars", "/opt/spark-apps/postgresql-42.7.1.jar") \
    .getOrCreate()

# Read from raw_listings
df = spark.read.jdbc(url=pg_url, table="raw_listings", properties=pg_properties)

# Clean data
clean_df = df.filter(col("title").isNotNull()) \
    .withColumn("price", regexp_replace("price", "[^0-9.]", "").cast(DoubleType())) \
    .withColumn("size_sqm", regexp_replace("size_sqm", "[^0-9.]", "").cast(DoubleType())) \
    .withColumn("bedrooms", col("bedrooms").cast(IntegerType())) \
    .withColumn("bathrooms", col("bathrooms").cast(IntegerType())) \
    .withColumn("parking", col("parking").cast(IntegerType())) \
    .withColumn("title", trim(col("title"))) \
    .dropDuplicates(["title", "price", "address"])

# Write to clean_listings (append mode)
clean_df.write.jdbc(
    url=pg_url,
    table="clean_listings",
    mode="append",
    properties=pg_properties
)

spark.stop()
