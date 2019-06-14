import os
import sys
import site
import inspect

def startup():

    sys.stdout.write("#"*50)
    sys.stdout.write("\ndcc_venv_startup\n")
    
    # Add site-packages to sys.path
    CURRENT_DIR = os.path.dirname(inspect.getfile(inspect.currentframe()))
    
    if CURRENT_DIR not in site.getsitepackages():
        site.addsitedir(CURRENT_DIR)
        
    # startup complete
    sys.stdout.write("#"*50)

    
if __name__ == "__startup__":
    startup()
