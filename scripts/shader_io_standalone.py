import vray.aetemplates.AEVRayProxyTemplate as vrayIO
import maya.cmds as mc
import sys
import os
import PrismInit
sys.path.append("Z:\\junior_year\\F23\\collab\\git_repos\\material_assignment\\")
from scripts.material_assignment import export_materials as em

NAME = "ShaderIO"
CLASSNAME = "ShaderIO"
CORE = PrismInit.pcore
VERSION = "v2.0.0beta17.8"

proxy_list = em.get_proxy_from_selection(mc.ls(sl=True))

print(proxy_list)

filepath = CORE.getCurrentFileName()
asset = filepath.split("Characters\\")[1].split("\\", 1)[0]
look_dir = f"{CORE.projectPath}\\03_Production\\Assets\\Characters\\{asset}\\Look"
look_file = f"{look_dir}\\look.ma"
assignment_file = f"{look_dir}\\assignment.xml"

vrayIO.vrayExportProxyRules()

# print checks
# print(filepath)
# print(asset)
# print(look_dir)
# print(look_file)
# print(assignment_file)