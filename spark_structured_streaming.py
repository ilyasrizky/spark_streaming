from os import truncate
from pyspark.sql import SparkSession
from pyspark.sql import functions as f

BOOTSTRAP_SERVER = "localhost:29092"
TOPIC_NAME = "data_pengguna"

spark = SparkSession \
    .builder \
    .appName("StructuredStreamingContoh") \
    .getOrCreate()

spark.sparkContext.setLogLevel('WARN')

df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", BOOTSTRAP_SERVER) \
    .option("subscribe", TOPIC_NAME) \
    .option("startingOffsets", "earliest") \
    .load()


def foreach_batch_function(data, epoch_id):
    data.show(truncate=False)


df \
    .withColumn("tahun_lahir", f.date_format(f.get_json_object(f.col("value"), "$.tanggal_lahir").cast("date"), "yyyy").cast("int")) \
    .groupBy("tahun_lahir") \
    .agg(f.count("*").alias("jumlah_orang")) \
    .select("*") \
    .writeStream \
    .foreachBatch(foreach_batch_function) \
    .start() \
    .awaitTermination()
