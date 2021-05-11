import hou
import os
import json
from datetime import datetime as dt

#setup ROOT, PROJECT and SHOT env, save it as json, save current version and version history in json, save scene-up time in json to monitor time spent#

def setup_project():
    #get project name, root dir and shot name
    
    #set root dir
    home_dir = hou.getenv("HOME")
    houdini_proj_dir = home_dir + "/houdini_projects"
    root = hou.ui.selectFile(start_directory=houdini_proj_dir, title="Select Root Directory", file_type=hou.fileType.Directory)
    
    #check if root dir is being seen as relative path and abort in that case
    if root[0] == "$":
        print("please dive into the root folder and not just select it")
        hou.ui.displayConfirmation("Please dive into the root folder and not just select it")
        return
    else:
        #get project name
        project = hou.ui.readInput("Project Name", buttons=("Create", "Cancel"))
        
        #get shot name
        shot = hou.ui.readInput("Shot Name", buttons=("Create", "Cancel"))
        
        #setup hip name and pathing
        version = 1
        hip_name = shot[1].replace(" ", "_") + "_fx_v" + str(version).zfill(3)
        shot_name = shot[1]
        project_name = project[1]
        
        print("root dir: " + root)
        print("project dir: " + root + project[1] + "/")
        print("project name: " + project[1])
        print("hip name: " + hip_name)
        
        #check if path already exists (meaning: project already exists)
        project_path = root + project[1]
        check_path = os.path.exists(project_path)
        
        
        
        #ADD SHOT TO EXISTING PROJECT#
        #if path exists, skip folder creation and further setup
        if check_path == True:
            #TO DO: check if shot already exists to prevent human error
        
            hou.ui.displayConfirmation("Project has been created previouvsly, shot will be added")
            print("project exists but shot will be added")
        
        #CREATE NEW PROJECT AND INITIALIZE FIST SHOT#
        #if path does not exist, create folder structure
        else:
        
            folders = ["import", "geo", "scenefiles", "flipbooks", "_metadata_", "export", "hda", "scripts"]
        
            create_proj_folder = os.mkdir(project_path)
            for folder in folders:
                create_folders = os.mkdir(project_path + "/" + folder)
            
            subfolder_scenefiles = os.mkdir(project_path + "/" + "scenefiles" + "/" + "deprecated")   
            
            
            
            #setup json files for project specific information and per shot json
            
            #PROJECT JSON#
           
            #ask for additional information           
            artist = hou.ui.readInput("Artist Name", buttons=("Confirm", "Cancel"))
            artist_name = artist[1].capitalize()
            company = hou.ui.readInput("Company Name", buttons=("Confirm", "Cancel"))
            company_name = company[1].capitalize()
            client = hou.ui.readInput("Client Name", buttons=("Confirm", "Cancel"))
            client_name = client[1].capitalize()
            
            #setup array of dictionaries storing information
            metadata_project = { }
            
            metadata_project["project_information"] = [ ]
            metadata_project["project_information"].append({
            
                "project_name" : project_name,
                "working_artist" : artist_name,
                "company_in_charge" : company_name,
                "client" : client_name,
                "current_shots" : "1",
            
            
            
            })
            
            metadata_project["shot_list_and_status"] = [ ]
            metadata_project["shot_list_and_status"].append({
                
                "shot_name" : shot_name,
                "status" : "in progress",
            
            
            })
            
            #json creation variables
            project_json = json.dumps(metadata_project, sort_keys=True, indent=4)
            project_json_extension = "PROJECT_INFO_" + project_name + ".json"
            
            #write project json
            project_json_file = open(project_path + "/_metadata_/" + project_json_extension, "w")
            project_json_file.write(project_json)
            project_json_file.close()
            
            
            
            
            #PER SHOT JSON#
            
            
            
            print("created new project and set up json files")
               
        
    
    
setup_project()



