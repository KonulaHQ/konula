import pandas as pd


class PandasConnector:
    def __init__(self, dataframe):
        self.dataframe = dataframe.infer_objects()

    def get_check_type(self):
        return 'table'

    def get_columns_list(self):
        return list(self.dataframe.columns)

    def check__table_columns_count(self):
        return {"result_type": "range", "result": self.dataframe.shape[1]}

    def check__table_columns_list(self):
        return {"result_type": "list", "result": list(self.dataframe.columns)}

    def check__col_min(self, col):
        """Get the column min value"""
        if self.dataframe[col].dtype in ["float64", "int64"]:
            return {"result_type": "range", "result": self.dataframe[col].agg("min")}

    def check__col_max(self, col):
        """Get the column max value"""
        if self.dataframe[col].dtype in ["float64", "int64"]:
            return {"result_type": "range", "result": self.dataframe[col].agg("max")}

    def check__col_mean(self, col):
        """Get the column mean value"""
        if self.dataframe[col].dtype in ["float64", "int64"]:
            return {"result_type": "range", "result": self.dataframe[col].agg("mean")}

    def check__col_median(self, col):
        """Get the column median value"""
        if self.dataframe[col].dtype in ["float64", "int64"]:
            return {"result_type": "range", "result": self.dataframe[col].agg("median")}

    def check__col_mode(self, col):
        """Get the column mode value"""
        if self.dataframe[col].dtype in ["float64", "int64"]:
            return {
                "result_type": "range",
                "result": float(self.dataframe[col].agg("mode")[0]),
            }

    def check__col_null_count(self, col):
        """Get the column null count"""
        if self.dataframe[col].dtype in ["float64", "int64"]:
            return {
                "result_type": "range",
                "result": int(self.dataframe[col].isna().sum()),
            }

    def check__col_empty_count(self, col):
        """Get the column empty string count"""
        if self.dataframe[col].dtype in ["float64", "int64"]:
            return {
                "result_type": "range",
                "result": int(
                    self.dataframe.loc[self.dataframe[col] == ""].count().iloc[0]
                ),
            }

    def check__col_null_or_empty_count(self, col):
        """Get the column null count plus the column empty string count"""
        if self.dataframe[col].dtype in ["float64", "int64"]:
            return {
                "result_type": "range",
                "result": int(
                    self.dataframe[col].isna().sum()
                    + self.dataframe.loc[self.dataframe[col] == ""].count().iloc[0]
                ),
            }

    def check__col_distinct_count(self, col):
        """Get the column distinct count"""
        if self.dataframe[col].dtype in ["float64", "int64"]:
            return {
                "result_type": "range",
                "result": int(self.dataframe[col].nunique()),
            }

    def check__col_distinct_list(self, col):
        """Get the column distinct list"""
        if self.dataframe[col].dtype in ["float64", "int64"]:
            return {"result_type": "list", "result": list(self.dataframe[col].unique())}

    def check__col_duplicate_count(self, col):
        """Get the column duplicate count"""
        df = self.dataframe
        df["duplicates"] = self.dataframe[col].duplicated()
        df = df[df["duplicates"] == True]
        if self.dataframe[col].dtype in ["float64", "int64"]:
            return {"result_type": "range", "result": int(df[col].nunique())}

    def check__col_duplicate_list(self, col):
        """Get the column duplicate list"""
        df = self.dataframe
        df["duplicates"] = self.dataframe[col].duplicated()
        df = df[df["duplicates"] == True]
        if self.dataframe[col].dtype in ["float64", "int64"]:
            return {"result_type": "list", "result": list(df[col].unique())}
