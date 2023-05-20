import pandas as pd
import json
from core.base.check import Check
from core.connectors.sources.pandas_connector import PandasConnector

data = [
    ["tom", 10, "jones"],
    ["nick", 15, "jones"],
    ["juli", 14, "jones"],
    ["sam", 14, "jones"],
    ["", 14.55, "jones"],
    ["nick", None, "jones"],
]
df = pd.DataFrame(data, columns=["Name", "Age", "LName"], dtype="object")

conn = PandasConnector(dataframe=df)
check = Check(connector=conn, checkpoint_id="test")

check_list = check._generate_checks()

results = check.run_local(checks=check_list)

print(results)
