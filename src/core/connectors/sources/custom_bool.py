# Test
class CustomBoolConnector:

    def get_check_type(self):
        return 'custom'
    
    def check__bool(self, value: bool, metadata: dict):
        return {"result_type": "bool", "result": {"value":value, "metadata":metadata}}
    
    # def check__http_health(self):
    #     return
    
