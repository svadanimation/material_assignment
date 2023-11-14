import sys
import os
import importlib

import maya.cmds as mc

import vray.aetemplates.AEVRayProxyTemplate as vrayIO
import PrismInit
from material_assignment import export_materials_prism as em

core = PrismInit.pcore


def import_single_proxy():
    if not em.get_current_context(shot=True):
        return

    selection = mc.ls(sl=True)

    if len(selection) == 0:
        mc.warning("Cannot apply shaders to nothing. Please select a vrayproxy for export")
        return

    if len(selection) != 1:
        mc.warning("Multiple objects selected. Only applying to first selection.")

    selection = selection[0]
    proxy = em.get_proxy_from_selection(selection)[0]
    
    abc_filename = em.get_alembic_filename(selection)
    if not abc_filename or not os.path.isfile(abc_filename):
        print (f'{abc_filename}  on {selection} is not a valid abc path')
        return False
        
    asset = abc_filename.split("Export/")[1].split("/", 1)[0]

    look_dir = f"{core.projectPath}03_Production\\Assets\\Characters\\{asset}\\Look"
    look_file = f"{look_dir}\\{asset}_look.ma"
    assignment_file = f"{look_dir}\\assignment.xml"
    apply_file = f"{look_dir}\\assignment_apply.xml"

    em.apply_shaders(look_file, assignment_file, proxy)

if __name__ == '__main__':
    export_single = True
    from_selected = False
    export_all = False

    if em.get_current_context(shot=True):
        if export_single:
            import_single_proxy()
        
        if export_all:
            # add export all func
            pass