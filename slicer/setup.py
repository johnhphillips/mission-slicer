from distutils.core import setup
import py2exe
 
setup(
windows = [
    {
        "script": "slicer_gui.py",
        "icon_resources": [(1, "default.ico")]
    }
],
)
