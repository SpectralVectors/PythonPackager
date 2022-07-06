bl_info = {
    "name": "Python Packager",
    "author": "Spectral Vectors",
    "version": (0, 0, 2),
    "blender": (2, 90, 0),
    "location": "Edit > Preferences > Addons > PythonPackager",
    "description": "A tool to download extra Python packages to Blender's internal Python",
    "warning": "",
    "doc_url": "",
    "category": "Addons",
}

import bpy, subprocess, sys


class PythonPackagerOperator(bpy.types.Operator):
    """Tooltip"""
    
    bl_idname = "addon.pythonpackager_operator"
    bl_label = "Install Package"

    def execute(self, context):
        try:
            string = bpy.app.version_string
            blenderversion = string.rstrip(string[-2:])

            preferences = context.preferences
            addon_prefs = preferences.addons[__name__].preferences

            package = addon_prefs.PackageName

            subprocess.check_call([
                sys.executable, 
                "-m", "ensurepip"])

            subprocess.check_call([
                sys.executable, 
                "-m", "pip", "install", "--upgrade", "pip"])

            subprocess.check_call([
                sys.executable, 
                "-m", "pip", "install",
                f"--target=C:\\Program Files\\Blender Foundation\\Blender {blenderversion}\\{blenderversion}\\python\\lib", 
                package])
        except:
            bpy.ops.message.messagebox('INVOKE_DEFAULT')
        
        return {'FINISHED'}


class PythonPackagerPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    PackageName: bpy.props.StringProperty(
        name='Package',
        description='The name of the package as it appears in PyPI',
        default='',
    )

    def draw(self, context):    
        layout = self.layout
        box = layout.box()
        column = box.column()
        row = column.row()
        row.prop(self, 'PackageName')
        row.operator(PythonPackagerOperator.bl_idname)


class PythonPackagerMessageBox(bpy.types.Operator):
    bl_idname = "message.messagebox"
    bl_label = "Python Packager - Permission Error!"

    def execute(self, context):
        #print(self.message)
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width = 400)

    def draw(self, context):
        self.layout.label(text= "You must run Blender as Administrator to install Python Packages.")
        self.layout.label(text="Close, then reopen Blender by right-clicking and selecting 'Run as Administrator'")

classes = [
    PythonPackagerPreferences,
    PythonPackagerOperator,
    PythonPackagerMessageBox,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)