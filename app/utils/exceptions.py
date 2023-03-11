import traceback
from datetime import datetime

from flask import current_app


def exception_handler(e):
    log_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(f"{current_app.root_path}/{current_app.config['ERROR_LOG']}", "a") as file:
        file.write(f"\n[{log_time}] " + str(e) + "\n")
        traceback.print_exc(file=file)

    return e
