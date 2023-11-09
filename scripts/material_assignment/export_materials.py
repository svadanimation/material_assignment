# builtins
import os
import xml.etree.ElementTree as etree
import alembic

# maya
import maya.cmds as mc

# prism
import PrismInit

# vray
import vray.aetemplates.AEVRayProxyTemplate as vrayIO

PLUGINS = ['vrayformaya']
CORE = PrismInit.pcore

def import_proxy(filepath, name):
    pass

def apply():
    # list all sel vray proxies in scene
    # for each proxy
        # figure out file paths
        # or get it from reference node
        # apply_shaders()
    pass

def export():
    # list all vray proxies in scene
    # for each proxy
        # figure out file paths
        # or get it from reference node
        #export_shaders()
    pass

def export_shaders(shader_filepath, assignment_filepath, vray_proxy):
    """
    Exports shaders and assignment xml for vray
    """
    if not plugin_check(PLUGINS):
        print("NOPE")
        return False
    
    # ensure object is VRayProxy
    if (not mc.objExists(vray_proxy) 
        or not mc.objectType(vray_proxy) == 'VRayProxy'):
        print (f'{vray_proxy} is not a VRayProxy')
        print("NOPE")
        return False
    
    shaders = connected_materials(vray_proxy)
    if not shaders:
        return False
    
    write_shaders(shaders, shader_filepath)
    write_assignments(vray_proxy, assignment_filepath)



def apply_shaders(shader_filepath, assignment_filepath, vray_proxy, filename, name=''):
    if not plugin_check(PLUGINS):
        return False

    if (not os.path.isfile(shader_filepath) 
        or not os.path.isfile(assignment_filepath)):
        mc.warning(f'Could not find shader or assignment file')
        return False
    
    # ensure object is VRayProxy
    # TODO split this to its own function
    # take an asset name as input
    if (not mc.objExists(vray_proxy) 
        or not mc.objectType(vray_proxy) == 'VRayProxy'):
        print (f'{vray_proxy} is not a VRayProxy')
        return False

    # failover to name if not explicitly set
    if not name:
        name = os.path.basename(shader_filepath).split('.')[0]

    # derive reference name
    reference_name = name + 'RN'

    # refresh reference
    if mc.objExists(reference_name):
        if mc.referenceQuery( reference_name,filename=True ) == shader_filepath:
                mc.file(shader_filepath, loadReference=reference_name)
    else:
        # import reference
        mc.file(shader_filepath, 
                r=True, 
                type='mayaAscii', 
                ignoreVersion=True, 
                namespace=name, 
                options='v=0')

    cache_namespace = abc_base_namespace(filename)
    shader_namespace = mc.referenceQuery(reference_name, namespace=True)

    if not all([cache_namespace, shader_namespace]):
        cache_namespace = shader_namespace = ':'


    assignment_filepath = parse_xml_namespace(assignment_filepath, 
                                              cache_namespace, 
                                              shader_namespace) 

    # import and apply assignments
    vrayIO.vrayImportProxyRules(vray_proxy,  assignment_filepath)

def parse_xml_namespace(filepath: str, 
                        pattern_namespace = ':',
                        scene_material_namespace = ':') -> str:
    # TODO file validation if it hasn't already happened
    p, ext = os.path.splitext(filepath)
    print(p, ext)
    out_filepath = os.path.join(f"{p}_apply{ext}")
    print(out_filepath)
    # Load the XML file
    tree = etree.parse(filepath)
    root = tree.getroot()

    # Find all occurrences of <pattern> and <sceneMaterial> and modify their text
    for pattern_rule in root.findall(".//patternRule"):
        pattern_element = pattern_rule.find("pattern")
        scene_material_element = pattern_rule.find("sceneMaterial")

        if pattern_element is not None:
            pattern_element.text = pattern_element.text[:-2].replace('/', f'{pattern_namespace}:') + '/*'

        if scene_material_element is not None:
            scene_material_element.text = f"{scene_material_namespace}:{scene_material_element.text.split(':')[-1]}"

    # Save the modified XML back to a file
    tree.write(out_filepath)
    if not os.path.isfile(out_filepath):
        print(f'Error writing file {out_filepath}')
        return filepath
    
    return out_filepath


def write_assignments(vray_proxy, filepath):
       # ensure filepath is valid
    file_dir = filepath.rsplit('\\', 1)[0]
    if not writable_filepath(file_dir):
        return False
    
    vrayIO.vrayExportProxyRules(vray_proxy, filepath)

def write_shaders(shaders, filepath):
    # store selection
    selection = mc.ls(sl=True)

    # ensure filepath is valid
    file_dir = filepath.rsplit('\\', 1)[0]
    if not writable_filepath(file_dir):
        return False

    #export shaders
    mc.select(list(shaders), r=True, ne=True)
    mc.file(filepath, force=True, options='v=0;', preserveReferences=False, type='mayaAscii', es=True)

    # reset selection
    mc.select(selection, r=True, ne=True)


def writable_filepath(filepath):
    if os.path.isdir(filepath):
        print(f"{filepath} is a valid path.")
        return True

    return False
    # try:
    #     with open(os.path.dirname(filepath), 'x') as tempfile: # OSError if file exists or is invalid
    #         pass
    # except OSError:
    #     # handle error here
    #     return False
    
    # return True

def connected_materials(vray_proxy):
    """
    Returns a list of shaders connected to the vray proxy
    """
    # get the proxy node
    # get the connected shaders
    # return the list of shaders
    
    # ensure object is VRayProxy
    if not mc.objectType(vray_proxy) == 'VRayProxy':
        print (f'{vray_proxy} is not a VRayProxy')
        return False
    
    # get the proxy node
    materials = mc.listConnections(f'{vray_proxy}.shaders')
    shading_groups = []
    for material in materials: 
        shading_groups.append(mc.listConnections(material, type='shadingEngine')[0])
    
    return shading_groups

def plugin_check(plugins = []):
    """
    Ensure that maya plugins are loaded
    """
    # check each plugin name
    # if not loaded, load it
    # return True if all plugins are loaded

    if not plugins:
        print (f'No plugins to check')
        return False
    
    for plugin in plugins:
        if not mc.pluginInfo(plugin, q=True, loaded=True):
            try:
                mc.loadPlugin(plugin)
            except:
                print (f'Failed to load plugin {plugin}')
                return False
            
    return True

def get_proxy_from_selection(selection):
    proxy_list = []
    selection = selection if isinstance(selection, list) else [selection] 
    for shape in selection:
        sel_shape = mc.listRelatives(shape, s=True)[0]
        if mc.objectType(sel_shape) == 'VRayProxy':
            proxy_list.append(sel_shape)    

    return proxy_list

def set_io_params():
    io_params = {
        "export_single":True,
        "from_selected":False,
        "export_all":False
    }

    export_single = mc.confirmDialog(
    m="Export shaders from selected Proxy?", 
    b=["Yes", "No"], 
    cb="No", 
    db="No"
    )

def get_current_context(filepath = '', shot=False):
    context_passed = True

    if filepath == 'unknown':
        mc.error("Context is unknown. Export aborted.")
        context_passed = False
        return context_passed

    if shot:
        # ref_path = mc.referenceQuery(mc.ls(sl=True)[0], filename=True)
        try:
            # asset = ref_path.split("Export/")[1].split("/", 1)[0]
            # asset = filepath.split("Export/")[1].split("/", 1)[0]
            path = f"{CORE.projectPath}\\03_Production\\Shots"
        except:
            mc.error("Not in proper context. Please move to Shot context.")
            context_passed = True
            return context_passed

    if not shot:
        try:
            asset = filepath.split("Characters\\")[1].split("\\", 1)[0]
        except:
            mc.error("Not in proper context. Please move to Look or Light.")
            return

        look_dir = f"{CORE.projectPath}\\03_Production\\Assets\\Characters\\{asset}\\Look"
        light_dir = f"{CORE.projectPath}\\03_Production\\Assets\\Characters\\{asset}\\Light"
        
        if not os.path.isdir(look_dir) or not os.path.isdir(look_dir):
            context_passed = False

    return context_passed

def get_alembic_filename(selection):
    cur_sel = selection
    sel_shape = mc.listRelatives(cur_sel, s=True)[0]
    filename = mc.getAttr(f"{cur_sel}.fileName")

    return filename

def get_asset_from_reference(selection):
    ref_path = mc.referenceQuery(selection, f=True)
    asset = ref_path.split('Export/')[1].split('/')[0]
    print(ref_path)
    print(asset)


def import_vray_proxy(alembic='', dir='', load_type=0):

    if not alembic.endswith(".abc"):
        mc.warning("File is not an alembic. Import cancelled.")
        return

    if not dir.endswith(".abc"):
        mc.warning("Path is not pointing to an alembic. Import cancelled.")
        return

    mc.vrayCreateProxy(
        node=alembic, 
        existing=True, 
        dir=dir,
        createProxyNode=True, 
        geomToLoad=load_type, 
        animType=3, 
        startFrame=1000, 
        endFrame=1100,
        newProxyNode=True
    )

def abc_base_namespace(filename):

    filename = str(filename)
    archive = alembic.Abc.IArchive(filename)
    root = archive.getTop()

    iterator = list(root.children)

    for obj in iterator:
        
        base_name = (obj.getFullName())
        
        if base_name:
            base_name = base_name.rsplit(':', 1)[0]
            return base_name
        
    return False
