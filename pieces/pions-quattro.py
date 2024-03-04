import bpy

#### efface le cube présent par défaut
bpy.ops.object.material_slot_add()
Cube = bpy.data.objects["Cube"]
print(dir(Cube))
Cube.select=True
bpy.ops.object.delete()

#### Crée deux matéraux, un blanc, un gris
couleurs = {"vert" : (0,255,0), "rouge" : (255,0,0)}
materiaux = {}
for col in couleurs:
    NEW_MATERIAL = bpy.data.materials.new(name=col)
    NEW_MATERIAL.diffuse_color = couleurs[col]
    materiaux[col]=NEW_MATERIAL

### Crée deux échelles
echelles={"grand" : (1,1,1.4), "petit" : (1,1,0.8)}


createfuncs={
    "cube": bpy.ops.mesh.primitive_cube_add,
    "cylinder": bpy.ops.mesh.primitive_cylinder_add,
}

for k in createfuncs:
    for col in couleurs:
        for creux in "plein", "vide":
            for taille in echelles:
                ## crée un objet
                createfuncs[k]()
                obj=bpy.context.object
                obj.name=k
                ## met une couleur
                obj.active_material = materiaux[col]
                ## creuse l'objet éventuellement
                if creux=="vide":
                    createfuncs[k]()
                    obj1=bpy.context.object
                    obj1.scale=(0.8,0.8,2)
                    mod_bool = obj.modifiers.new('my_bool_mod', 'BOOLEAN')
                    mod_bool.operation = 'DIFFERENCE'
                    mod_bool.object = obj1
                    bpy.context.scene.objects.active = obj
                    res = bpy.ops.object.modifier_apply(modifier = 'my_bool_mod')
                    obj1.select=True
                    bpy.ops.object.delete()
                ## change la taille
                obj.scale=echelles[taille]
                ## dessine l'objet
                bpy.data.scenes['Scene'].render.filepath = f'image-{taille}-{obj.name}-{creux}-{col}.png'                
                bpy.ops.render.render( write_still=True )
                obj.select=True
                bpy.ops.object.delete()
