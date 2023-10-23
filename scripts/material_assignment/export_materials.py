# builtins
import os

# maya
import maya.cmds as mc

PLUGINS = ['vrayformaya']

def import_proxy(filepath, name):
    pass

def apply():
    # list all vray proxies in scene
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
        return False
    
    # ensure object is VRayProxy
    if (not mc.objExists(vray_proxy) 
        or not mc.objectType(vray_proxy) == 'VRayProxy'):
        print (f'{vray_proxy} is not a VRayProxy')
        return False
    
    shaders = connected_materials(vray_proxy)
    if not shaders:
        return False
    
    write_shaders(shaders, shader_filepath)
    write_assignments(vray_proxy, assignment_filepath)



def apply_shaders(shader_filepath, assignment_filepath, vray_proxy, name=''):
    if not plugin_check(PLUGINS):
        return False

    if (not os.path.isfile(shader_filepath) 
        or not os.path.isfile(assignment_filepath)):
        mc.warning(f'Could not find shader or assignment file')
        return False
    
    # ensure object is VRayProxy
    if (not mc.objExists(vray_proxy) 
        or not mc.objectType(vray_proxy) == 'VRayProxy'):
        print (f'{vray_proxy} is not a VRayProxy')
        return False

    # failover to name if not explicitly set
    if not name:
        name = os.path.basename(assignment_filepath).split('.')[0]

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

    # import and apply assignments
    mc.vrayImportProxyRules(vray_proxy,  assignment_filepath)


def write_assignments(vray_proxy, filepath):
       # ensure filepath is valid
    if not writable_filepath(filepath):
        return False
    
    mc.vrayExportProxyRules(vray_proxy, filepath)

def write_shaders(shaders, filepath):
    # store selection
    selection = mc.ls(sl=True)

    # ensure filepath is valid
    if not writable_filepath(filepath):
        return False

    #export shaders
    mc.select(list(shaders), r=True, ne=True)
    mc.file(filepath, force=True, options='v=0;', preserveReferences=False, type='mayaAscii', es=True)
    
    # reset selection
    mc.select(selection, r=True, ne=True)


def writable_filepath(filepath):
    try:
        with open(os.dirname(filepath), 'x') as tempfile: # OSError if file exists or is invalid
            pass
    except OSError:
        # handle error here
        return False
    
    return True

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
        shading_groups.append(mc.listConnections(material, type='shadingEngine'))
    
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