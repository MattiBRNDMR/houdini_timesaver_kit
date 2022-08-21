def create_out_nodes():
   
    #get nodes
    nodes = hou.selectedNodes()
    prefix = "OUT_"
  
    
    for node in nodes:
    
        
        #query each selected node and ask for it's out null name
        null_name = hou.ui.readInput("Name for OUT-Null after:" + " " + str(node), buttons=("Create", "Cancel"))
        
        #if "create" was clicked
        if null_name[0] == 0:
            
            #create null node, add underscores and capitalize the name, add black color to out null
            out_null = node.createOutputNode("null", prefix + null_name[1].replace(" ", "_").upper())
            out_null.setColor(hou.Color((0,0,0)))
            out_null.move(hou.Vector2(0.0, -1.0))
           
    
        
        #if "cancel" was clicked    
        else: 
            
            exit()
        
        
        
create_out_nodes()
