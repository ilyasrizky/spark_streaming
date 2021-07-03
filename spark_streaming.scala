import org.apache.kafka.clients.consumer.ConsumerRecord
import org.apache.kafka.common.serialization.StringDeserializer
import org.apache.spark.streaming.kafka010._
import org.apache.spark.streaming.kafka010.LocationStrategies.PreferConsistent
import org.apache.spark.streaming.kafka010.ConsumerStrategies.Subscribe
import org.apache.spark.sql.functions._
import org.apache.spark._
import org.apache.spark.streaming._

val ssc = new StreamingContext(sc, Seconds(1))
val kafkaParams = Map[String, Object](
  "bootstrap.servers" -> "localhost:29092",
  "key.deserializer" -> classOf[StringDeserializer],
  "value.deserializer" -> classOf[StringDeserializer],
  "group.id" -> "group_1",
  "auto.offset.reset" -> "earliest",
  "enable.auto.commit" -> (false: java.lang.Boolean)
)

val topics = Array("data_pengguna")
val stream = KafkaUtils.createDirectStream[String, String](
  ssc,
  PreferConsistent,
  Subscribe[String, String](topics, kafkaParams)
)

stream.foreachRDD(rdd =>
    if (!rdd.isEmpty()) {
        val topicValueStrings = rdd.map(record => (record.value()).toString)
        val df = spark.read.json(topicValueStrings)
        val transformed_df = df.withColumn("alamat", regexp_replace('alamat, "[\n\r]", " "))
        transformed_df.show(false)
})

ssc.start()
// Optional
// ssc.awaitTermination()