

## Export

- Write a .ma file containing the linked shaders [export_shaders]
- Get the `{entity}_{product}_{version}`to determine export path, ie `03_Production\Assets\Characters\Junebug\Look\look.ma` and `..\assignments.ma`
- Extract prism naming `{entity}_{product}_{version}` for the above files
- Also publish a master to the same location

## Import
- Hook into prism as much as practical
- Add option to import state for `vrayProxy`
- https://docs.chaos.com/display/VMAYA/vrayCreateProxy
- Add option to `apply shaders`
    - Reference the .ma file which contains the shaders
    - Apply the assignment file [apply_shaders] 