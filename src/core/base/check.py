import datetime
import json
import requests
from .logger import Logger


class Check:
    def __init__(
        self,
        connector: callable,
        checkpoint_id: str,
        secondary_connector: callable = None,
    ):
        self.connector = connector
        self.secondary_connector = secondary_connector
        self.checkpoint_id = checkpoint_id
        self.check_type = connector.get_check_type()
        self.logger = Logger()


    def _get_connector_checks(self):
        method_list = [
            func
            for func in dir(self.connector)
            if callable(getattr(self.connector, func))
        ]
        valid_checks = [
            x.replace("check__", "") for x in method_list if x.startswith("check__")
        ]
        return valid_checks

    def _validate_connector_compatibility(self, checks):
        self.logger.log(log_severity='info', log_type='INFO', message='Validating test compatibility')
        for c in checks:
            if c["check"] not in self._get_connector_checks():
                # TODO: Handle error if its not here, rather than just printing
                self.logger.log(log_severity='error', log_type='DEBUG', message='Connector test unavailable')


    def _generate_checks(self, check_list: str = "__all__", col_list: str = "__all__"):
        self.logger.log(log_severity='info', log_type='INFO', message='Generating connector tests')
        if check_list == "__all__":
            check_list = self._get_connector_checks()
        if col_list == "__all__" and self.check_type == 'table':
            col_list = self.connector.get_columns_list()
        gen_checks = []
        table_check_count = 0
        col_check_count = 0

        for c in check_list:
            if c.startswith("table_"):
                table_check_count += 1
            elif c.startswith("col_"):
                col_check_count += 1

        self.logger.log(log_severity='info', log_type='INFO', message=f'Running ({table_check_count}) table and ({col_check_count}) col test generations')

        for c in check_list: 
            if c.startswith("table_"):
                check = getattr(self.connector, f"check__{c}")
                check_run = check()
                if check_run["result_type"] == "range":
                    check_run_result = [check_run["result"], check_run["result"]]
                else:
                    check_run_result = check_run["result"]
                gen_checks.append(
                    {"check": c, "column": col, "expected": check_run_result}
                )
            elif c.startswith("col_"):
                for col in col_list:
                    check = getattr(self.connector, f"check__{c}")
                    check_run = check(col=col)
                    if check_run:
                        if check_run["result_type"] == "range":
                            check_run_result = [
                                check_run["result"],
                                check_run["result"],
                            ]
                        else:
                            check_run_result = check_run["result"]
                        gen_checks.append(
                            {"check": c, "column": col, "expected": check_run_result}
                        )
        self.logger.log(log_severity='success', log_type='STATE', message=f'Connector tests created')
        return gen_checks

    def _interpret_check_success(self, result_type, expected, actual):
        if result_type == "list":
            expected_list = expected.sort()
            result_list = actual.sort()
            if expected_list == result_list:
                return True
        elif result_type == "range":
            if (
                actual >= expected[0]
                and actual <= expected[1]
            ):
                return True
        elif result_type == "bool":
            if (
                actual["value"] == expected
            ):
                return True
        return False
        
    def _initiate_run(self, checks):
        """Setup the check run"""
        self._validate_connector_compatibility(checks=checks)
        failed_checks = 0
        successful_checks = 0
        id = 0
        self.logger.log(log_severity='info', log_type='INFO', message=f'Running ({len(checks)}) tests')
        for c in checks:
            c["id"] = id
            id += 1
            check = getattr(self.connector, f"check__{c['check']}")
            if c["check"].startswith("col"):
                check_res = check(col=c["column"])
            elif c["check"].startswith("table"):
                check_res = check()
            elif c["check"].startswith("bool"):
                check_res = check(value=c["value"], metadata=c["metadata"])
            c["result"] = check_res["result"]
            c["result_type"] = check_res["result_type"]
            check_success = self._interpret_check_success(result_type=check_res["result_type"], expected=c["expected"], actual=c["result"])
            if check_success:
                c["success"] = True
                successful_checks += 1
            else:
                c["success"] = False
                failed_checks += 1
                    
        self.logger.log(log_severity='success', log_type='STATE', message=f'Tests completed')
        if failed_checks > 0:
            success_rate = int(
                (successful_checks / (successful_checks + failed_checks)) * 100
            )
            self.logger.log(log_severity='error', log_type='RESULT', message=f'One or more tests failed')
        else:
            success_rate = 100
            self.logger.log(log_severity='success', log_type='RESULT', message=f'All tests succeeded')
        check_result = {
            "summary": {
                "all_succeeded": failed_checks == 0,
                "success_rate": success_rate,
                "successful_checks": successful_checks,
                "failed_checks": failed_checks,
                "check_type": self.check_type
            },
            "checks": checks,
        }
        self.logger.log(log_severity='success', log_type='STATE', message=f'Test results stored')

        return check_result

    
    def run_local(self, checks):
        """Run locally"""
        self.logger = Logger(log_method='local')

        return self._initiate_run(checks=checks)
    