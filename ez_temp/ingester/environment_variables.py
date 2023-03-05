import os
import sys
from datetime import datetime


def collect_variables():
    vars = {}

    time_vars = {
        "now": datetime.now()
    }
    vars.update(time_vars)

    os_vars = {
        "os": {
            "name": os.name,
            
        }
    }
    vars.update(os_vars)

    sys_vars = {
        "sys": {
            "defaultencoding": sys.getdefaultencoding(),
            "platform": sys.platform, 
            "winver": sys.getwindowsversion().major if sys.platform == "win32" else None
        }
    }
    vars.update(sys_vars)

    env = {
        "environ": {}
    }
    env['environ'].update(os.environ)
    vars.update(env)

    return vars

