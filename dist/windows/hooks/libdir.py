import os
import sys

def extend_system_path(paths):
    old = os.environ.get('PATH', '')
    paths.append(old)
    new = os.pathsep.join(paths)
    os.environ['PATH'] = new

d = os.path.abspath(os.path.join(sys._MEIPASS, "lib"))

sys.path.append(d)
extend_system_path([d])
