from py4j.protocol import Py4JJavaError
from pyspark.sql import SparkSession
from pyspark.sql.utils import AnalysisException
from utility.log_utils import LogUtils
    
class SparkServiceException(Exception):
    pass


class SparkService:
    def __init__(self, app_name):
        self.spark = (
            SparkSession.builder.appName(app_name).enableHiveSupport().getOrCreate()
        )

        self.spark.conf.set("spark.sql.sources.partitionOverwriteMode", "dynamic")
        self.spark.conf.set("hive.exec.dynamic.partition.mode", "nonstrict")
        self.spark.conf.set("mapreduce.fileoutputcommitter.marksuccessfuljobs", "false")
        self.spark.conf.set("spark.sql.legacy.parquet.datetimeRebaseModeInWrite", "CORRECTED")

        spark_context = self.spark.sparkContext
        spark_context.setLogLevel("INFO")
        self.log_utils = LogUtils()

    def read_parquet_file(self, file_path):
        """
        Function to read a file
        Args:
            file_path (str): The file path where the file is located
        Raises:
            error: Exception thrown if an error occurred
        Returns:
            [dataframe]: The dataframe with the content of the file
        """
        try:
            data_frame = self.spark.read.parquet(file_path)
        except (Py4JJavaError, AnalysisException) as error:
            if "Path does not exist" in str(error):
                return None
            self.log_utils.log_error(
                f"An error ocurred trying to read this file {file_path}. {error}"
            )
            self.log_utils.log_error(error)
            self.stop_spark()
            raise SparkServiceException(error) from error

        return data_frame

    def read_json_file(self, file_path, schema=None):
        """
        Function to read a json file
        Args:
            file_path (str): The file path where the file is located
            schema (schema): Defined schema for json
        Raises:
            error: Exception thrown if an error occurred
        Returns:
            [dataframe]: The dataframe with the content of the file
        """
        try:
            if schema is None:
                data_frame = self.spark.read.json(file_path, multiLine="true")
            else:
                data_frame = self.spark.read.json(
                    file_path, schema=schema, multiLine="true"
                )
        except (Py4JJavaError, AnalysisException, Exception) as error:
            if "Path does not exist" in str(error):
                return None
            self.log_utils.log_error(
                f"An error ocurred trying to read this file {file_path}. {error}"
            )
            self.log_utils.log_error(error)
            self.stop_spark()
            raise SparkServiceException(error) from error

        return data_frame

    def read_xml_file(self, file_path, rootTag, rowTag):
        """
        Function to read a xml file
        Args:
            file_path (str): The file path where the file is located
        Raises:
            error: Exception thrown if an error occurred
        Returns:
            [dataframe]: The dataframe with the content of the file
        """
        try:
            data_frame = (
                self.spark.read.format("com.databricks.spark.xml")
                .option("rootTag", rootTag)
                .option("rowTag", rowTag)
                .load(file_path)
            )

        except (Py4JJavaError, AnalysisException, Exception) as error:
            if "path does not exist" in str(error):
                return None
            self.log_utils.log_error(
                f"An error ocurred trying to read this file {file_path}. {error}"
            )
            self.log_utils.log_error(error)
            self.stop_spark()
            raise SparkServiceException(error) from error

        return data_frame

    def read_csv_file(self, file_path):
        """
        Function to read a csv file
        Args:
            file_path (str): The file path where the file is located
        Raises:
            error: Exception thrown if an error occurred
        Returns:
            [dataframe]: The dataframe with the content of the file
        """
        try:
            data_frame = self.spark.read.option("header", "true").csv(file_path)
        except (Py4JJavaError, AnalysisException, Exception) as error:
            if "Path does not exist" in str(error):
                return None
            self.log_utils.log_error(
                f"An error ocurred trying to read this file {file_path}. {error}"
            )
            self.log_utils.log_error(error)
            self.stop_spark()
            raise SparkServiceException(error) from error

        return data_frame

    def read_from_database(self, table_properties, credentials):
        """
        Function to read a table from postgres
        Args:
            table_properties (str): The table name to read
            credentials (dict): The credentials to connect to the database
        Raises:
            AnalysisException: An exception if an error ocurred
        Returns:
            [dataframe]: The dataframe with the content of the table
        """

        jdbc_reader = (
            self.spark.read.format("jdbc")
            .option("url", credentials.get("url"))
            .option("dbtable", table_properties.get("table_name"))
            .option("user", credentials.get("user"))
            .option("password", credentials.get("password"))
            .option("driver", credentials.get("driver"))
            .option("numPartitions", table_properties.get("num_partitions"))
        )

        partition_column = table_properties.get("partition_column")
        if (
            partition_column and table_properties.get("type_partition_column").upper() != "STRING"
        ):
            jdbc_reader = (
                jdbc_reader.option("partitionColumn", partition_column)
                .option("lowerBound", table_properties.get("lower_bound"))
                .option("upperBound", table_properties.get("upper_bound"))
            )

        try:
            data_frame = jdbc_reader.load()
        except (Exception, AnalysisException) as error:
            self.log_utils.log_error(
                "An error ocurred trying to read this table/query "
                f"{table_properties.get('table_name')}"
            )
            self.log_utils.log_error(error)
            self.stop_spark()
            raise SparkServiceException(error) from error

        return data_frame

    def save_frame(
        self, data_frame, path, num_partitions, mode="overwrite", partiton_columns=None
    ):
        """
        This function will write a dataframe into a path
        Args:
            data_frame (dataframe): The dataframe that will be written
            path (str): The path where the file will be stored
            num_partitions (int): The number of files generated to be saved
            partiton_columns (list[str]): list of column names to partition at save
        Raises:
            SparkServiceException: If an error occurred this exception will be raised
        """
        try:
            if partiton_columns:
                data_frame.repartition(num_partitions).write.format("parquet").mode(
                    mode
                ).partitionBy(*partiton_columns).save(path)
            else:
                data_frame.repartition(num_partitions).write.format("parquet").mode(
                    mode
                ).save(path)
        except (Exception, AnalysisException) as error:
            self.log_utils.log_error(
                f"An error ocurred trying to save the frame into this path {path}"
            )
            self.log_utils.log_error(error)
            self.stop_spark()
            raise SparkServiceException(error) from error

    def get_max_value_from_table(self, table_name, credentials, partition_column):
        """
        This method will get the max value associated to a column from the table
        Args:
            table_name (str): The table name
            credentials (dict): The credentials to connect to the database
            partition_column (str): The column name where the value will be gotten

        Raises:
            SparkServiceException: If an error occurred this exception will be raised

        Returns:
            [str]: The max value from the table
        """
        table_name = f"(SELECT MAX({partition_column}) as MAX from {table_name}) S"
        try:
            data_frame = (
                self.spark.read.format("jdbc")
                .option("url", credentials.get("url"))
                .option("dbtable", table_name)
                .option("user", f"{credentials.get('user')}")
                .option("password", f"{credentials.get('password')}")
                .option("driver", credentials.get("driver"))
                .load()
            )

            column_name = data_frame.schema.names[0]
            max_value = (
                data_frame.select(data_frame[column_name].cast("string"))
                .limit(1)
                .collect()[0][column_name]
            )
        except (Exception, AnalysisException) as error:
            self.log_utils.log_error(
                "An error ocurred trying to get the max value from this table "
                f"{table_name} using this column {partition_column}"
            )
            self.log_utils.log_error(error)
            self.stop_spark()
            raise SparkServiceException(error) from error

        return max_value.replace(" ", "")

    def stop_spark(self):
        """
        Function to stop the spark session
        """
        self.spark.stop()
