"""
Test env for material assignment scripts
"""

from importlib import reload


RUN = False
EXPORT = False
GARBAGE = True
RELOAD_PLUGINS = True
REPO = r'Z:/junior_year/F23/collab/git_repos'
MODULE = 'material_assignment'
SCRIPTS = 'scripts'
DEPLOY = f'K:\\Animation\\Pipeline\\SVAD_2023\\maya\\apps\\{MODULE}\\scripts'

plugins = []

add = [
    os.path.join(REPO, MODULE, SCRIPTS),
    os.path.join(REPO, MODULE),
]

remove = [DEPLOY]


    
for path in remove:
    realpath = os.path.normpath(path)
    for i, real in enumerate(realpath):
        if path == real:
            actual_path = sys.path[i]
            print(f'Removed {actual_path} from sys.path')
            sys.path.remove(actual_path)


if GARBAGE:
    # brutal and ugly way to garbage collect old modules in the package
    mod_to_del = []
    for mod in sys.modules.keys():
        if mod.startswith(MODULE):
            mod_to_del.append(mod)
        
    for mod in mod_to_del:
        print(f'Deleting {mod} from sys.modules')
        del sys.modules[mod]
        del mod

print("Appending env")
realpaths = [os.path.normpath(p) for p in sys.path]
for path in add:
    if os.path.normpath(path) not in realpaths:
        print(f"Appending {path}")
        sys.path.append(path)
    else:
        print(f"Already in path: {path}")

# print("Appending env")
# for env in envs:
#     if env not in sys.path:
#         sys.path.append(os.path.expanduser(env))
#     else:
#         print(f"Already in path: {env}")

# Reloads
from test_dev import reload_modules

# The irony
reload(reload_modules)

if RELOAD_PLUGINS:
    # Unload plugins
    for plugin_path in plugins:
        try:
            mc.unloadPlugin(os.path.basename(plugin_path), force=True)
        except Exception as e:
            mc.warning(f"Error unloading: {plugin_path}. {e}")

# Load plugins
for plugin_path in plugins:
    try:
        mc.loadPlugin(plugin_path)
    except Exception as e:
        mc.warning(f"Error loading: {plugin_path}. {e}")


# finally, run the test
if RUN:
    from material_assignment import shader_import_standalone
    from material_assignment import shader_export_standalone

    if EXPORT:
            proxy_export_all()

    else:
        import_single_proxy()