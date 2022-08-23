def create_out_nodes():
   
    #get nodes
    nodes = hou.selectedNodes()
    prefix = "OUT_"
  
    
    for node in nodes:
    
        #check for multiple node outputs
        outputs = node.outputLabels()
        
        amt_outputs = len(outputs)
        
        if amt_outputs > 1:
            
            for output in outputs:
                
                #query each nodes output and ask for it's out null name
                output_null_name = hou.ui.readInput("Name for Output OUT-Null after:" + " " + str(output), buttons=("Create", "Cancel"))
                
                #if "create" was clicked
                if output_null_name[0] == 0:
                    
                    #create output null node, add underscores and capitalize the name, add black color to out null
                    output_index = outputs.index(output)
                    offset = 2.0 * ( float(output_index) - 1.0 )
                    parent_pos = node.position()
                    output_out_null = node.node("..").createNode("null", prefix + output_null_name[1].replace(" ", "_").upper())
                    output_out_null.setPosition(parent_pos)
                    output_out_null.setColor(hou.Color((0,0,0)))
                    output_out_null.move(hou.Vector2(offset, -1.5))
                    output_out_null.setInput(0, node, output_index)
                         
        
        else:    
            
            
            #query each selected node with one output and ask for it's out null name
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
