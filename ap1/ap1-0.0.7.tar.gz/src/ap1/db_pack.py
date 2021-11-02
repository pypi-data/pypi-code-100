import re
import psycopg2
import psycopg2.extras


class Database:
    def __init__(self, out_conn_config, monitoring_conn_config, monitoring_source_name, logger):
        self.out_conn = psycopg2.connect(out_conn_config) if out_conn_config else None
        self.monitoring_conn = psycopg2.connect(monitoring_conn_config) if monitoring_conn_config else None
        self.monitoring_source_name = monitoring_source_name
        self.logger = logger

    def camelCase_To_snake_case(self, s):
        return re.sub(r'(?<!^)(?=[A-Z])', '_', s).lower()

    def upload(self, table_name, fields, objects):
        if not self.out_conn:
            raise Exception("Add out_conn to config file")

        snake_case_fields = list(map(lambda s: self.camelCase_To_snake_case(s), fields))
        fields_text = ' ,'.join(snake_case_fields)
        query = "insert into {}({}) values %s".format(table_name, fields_text)
        cursor = self.out_conn.cursor()
        # cursor.execute(f"Select * FROM {table_name} LIMIT 0")
        # colnames = [desc[0] for desc in cursor.description]
        # print(colnames)

        try:
            psycopg2.extras.execute_values(cursor, query, objects, template=None, page_size=100)
            self.out_conn.commit()
            self.logger.info('Upserted objects ' + str(len(objects)) + ' into ' + table_name)

        except (Exception, psycopg2.DatabaseError) as error:
            self.logger.error(error, 'xx')
            self.out_conn.rollback()
            cursor.close()
            return 1

    def getParserStatus(self):
        if not self.monitoring_conn:
            self.logger.warning("Monitoring is ignored. Remove debug_mode from config file or set to false")
            return

        query = f"""
             select parsed from monitoring.parser_monitoring
        where name = {self.monitoring_source_name}
            """

        dict_cur = self.monitoring_conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        self.logger.info('Selecting parser status')
        try:
            dict_cur.execute(query)
        except (Exception, psycopg2.DatabaseError) as error:
            self.logger.warning(error)
        rows = dict_cur.fetchall()
        if rows:
            return rows[0]
        else:
            raise Exception(f"{self.monitoring_source_name} not in monitoring")

    def updateParserStatus(self, status):
        if not self.monitoring_conn:
            self.logger.warning("Monitoring is ignored. Remove debug_mode from config file or set to false")
            return

        query = f"""
        update
        parser_monitoring
        set
        parsed = %s
        {',last_parsed = now()' if status else ''}
        where
        name = {self.monitoring_source_name} """

        cursor = self.monitoring_conn.cursor()
        self.logger.info('Updating parser info')
        try:
            cursor.execute(query, (status,))
            self.monitoring_conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            self.logger.warning(error)
            self.monitoring_conn.rollback()
            cursor.close()
            return 1
