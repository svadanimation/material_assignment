"""This module will reload all of the modules in the order in which
they need to be reloaded. This way we can quickly iterate and
not have files contain reloads in them."""

# COMPATABILITY
import sys
import os
from importlib import reload

print('Reloading modules ...')


ROOT_PATH = os.path.abspath("../scripts")
PLUGIN_PATH = os.path.abspath("../plug-ins")
PACKAGE = 'material_assignment'

if ROOT_PATH not in sys.path:
    sys.path.insert(0, ROOT_PATH)

if PLUGIN_PATH not in sys.path:
    sys.path.insert(0, PLUGIN_PATH)

# Get the name of the current package
# if __name__ == '__main__':
#     current_package = PACKAGE
# else:
#     current_package = __name__.rpartition('.')[0]

# This test suite runs outside the main module,
# so we need to hardcode the package name
current_package = PACKAGE

# Reloads
from material_assignment import shader_export_standalone
from material_assignment import shader_import_standalone

# base package
import material_assignment
reload(material_assignment)

# Iterate over the modules in sys.modules with the same package name
success = True
for module_name in list(sys.modules.keys()):
    if module_name.startswith(current_package + '.'):

        # Reload the module using the importlib.reload() function
        try:
            reload(sys.modules[module_name])
            print(f'Module {module_name} has been reloaded...')
        except Exception as exc:
            success = False
            print(f'Module {module_name} FAILED reload...')

if success:
    print(f'SUCCESS: All modules in package {current_package} have been reloaded.')
else:
    print('FAILURE: Some modules in package {current_package} have failed to reload.')