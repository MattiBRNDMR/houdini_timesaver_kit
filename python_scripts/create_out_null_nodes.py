def create_node():
    #check for selected nodes
    target_node = hou.selectedNodes()
    
    #create a null for every selected node
    for node in target_node:
    
    
        
        null_name = hou.ui.readInput("Name for OUT-Null after:" + " " + str(node), buttons=("Create", "Cancel"))
        
        
        
        #create nulls if "OK" has been clicked
        if null_name[0] == 0:
            node_parent_dir = node.node("..")
            #empty spaces will be replaced with underscores automaticly
            out_null = node_parent_dir.createNode("null", "OUT" + "_" + null_name[1].replace(" ", "_"))
            out_null.setNextInput(node)
            out_null.setPosition(node.position())
            out_null.move([0,-1])
            out_null.setColor(hou.Color((0,0,0)))
            node.setSelected(False)
            node.setDisplayFlag(False)
            node.setRenderFlag(False)
            out_null.setSelected(True)
            out_null.setDisplayFlag(True)
    
            
create_node()
