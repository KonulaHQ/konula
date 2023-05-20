import requests


class Logger:
    def __init__(self, log_method: str = "local"):
        self.log_method = log_method

    def _handle_logging_error(self):
        return

    def _log_to_terminal(self, log_severity, log_type, message):
        if log_severity == "info":
            print(f"[\033[96m{log_type}\033[0m] --- {message}")
        elif log_severity == "warning":
            print(f"[\033[93m{log_type}\033[0m] --- {message}")
        elif log_severity == "error":
            print(f"[\033[91m{log_type}\033[0m] --- {message}")
        elif log_severity == "success":
            print(f"[\033[92m{log_type}\033[0m] --- {message}")
        else:
            print(f"[\033[94m{log_type}\033[0m] --- {message}")
            

    def log(self, log_severity: str, log_type: str, message: str):
        if self.log_method == "local":
            self._log_to_terminal(
                log_severity=log_severity, log_type=log_type, message=message
            )