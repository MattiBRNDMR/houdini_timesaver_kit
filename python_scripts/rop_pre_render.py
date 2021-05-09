import hou
import os

#this will setup several things before the cache starts, e.g checks if path already exists (prevent overriding caches), alter path if cache is just a static frame


#fetch this rop node
node = hou.node(".")


#fetch output path template and modify without hardcoding
path_raw_sequence = node.parm("path_sequence").rawValue()
false_path_sequence = path_raw_sequence.replace("""v`padzero(3, chs("version"))`""","""v`padzero(3, chs("version"))`_WRONG""")

path_raw_static = node.parm("path_static").rawValue()
false_path_static = path_raw_static.replace("""v`padzero(3, chs("version"))`""","""v`padzero(3, chs("version"))`_WRONG""")

#check whether its a sequence or a single frame to be cached

####IF SEQUENCE#######
if node.parm("static_cache").eval() == 0:   

    #switch render frame range to range
    node.parm("trange").set("normal")   
    
    #store original pass
    path_orig_seq = path_raw_sequence

    #reset original path    
    node.parm("sopoutput").set(path_orig_seq)

    #check if path already exists on disk
    path = node.parm("sopoutput").eval()
    check_path = os.path.exists(path)

    #if path exists
    if check_path == True:  
         
        create_false_path = false_path_sequence        
        node.parm("sopoutput").set(create_false_path) 
        notify = hou.ui.displayConfirmation("Caching directory already exists, this cache will be stored in a folder with _WRONG postfix. Fix your shit!")

    #if path does not already exists
    else:         
        print(str(node) + " is caching.. .. .. ..")


#####IF STATIC CACHE########'
else:

    #switch render frame range to single
    node.parm("trange").set("off") 

    #store original pass
    path_orig_static = path_raw_static

    #reset original path    
    node.parm("sopoutput").set(path_orig_static)

    #check if path already exists on disk
    path = node.parm("sopoutput").eval()
    check_path = os.path.exists(path)

    #if path exists
    if check_path == True:
        create_false_path = false_path_static
        node.parm("sopoutput").set(create_false_path) 
        notify = hou.ui.displayConfirmation("Caching directory already exists, this cache will be stored in a folder with _WRONG postfix. Fix your shit!")

    else:      
        print(str(node) + " is caching.. .. .. ..")
    
    
