from pyspark import SparkConf, SparkContext
import collections

conf = SparkConf().setMaster("local").setAppName("Ratings")
sc = SparkContext.getOrCreate(conf=conf)

lines = sc.textFile("smaple.txt")

lines.count()

lines.first()

lines.take(3)
