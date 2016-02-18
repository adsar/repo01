/**
  * Created by adrian on 1/18/16.

  * standalone spark program
  * Run config class:
  *           com.incra.prosper.RunLoanDefaultPredictor
  *
  * Dependencies
  * - Scala 2.11.7
  * - Spark & Hadoop 2.4 .jar build with compatibility option for Scala 11 (built from github)
  *
  *
  */

package com.selftaught.meetup

import au.com.bytecode.opencsv.CSVParser
import org.apache.log4j.{Level, Logger}
import org.apache.spark.mllib.classification.LogisticRegressionWithLBFGS
import org.apache.spark.mllib.evaluation.BinaryClassificationMetrics
import org.apache.spark.mllib.linalg.Vectors
import org.apache.spark.mllib.optimization.{L1Updater, SquaredL2Updater}
import org.apache.spark.mllib.regression.LabeledPoint
import org.apache.spark.{SparkConf, SparkContext}

/**
  */
object RunSelfContained {


  def main(args: Array[String]): Unit = {
    val conf = new SparkConf()
      .setAppName("Template")
      .set("spark.executor.memory", "1g")  //6g
      .setMaster("local[1]")    // 4 threads
    val sc = new SparkContext(conf)

    Logger.getRootLogger.setLevel(Level.WARN)

    val base = "/media/sf_as/repo01/bigd/4ML/data/"
    val rawData = sc.textFile(base + "iris.data")

    val headerAndRows = rawData.map { line => mLine(line) }
    val header = headerAndRows.first
    header foreach println

    val data = headerAndRows.filter(_(0) != header(0))
    println("Number of valid input records " + data.count)

    sc.stop()
  }

  def mLine(line: String) = {
    val parser = new CSVParser(',')
    parser.parseLine(line)
  }

  def safe[S, T](f: S => T): S => Either[T, Exception] = {
    new Function[S, Either[T, Exception]] with Serializable {
      def apply(s: S): Either[T, Exception] = {
        try {
          Left(f(s))
        } catch {
          case e: Exception => Right(e)
        }
      }
    }
  }
}


