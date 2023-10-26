import maya.cmds as mc
import os

name = "ShaderIO"
classname = "ShaderIO"


class ShaderIO:
    def __init__(self, core):
        self.core = core
        self.version = "v2.0.0beta17.8"

        # register prePublish and preExport callbacks
        self.core.registerCallback("postImport", self.postImport, plugin=self)
        self.core.registerCallback("postPublish", self.postPublish, plugin=self)

    # importing funcs
    def postImport(self, *args, **kwargs):
        asset_path = kwargs["state"].getImportPath()
        import_proxy = "No"

        if os.path.splitext(asset_path)[1] == '.abc':
            asset_dir = asset_path.rsplit('\\', 1)[0]
            print(asset_dir)

            # os.chdir("..\\..\\..\\..\\..\\..\\Assets\\Characters\\Look")
            look_file = f"{os.getcwd()}\\look.ma"
            print(look_file)

            import_proxy = mc.confirmDialog(
                m="Import Proxy for selected Alembic?", 
                b=["Yes", "No"],
                cb="No", 
                db="No"
            )


        if import_proxy == "Yes":
            sel_shapes = []
            sel_transforms = mc.ls(sl=True)
            
            for sel in sel_transforms:
                sel_shape = mc.listRelatives(sel, s=True)
                sel_shapes.append(sel_shape)
                
            look_dir = f"{self.core.projectPath()}"

    def postPublish(self, *args, **kwargs):
        export_shaders = "No"
        export_shaders = mc.confirmDialog(
            m="Export shaders from selected Proxy?", 
            b=["Yes", "No"], 
            cb="No", 
            db="No"
        )


        if export_shaders == "Yes":
            sel_transforms = mc.ls(sl=True)
            sel_shapes = [mc.listRelatives(sel, s=True)[0] for sel in sel_transforms]
            mc.file("D:\\look.ma", force=True, options='v=0', preserveReferences=False, type='mayaAscii', es=True)

            for sel in sel_transforms:
                look_dir = f"{self.core.projectPath()}\\03_Production\\Assets\\Characters\\{sel}\\Look"

            import_as_vray_proxy()        
            
    def import_as_vray_proxy(self, asset, look_file):
        pass
        
def import_as_vray_proxy(asset='', look_file=''):
    self.core.getProjectPath()
    alembic_dir = "P:\\Glasses\\03_Production\\Shots\\010\\010\\Export\\Animation\\master\\010-010_Animation_master.abc"
    alembic_file = '010-010_Animation_master.abc'

    # mc.vrayCreateProxy(
    #     node=alembic_file, 
    #     existing=True, 
    #     dir=alembic_dir,
    #     createProxyNode=True, 
    #     geomToLoad=2, 
    #     animType=3, 
    #     startFrame=1000, 
    #     endFrame=1100,
    #     newProxyNode=True
    # )