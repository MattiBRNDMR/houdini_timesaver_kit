import hou

def create_cache_setup():

    #gather nodes to cache and ask for element name to cache
    target_node = hou.selectedNodes()
    
    for node in target_node:
    
        node_parent_dir = node.node("..")
       
        #print(node_parent_dir)
    
    
        element_name = hou.ui.readInput("Element To Cache:", buttons=("Create", "Cancel"))
        
        
        #when create button was pressed
        
        if element_name[0] == 0:
        
            #talk output to user
            print(element_name[1] + " has been set up for caching")
            
            #create rop output
            rop_name_raw = "WRITE_CACHE" + "_" + element_name[1].replace(" ", "_")
            rop_out = node_parent_dir.createNode("rop_geometry", rop_name_raw)
            
            #check if name already exists to prevent duplicates by comparing rop node name pre and post creation
            rop_name_post_create = rop_out.name()
            
            #if name is not identical (houdini adds a number to the name if it already exists) interrupt
            if rop_name_post_create != rop_name_raw:
                print("this cache name already exists, choose another one")
                exit_notification = hou.ui.displayConfirmation("This cache name is already taken, choose another one and keep it fucking organized you lazy piece of shit!")
                rop_out.destroy()
                return
                
            else:
                print("this cache name is not taken yet! Proceeding.. .. ..")
                
                rop_out.setNextInput(node)
                rop_out.setPosition(node.position())
                rop_out.move([0,-1.5])
                rop_out.setColor(hou.Color((1,0,0)))
                rop_out.parm("element_name").set("CACHE_" + element_name[1].replace(" ", "_"))
                
                #inteligently check given element name for data type 
                
                #keywords hinting voxel data
                keywords_vol = ["vol", "VOL", "volume", "VOLUME", "vdb", "VDB"]                
                
                #check for keywords in element name and set data type accordingly
                if any(word in element_name[1] for word in keywords_vol):
                    print("seems to be voxel data")
                    rop_out.parm("element_type").set("vdb")
                    
                else:
                    print("seems to be non voxel data")
                    rop_out.parm("element_type").set("bgeo.sc")
                    
                    
                
                #create file node to read back the cache
                
                file_in = node_parent_dir.createNode("file", "READ_CACHE" + "_" + element_name[1].replace(" ", "_"))
                #print(file_in)
                file_in.setPosition(rop_out.position())
                file_in.move([0,-1.5])
                file_in.setColor(hou.Color((1,0,0)))
                file_in.parm("missingframe").set("empty")
                
                #generate string to relative reference output rop's cache path in file node
                
                ref_path = """`chs("../{elem}/sopoutput")`""".format(elem="WRITE_CACHE" + "_" + element_name[1].replace(" ", "_"))
                #print(ref_path)
                file_in.parm("file").set(ref_path)
                
                
                
                #create timeshift
                
                timeshift = node_parent_dir.createNode("timeshift", "CLAMP_CACHE" + "_" + element_name[1].replace(" ", "_"))
                timeshift.setNextInput(file_in)
                timeshift.setPosition(file_in.position())
                timeshift.move([0,-1.5])
                timeshift.setColor(hou.Color((1,0,0)))
                timeshift.parm("frame").deleteAllKeyframes()
                timeshift.parm("frame").setExpression("$FF")
                timeshift.parm("rangeclamp").set("both")
                
                #link clamp range to rop's cache range
                
                timeshift.parm("frange1").deleteAllKeyframes()
                timeshift.parm("frange2").deleteAllKeyframes()
                
                frange1_link = """ch("../{elem}/f1")""".format(elem="WRITE_CACHE" + "_" + element_name[1].replace(" ", "_"))
                frange2_link = """ch("../{elem}/f2")""".format(elem="WRITE_CACHE" + "_" + element_name[1].replace(" ", "_"))
                
                timeshift.parm("frange1").setExpression(frange1_link)
                timeshift.parm("frange2").setExpression(frange2_link)
                
                ########setup pre and postrender scripts for rop for (hopefully) reducing human error########
                
                #pre render: check if folder already exists and notify user if thats the case
                
                pre_render = """execfile("$HIH/PIPELINE/rop_pre_render.py")"""
                rop_out.parm("prerender").set(pre_render)
                
                #post render: reload geo in file node to double check fetching the correct cache
                
                
                post_render = """import hou; node = hou.node("{filecache}"); node.parm("reload").pressButton(); print("v`padzero(3, chs("version"))` of {elem} was loaded");""".format(filecache = file_in.path(), elem = element_name[1])
                rop_out.parm("postrender").set(post_render)
                    
create_cache_setup()
