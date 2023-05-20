# BETA

import redshift_connector

class RedshiftConnector:
    def __init__(
        self,
        creds: dict,
        database: str,
        table: str,
        schema: str = "public",
        port: int = 5439,
    ):
        self.creds = creds
        self.table = table
        self.schema = schema
        self.conn = redshift_connector.connect(
            database=database,
            user=creds["user"],
            password=creds["password"],
            host=creds["host"],
            port=port,
        )
        self.cursor = self.conn.cursor()
        self.col_data_types = self._get_data_type()

    def _execute(self, sql):
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        return results

    def _get_data_type(self):
        sql = f"""
            SELECT column_name, data_type
            FROM information_schema.columns
            WHERE table_schema = '{self.schema}'
            AND table_name = '{self.table}';"""
        mapping = {}
        results = self._execute(sql=sql)
        for r in results:
            mapping[r[0]] = r[1]
        return mapping

    def get_columns_list(self):
        sql = f"""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_schema = '{self.schema}'
            AND table_name = '{self.table}';"""
        result_list = []
        results = self._execute(sql=sql)
        for r in results:
            result_list.append(r[0])
        return result_list

    def check__table_columns_count(self):
        sql = f"""
            SELECT count(*)
            FROM information_schema.columns
            WHERE table_schema = '{self.schema}'
            AND table_name = '{self.table}';"""
        return {"result_type": "range", "result": self._execute(sql=sql)[0][0]}

    def check__table_columns_list(self):
        sql = f"""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_schema = '{self.schema}'
            AND table_name = '{self.table}';"""
        result_list = []
        results = self._execute(sql=sql)
        for r in results:
            result_list.append(r[0])
        return {"result_type": "list", "result": result_list}

    def check__col_min(self, col):
        """Get the column min value"""
        if self.col_data_types[col] in [
            "smallint",
            "integer",
            "bigint",
            "decimal",
            "numberic",
            "real",
            "double_precision",
            "smallserial",
            "serial",
            "bigserial",
        ]:
            sql = f"""
                SELECT MIN({col})
                FROM {self.schema}.{self.table}"""
            return {
                "result_type": "range",
                "result": float(self._execute(sql=sql)[0][0]),
            }
        return None

    def check__col_max(self, col):
        """Get the column min value"""
        if self.col_data_types[col] in [
            "smallint",
            "integer",
            "bigint",
            "decimal",
            "numberic",
            "real",
            "double_precision",
            "smallserial",
            "serial",
            "bigserial",
        ]:
            sql = f"""
                SELECT MAX({col})
                FROM {self.schema}.{self.table}"""
            return {
                "result_type": "range",
                "result": float(self._execute(sql=sql)[0][0]),
            }
        return None

    def check__col_mean(self, col):
        """Get the column mean value"""
        if self.col_data_types[col] in [
            "smallint",
            "integer",
            "bigint",
            "decimal",
            "numberic",
            "real",
            "double_precision",
            "smallserial",
            "serial",
            "bigserial",
        ]:
            sql = f"""
                SELECT AVG({col})
                FROM {self.schema}.{self.table}"""
            return {
                "result_type": "range",
                "result": float(self._execute(sql=sql)[0][0]),
            }
        return None

    def check__col_median(self, col):
        """Get the column median value"""
        if self.col_data_types[col] in [
            "smallint",
            "integer",
            "bigint",
            "decimal",
            "numberic",
            "real",
            "double_precision",
            "smallserial",
            "serial",
            "bigserial",
        ]:
            sql = f"""
                SELECT PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY {col}) AS median
                FROM {self.schema}.{self.table}"""
            return {
                "result_type": "range",
                "result": float(self._execute(sql=sql)[0][0]),
            }
        return None

    def check__col_mode(self, col):
        """Get the column mode value"""
        if self.col_data_types[col] in [
            "smallint",
            "integer",
            "bigint",
            "decimal",
            "numberic",
            "real",
            "double_precision",
            "smallserial",
            "serial",
            "bigserial",
        ]:
            sql = f"""
                SELECT MODE() WITHIN GROUP (ORDER BY {col}) AS mode
                FROM {self.schema}.{self.table}"""
            return {
                "result_type": "range",
                "result": float(self._execute(sql=sql)[0][0]),
            }
        return None

    def check__col_null_count(self, col):
        """Get the column null count"""
        sql = f"""
                select count(*)
                from {self.schema}.{self.table}
                where {col}
                is NULL;"""
        return {
            "result_type": "range",
            "result": float(self._execute(sql=sql)[0][0]),
        }

    def check__col_empty_count(self, col):
        """Get the column empty string count"""
        if self.col_data_types[col] in [
            "character",
            "varying",
            "varchar",
            "character",
            "char",
            "text",
        ]:
            sql = f"""
                    select count(*)
                    from {self.schema}.{self.table}
                    where {col}
                    = '';"""
            return {
                "result_type": "range",
                "result": float(self._execute(sql=sql)[0][0]),
            }
        return

    def check__col_null_or_empty_count(self, col):
        """Get the column null count plus the column empty string count"""
        if self.col_data_types[col] in [
            "character",
            "varying",
            "varchar",
            "character",
            "char",
            "text",
        ]:
            sql = f"""
                    select count(*)
                    from {self.schema}.{self.table}
                    where {col}
                    = '' or {col} is NULL;
                """
            return {
                "result_type": "range",
                "result": float(self._execute(sql=sql)[0][0]),
            }
        return

    def check__col_distinct_count(self, col):
        """Get the column distinct count"""
        sql = f"""
                select count(distinct({col}))
                from {self.schema}.{self.table};
            """
        return {
            "result_type": "range",
            "result": float(self._execute(sql=sql)[0][0]),
        }

    def check__col_distinct_list(self, col):
        """Get the column distinct list"""
        sql = f"""
                select distinct({col})
                from {self.schema}.{self.table};
            """
        result = self._execute(sql=sql)
        result = ["".join(str(i)) for i in result]
        return {
            "result_type": "list",
            "result": result,
        }

    def check__col_duplicate_list(self, col):
        """Get the column duplicate list"""
        sql = f"""
                select {col}, count(*)
                from {self.schema}.{self.table}
                group by {col}
                HAVING count(*) > 1
            """
        result_list = []
        result = self._execute(sql=sql)
        for r in result:
            result_list.append(r[0])
        return {
            "result_type": "list",
            "result": result_list,
        }
