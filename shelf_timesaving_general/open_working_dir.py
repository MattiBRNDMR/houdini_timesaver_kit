import hou  
import os 

hip_dir = hou.hipFile.path()
path = hip_dir.split("/")[0:-1]
open_path = "/".join(path)

hou.ui.showInFileBrowser(open_path)
