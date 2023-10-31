import os
import sys
from datetime import datetime


def collect_variables():
    variables = {}
    time_vars = {
        "now": datetime.now().strftime("%H:%M %d-%m-%y")
    }
    variables.update(time_vars)

    os_vars = {
        "os": {
            "name": os.name,
        }
    }
    variables.update(os_vars)

    sys_vars = {
        "sys": {
            "defaultencoding": sys.getdefaultencoding(),
            "platform": sys.platform,
            "winver": sys.getwindowsversion().major if sys.platform == "win32" else None,
        }
    }
    variables.update(sys_vars)

    env = {
        "environ": {}
    }
    env['environ'].update(os.environ)
    variables.update(env)

    return variables

