import vray.aetemplates.AEVRayProxyTemplate as vrayIO
import maya.cmds as mc
import importlib
import sys
import os
import PrismInit
sys.path.append("Z:\\junior_year\\F23\\collab\\git_repos\\material_assignment\\")
from scripts.material_assignment import export_materials as em
importlib.reload(em)

CORE = PrismInit.pcore

export_single = True
from_selected = False
export_all = False

CURRENT_PATH = CORE.getCurrentFileName()
CHECK_CONTEXT = em.get_current_context(filepath=CURRENT_PATH, shot=True)

def import_single_proxy():
    selection = mc.ls(sl=True)

    if len(selection) == 0:
        mc.warning("Cannot apply shaders to nothing. Please select a vrayproxy for export")
        return

    if len(selection) != 1:
        mc.warning("Multiple objects selected. Only applying to first selection.")

    selection = selection[0]
    filename = em.get_alembic_filename(selection)
    proxy = em.get_proxy_from_selection(selection)[0]
    asset = filename.split("Export/")[1].split("/", 1)[0]
    look_dir = f"{CORE.projectPath}03_Production\\Assets\\Characters\\{asset}\\Look"
    look_file = f"{look_dir}\\{asset}_look.ma"
    assignment_file = f"{look_dir}\\assignment.xml"
    apply_file = f"{look_dir}\\assignment_apply.xml"

    em.apply_shaders(look_file, assignment_file, proxy, filename)

if CHECK_CONTEXT:
    if export_single:
        import_single_proxy()
    
    if export_all:
        # add export all func
        pass