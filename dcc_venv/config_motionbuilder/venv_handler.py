import os


import logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(" motionbuilder-venv ")



def ensure_dir_file_path(file_path):
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))



def get_mobu_startup_script_paths():
    """
    :return: C:/Users/USERNAME/Documents/maya/modules/dcc-venv-maya.mod
    """
    user_documents_folder = os.path.expanduser('~')
    
    if "documents" not in user_documents_folder.lower():  # Standalone interpreter goes to username folder not documents
        user_documents_folder += "/Documents"
    
    startup_paths = []
    mobu_root_folder = os.path.join(user_documents_folder, "MB")
    for mobu_version_number in os.listdir(mobu_root_folder):
        mobu_version_dir = os.path.join(mobu_root_folder, mobu_version_number)
        
        startup_script_path = os.path.join(mobu_version_dir, "config", "PythonStartup", "dcc-venv-mobu-startup.py").replace("\\", "/")
        startup_paths.append(startup_script_path)
    
    return startup_paths
    
    
    
def install(venv_path, *args, **kwargs):

    venv_startup_script_path = os.path.join(venv_path, "Lib", "site-packages", "dcc_venv_startup.py").replace("\\", "/")
    startup_script_content = 'import runpy; runpy.run_path("{}", run_name="__startup__")'.format(venv_startup_script_path)
    
    for startup_script_path in get_mobu_startup_script_paths():
    
        ensure_dir_file_path(startup_script_path)
        
        log.info("Creating {}".format(startup_script_path))
        with open(startup_script_path, "w") as fp:
            fp.write(startup_script_content)
    
    
    return True
 
 
def uninstall(*args, **kwargs):
    for startup_script_path in get_mobu_startup_script_paths():
        if os.path.exists(startup_script_path):
            log.info("Removing {}".format(startup_script_path))
            os.remove(startup_script_path)
            
    return True
