import os

import logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(" blender-venv  ")


    
def ensure_dir_file_path(file_path):
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))

        
def get_startup_script_paths():
    paths = []
    blender_versions_dir = os.path.join(os.getenv("APPDATA"), "Blender Foundation", "Blender")
    for version_folder in os.listdir(blender_versions_dir):
        startup_script_path = os.path.join(blender_versions_dir, version_folder, "scripts", "startup", "dcc_venv_startup.py")
        paths.append(startup_script_path)
    return paths



def install(venv_path, *args, **kwargs):
    
    # Startup Script
    venv_startup_script_path = os.path.join(venv_path, "Lib", "site-packages", "dcc_venv_startup.py").replace("\\", "/")
    
    startup_script_content = '''import runpy
def register():
    runpy.run_path("{}", run_name="__startup__")

def unregister():
    print("unregister dcc-venv here")

if __name__ == "__main__":
    register()
'''.format(venv_startup_script_path)
    
    # Write dcc_venv_startup.py 
    for startup_script_path in get_startup_script_paths():
        ensure_dir_file_path(startup_script_path)
        
        with open(startup_script_path, "w") as fp:
            fp.write(startup_script_content)
        
    log.info("Created: {}".format(startup_script_path))
    
    

def uninstall(*args, **kwargs):
    for startup_script_path in get_startup_script_paths():
        os.remove(startup_script_path)


