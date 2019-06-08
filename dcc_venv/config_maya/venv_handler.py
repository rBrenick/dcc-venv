import os

import logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(" maya-venv  ")



def get_mod_file_path():
    """
    :return: C:/Users/USERNAME/Documents/maya/modules/dcc-venv-maya.mod
    """
    user_documents_folder = os.path.expanduser('~')
    
    if "documents" not in user_documents_folder.lower():  # Standalone interpreter goes to username folder not documents
        user_documents_folder += "/Documents"
        
    mod_path = os.path.join(user_documents_folder, "maya", "modules", "dcc-venv-maya.mod").replace("\\", "/")
    
    return mod_path

    
def ensure_dir_file_path(file_path):
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))
    
    

def install(venv_path, *args, **kwargs):
    
    # Startup Script
    venv_startup_script_path = os.path.join(venv_path, "Lib", "site-packages", "dcc_venv_startup.py").replace("\\", "/")
    startup_script_content = 'import runpy; runpy.run_path("{}", run_name="__startup__")'.format(venv_startup_script_path)
    
    venv_mod_path = os.path.join(venv_path, "_module_path")
    startup_script_path = os.path.join(venv_mod_path, "scripts", "userSetup.py").replace("\\", "/")
    
    # Write userSetup.py 
    ensure_dir_file_path(startup_script_path)
    with open(startup_script_path, "w") as fp:
        fp.write(startup_script_content)
        
    
    
    # Make .mod file in user documents pointing to venv_mod_path
    mod_path = get_mod_file_path()
    
    log.info("Creating: {}".format(mod_path))
    
    # Safety create folders
    ensure_dir_file_path(mod_path)
    with open(mod_path, "w") as fp:
        fp.write("+ dcc-venv 1.0 {}".format(venv_mod_path))
        
    log.info("Created: {}".format(mod_path))
    
    
    


def uninstall(*args, **kwargs):
    mod_path = get_mod_file_path()
    if os.path.exists(mod_path):
        log.info("Removing: {}".format(mod_path))
        os.remove(mod_path)





