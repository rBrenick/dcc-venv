import os
import sys
import inspect

sys.stdout.write("#"*50)
sys.stdout.write("\n dcc_venv setup\n")

CURRENT_DIR = os.path.dirname(inspect.getfile(inspect.currentframe()))

site_paths = []
for f in os.listdir(CURRENT_DIR):
    if f.endswith('.egg-link'):
    
        egg_link_path = os.path.join(CURRENT_DIR, f)
        
        with open(egg_link_path, "r") as fp:
            for path in fp.read().splitlines():
                if path == ".":
                    continue
                    
                site_paths.append(os.path.abspath(path))

if site_paths:
    sys.stdout.write("\nDEV site-setup\n")
                    
    for site_path in site_paths:
        if not site_path in sys.path:
            print("DEV - adding to sys.path {}".format(site_path))
            sys.path.append(site_path)
        
sys.stdout.write("#"*50)
