def object_merge_nodes():

    ctrl_click = kwargs['ctrlclick'] or kwargs['cmdclick']
    
    print(ctrl_click)

    #fetch selected nodes
    nodes = hou.selectedNodes()
    amount = len(nodes)
    iter = 0
    totalnodes = [ ]
    
    for node in nodes:
        
        #fetch current nodes dir in scene and create object merge in same dir, also de-select nodes to be object-merged
        currNodeDir = node.node("..")
        currNodePath = node.path()
        node.setSelected(False)
        
        
        obj_merge = currNodeDir.createNode("object_merge", "GET_" + str(node).upper())
        
        #fill out objmerges parms, for multiple objmerges create space between the nodes, also select new objmerge nodes to copy to clipboard
        if ctrl_click == False:
            rel_path = "../" + node.name()
            obj_merge.parm("objpath1").set(rel_path)
            
        else: 
            obj_merge.parm("objpath1").set(currNodePath)
            
        obj_merge.parm("xformtype").set(1)
        obj_merge.setColor(hou.Color((0,0.5,1)))
        obj_merge.move([iter*2, 0])
        
        obj_merge.setSelected(True)
        
        
        iter += 1
        
    #copy new nodes to clipboard
    newNodes = hou.selectedNodes()
    hou.copyNodesToClipboard(newNodes)
    
    #delete new nodes from the scene to only keep the ones on the clipboard
    for x in newNodes:
        x.destroy()
    
    
object_merge_nodes()
