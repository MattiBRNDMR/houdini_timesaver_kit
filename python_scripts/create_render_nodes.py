import hou

def create_render_nodes():
    #get global variables
    target_node = hou.selectedNodes()
    scene_root = hou.node("/obj")
    
    #create render node for each selected node
    for node in target_node:
        #variables per node 
        target_node_path = node.path()
        prims = hou.node(target_node_path).geometry().prims()
        points = hou.node(target_node_path).geometry().points()
        
        #check geometry type
        
        if len(prims) == len(points): #if geo is volume
            
            print "render node for " + str(node) + " contains volume data"
            #ask for render node name
            render_node_name = hou.ui.readInput("Rendernode name for " + str(node), buttons=("Create", "Cancel"))
            
            
            #if volume, get path to file (read from filecache)
            path_to_volume_cache_node = hou.ui.selectNode(initial_node = hou.node(target_node_path), title="filecache for this volume")
            
            check_filecache = hou.node(path_to_volume_cache_node).type().name()
            #check if its filecache or ropoutput
            if check_filecache == "filecache":
                print "its a filecache"
                path_to_volume = hou.node(path_to_volume_cache_node).parm("file").rawValue()
                path_to_volume_abs = path_to_volume.replace("$OS", str(hou.node(path_to_volume_cache_node).name()))
                #print path_to_volume_abs
             
            if check_filecache == "rop_geometry":
                print "its a ropgeo"
                path_to_volume = hou.node(path_to_volume_cache_node).parm("sopoutput").rawValue()
                path_to_volume_abs = path_to_volume.replace("$OS", str(hou.node(path_to_volume_cache_node).name()))
                #print path_to_volume_abs
            
            
            #if button create was clicked
            if render_node_name[0] == 0:
                render_node = scene_root.createNode("matti_render_volumes", "RENDER_VOLUME_" + render_node_name[1].replace(" ", "_"))
                render_node.setColor(hou.Color((1.0,0.0,0.0)))
                render_node.parm("file").set(path_to_volume_abs)
                
                
                
        else:
    
            if len(prims) and len(points) > 0: #if geo is solid (has polys)
               
                print "render node for " + str(node) + " contains polygon data"
                #get render node name
                render_node_name = hou.ui.readInput("Rendernode name for " + str(node), buttons=("Create", "Cancel"))
                
                #when button create has been clicked, create render_geo hda and write the path to the selected node into object merge
                if render_node_name[0] == 0:
                    render_node = scene_root.createNode("render_geo", "RENDER_GEOMETRY_" + render_node_name[1].replace(" ", "_"))
                    render_node.setColor(hou.Color((1.0,0.0,0.0)))
                    render_node.parm("objpath").set(target_node_path)
                
            
            
            
            else:
        
                if len(prims) == 0 and len(points) > 0: #if geo is points (particles)
                    
                    print "render node for " + str(node) + " contains point data"
                    render_node_name = hou.ui.readInput("Rendernode name for " + str(node), buttons=("Create", "Cancel"))
                
                     #when button create has been clicked, create render_geo hda and write the path to the selected node into object merge
                    if render_node_name[0] == 0:
                       render_node = scene_root.createNode("matti_render_particles", "RENDER_PARTICLES_" + render_node_name[1].replace(" ", "_"))
                       render_node.setColor(hou.Color((1.0,0.0,0.0)))
                       render_node.parm("objpath1").set(target_node_path)
        
        
        
            
       
    
    
create_render_nodes()
