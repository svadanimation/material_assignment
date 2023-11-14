import vray.aetemplates.AEVRayProxyTemplate as vrayIO
import maya.cmds as mc
import importlib
import sys
import os
import PrismInit
from material_assignment import export_materials as em

core = PrismInit.pcore


def proxy_export_single():
    if not em.get_current_context():
        return

    if len(mc.ls(sl=True)) == 0:
        mc.warning("Cannot export nothing. Please select a vrayproxy for export")
        return

    if not len(mc.ls(sl=True)) == 1:
        mc.warning("Multiple objects selected. Only exporting first selection.")
        
    proxy = em.get_proxy_from_selection(mc.ls(sl=True))[0]
    materials = em.connected_materials(proxy)

    asset = core.getCurrentFileName().split("Characters\\")[1].split("\\", 1)[0]
    look_dir = f"{core.projectPath}03_Production\\Assets\\Characters\\{asset}\\Look"
    look_file = f"{look_dir}\\look.ma"
    assignment_file = f"{look_dir}\\assignment.xml"

    em.export_shaders(look_file, assignment_file, proxy)

def proxy_export_all():
    if not em.get_current_context():
        return

    proxy_list = mc.ls(type='VRayProxy')

    for proxy in proxy_list:
        materials = em.connected_materials(proxy)
        asset = mc.getAttr(f"{proxy}.fileName").split("Characters/")[1].split("/", 1)[0]
        print(asset)
        look_dir = f"{core.projectPath}03_Production\\Assets\\Characters\\{asset}\\Look"
        look_file = f"{look_dir}\\{asset}_look.ma"
        assignment_file = f"{look_dir}\\assignment.xml"
        em.export_shaders(look_file, assignment_file, proxy)

if __name__ == '__main__':
    # placeholders to be determined by user
    export_single = False
    from_selected = False
    export_all = True

    if export_single:
        proxy_export_single()
    
    elif from_selected:
        pass
        # add from selected func

    elif export_all:
        proxy_export_all()
    