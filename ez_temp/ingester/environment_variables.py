import os
import sys
import pprint

def collect_variables():
    vars = {}
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


