from fbs_runtime.application_context.PySide2 import ApplicationContext
from Todo import Todo

import sys

if __name__ == '__main__':
    appctxt = ApplicationContext()  # 1. Instantiate ApplicationContext
    stylesheet = appctxt.get_resource("styles/dark.qss")
    appctxt.app.setStyleSheet(open(stylesheet).read())
    window = Todo()
    window.show()
    exit_code = appctxt.app.exec_()      # 2. Invoke appctxt.app.exec_()
    sys.exit(exit_code)