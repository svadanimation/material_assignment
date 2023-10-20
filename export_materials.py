import maya.cmds as mc

def export_shaders(shader_filepath, assignment_filepath, vray_proxy):
    """
    Exports shaders and assignment xml for vray
    """
    if not plugin_check(['vrayformaya']):
        return False
    
    shaders = connected_materials(vray_proxy)
    if not shaders:
        return False
    
    write_shaders(shaders, shader_filepath)
    write_assignments(vray_proxy, assignment_filepath)
    
    
def write_assignments(vray_proxy, filepath):
       # ensure filepath is valid
    if not validate_filepath(filepath):
        return False
    
    mc.vrayExportProxyRules(vray_proxy, filepath)

def write_shaders(shaders, filepath):
    # store selection
    selection = mc.ls(sl=True)

    # ensure filepath is valid
    if not validate_filepath(filepath):
        return False

    #export shaders
    mc.select(list(shaders), r=True, ne=True)
    mc.file(filepath, force=True, options='v=0;', preserveReferences=False, type='mayaAscii', es=True)
    
    # reset selection
    mc.select(selection, r=True, ne=True)

def validate_filepath(filepath):
    try:
        with open(filepath, 'x') as tempfile: # OSError if file exists or is invalid
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