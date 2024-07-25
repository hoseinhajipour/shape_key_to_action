bl_info = {
    "name": "Shape Key to Action",
    "blender": (4, 2, 0),
    "category": "Object",
    "description": "Create actions for each shape key"
}

import bpy

class ShapeKeyToActionOperator(bpy.types.Operator):
    bl_idname = "object.shape_key_to_action"
    bl_label = "Shape Key to Action"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.object
        if obj is None or obj.type != 'MESH' or not obj.data.shape_keys:
            self.report({'ERROR'}, "Selected object must be a mesh with shape keys")
            return {'CANCELLED'}
        
        shape_keys = obj.data.shape_keys.key_blocks

        if obj.animation_data is None:
            obj.animation_data_create()
        
        for shape_key in shape_keys:
            action_name = f"{obj.name}_{shape_key.name}_Action"
            action = bpy.data.actions.new(name=action_name)
            
            data_path = f'key_blocks["{shape_key.name}"].value'
            fcurve = action.fcurves.new(data_path=data_path)

            fcurve.keyframe_points.add(count=1)
            fcurve.keyframe_points[0].co = (0, 1.0)

            for keyframe in fcurve.keyframe_points:
                keyframe.interpolation = 'LINEAR'

            obj.animation_data.action = action
            bpy.context.scene.frame_set(0)
        
        return {'FINISHED'}

class ShapeKeyToActionPanel(bpy.types.Panel):
    bl_label = "Shape Keys to Actions"
    bl_idname = "OBJECT_PT_shape_keys_to_actions"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Shape Keys to Actions"

    def draw(self, context):
        layout = self.layout
        layout.operator(ShapeKeyToActionOperator.bl_idname, text="Create Actions for Shape Keys")

def register():
    bpy.utils.register_class(ShapeKeyToActionOperator)
    bpy.utils.register_class(ShapeKeyToActionPanel)

def unregister():
    bpy.utils.unregister_class(ShapeKeyToActionOperator)
    bpy.utils.unregister_class(ShapeKeyToActionPanel)

if __name__ == "__main__":
    register()
