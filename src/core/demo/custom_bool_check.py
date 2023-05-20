import pandas as pd
import json
from core.base.check import Check
from core.connectors.sources.custom import CustomConnector



conn = CustomConnector()
check = Check(connector=conn, checkpoint_id="test_custom")

check_list = check._generate_checks() # should successfully return empty list []

# print(json.dumps(check.run_local(checks=check_list)))
metadata = {
    'author':'scox',
    'project':'custom_test_demo',
    'version': 7,
    'list_of_items':
    [
        'list', 'of', 'items'
    ]
}
check_list = [{"check": "bool", "value": True, "expected":True, "metadata":metadata}]
print(check.run_local(checks=check_list))

check.run_remote(checks=check_list, name="test", check_id=2)
