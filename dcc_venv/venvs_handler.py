import os
import sys
import imp
import venv
import shutil
import stat

import logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(" dcc-venv  ")

import requirements_handler as reqhand

# VENV_ROOT_FOLDER = os.path.join(os.path.expanduser('~'), ".dcc-venvs")
VENV_ROOT_FOLDER = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), ".venvs")
CONFIGS_FOLDER = os.path.abspath(os.path.dirname(__file__))
CONFIG_PREFIX = "config_"
DCC_STARTUP_SCRIPT = os.path.join(CONFIGS_FOLDER, "common", "dcc_venv_startup.py")


def get_dcc_configs(target_configs=()):
    
    configs = {}
    for folder, subfolder, files in os.walk(CONFIGS_FOLDER):
        if CONFIG_PREFIX in folder:
            dcc_name = os.path.basename(folder).replace(CONFIG_PREFIX, "")
            configs[dcc_name] = os.path.abspath(folder)
    
    for target_config in target_configs:
        if target_config not in configs.keys():
            log.warning("{}{} not found in: {}".format(CONFIG_PREFIX, target_config, CONFIGS_FOLDER))
    
    return configs


def get_dcc_name_from_venv(venv_path):
    return venv_path.replace("\\", "/").split("/.")[-1].split("_venv")[0] # this is kinda dumb

    
def get_activate_bat_path(venv_path):
    dcc_name = get_dcc_name_from_venv(venv_path)
    bat_path = os.path.join(VENV_ROOT_FOLDER, f"venv_activate__{dcc_name}.bat")
    return bat_path
    
    
def create_activate_bat(venv_path):

    bat_path = get_activate_bat_path(venv_path)
    
    bat_content = r"start cmd /k call {}\Scripts\activate.bat".format(venv_path)
    
    with open(bat_path, "w") as fp:
        fp.write(bat_content)
    

def install_venv(target_configs=(), developer=False):
    
    dcc_configs = get_dcc_configs(target_configs)
    
    for dcc, config_folder in dcc_configs.items():
        if target_configs and dcc not in target_configs:
            continue
        
        requirements_path = os.path.join(config_folder, "requirements.txt")
        venv_name = ".{}_venv".format(dcc)
        venv_path = os.path.join(VENV_ROOT_FOLDER, venv_name)
        site_packages_path = os.path.join(venv_path, "Lib", "site-packages")
        
        
        log.info("#"*50)
        log.info("Creating {} ...".format(venv_path))
        venv.create(venv_path, with_pip=True)
        
        
        
        
        log.info("Installing Requirements for {} ...".format(dcc))
        
        if developer:
            req_dev_path = reqhand.create_requirements_dev(requirements_path)
            requirements_path = req_dev_path
            
        activate_cmd = "call {}/scripts/activate".format(venv_path)
        os.system('{} && pip install -r {}'.format(activate_cmd, requirements_path))
        
        
        
        log.info("Creating venv_activate__{}.bat".format(dcc))
        create_activate_bat(venv_path)
        
        
        
        log.info("Installing config {}".format(dcc))
        mod = imp.load_source("__dcc__", os.path.join(config_folder, "venv_handler.py"))
        mod.install(venv_path)
        
        
        
        log.info("Installing startup egg link script - {}".format(dcc))     
        startup_path = os.path.join(site_packages_path, os.path.basename(DCC_STARTUP_SCRIPT))
        shutil.copy(DCC_STARTUP_SCRIPT, startup_path)
        
        
        
        log.info("#"*50)
        sys.stdout.write("\n{} \n\n".format("-"*100))
        
        if developer and os.path.exists(req_dev_path):
            os.remove(req_dev_path)
            
        
    sys.stdout.write("\ndcc-venv install complete for: {}\n\n".format(", ".join(target_configs), "-"*100))


def update_venv(target_configs=(), developer=False):
    
    dcc_configs = get_dcc_configs(target_configs)
    
    for dcc, config_folder in dcc_configs.items():
        if target_configs and dcc not in target_configs:
            continue
        
        requirements_path = os.path.join(config_folder, "requirements.txt")
        venv_name = ".{}_venv".format(dcc)
        venv_path = os.path.join(VENV_ROOT_FOLDER, venv_name)
        
        
        if not os.path.exists(venv_path):
            log.warning("venv does not exist for updating: {}".format(venv_name))
            continue
            
            
        log.info("Reinstalling Requirements for {} ...".format(dcc))

        if developer:
            req_dev_path = reqhand.create_requirements_dev(requirements_path)
            requirements_path = req_dev_path
        
        
        activate_cmd = "call {}/scripts/activate".format(venv_path)
        os.system('{} && pip install --upgrade --force-reinstall -r {}'.format(activate_cmd, requirements_path))
        
        
        
        if developer and os.path.exists(req_dev_path):
            os.remove(req_dev_path)
        


def uninstall_venv(target_configs=(), developer=False):
    
    dcc_configs = get_dcc_configs(target_configs)
    
    for dcc, config_folder in dcc_configs.items():
        if target_configs and dcc not in target_configs:
            continue
        
        venv_name = ".{}_venv".format(dcc)
        venv_path = os.path.join(VENV_ROOT_FOLDER, venv_name)
        
        
        
        log.info("#"*50)
        log.info("Uninstalling {} ...".format(venv_name))
        
        if os.path.exists(venv_path):
            shutil.rmtree(venv_path, onerror=onremoveerror)
        
        activate_bat = get_activate_bat_path(venv_path)
        if os.path.exists(activate_bat):
            log.info("Removing venv_activate__{}.bat".format(dcc))
            os.remove(activate_bat)
        
        
        
        
        log.info("running config_{} uninstall".format(dcc))
        mod = imp.load_source("__dcc__", os.path.join(config_folder, "venv_handler.py"))
        mod.uninstall(venv_path)
        
        
        
        log.info("#"*50)
        sys.stdout.write("\n{} \n\n".format("-"*100))
    
    
    sys.stdout.write("\ndcc-venv uninstall complete for: {}\n\n".format(", ".join(target_configs), "-"*100))
    
    if len(os.listdir(VENV_ROOT_FOLDER)) == 0: # remove folder if empty
        os.rmdir(VENV_ROOT_FOLDER)
    
        
def onremoveerror(func, path, exc_info):
    """
    Error handler for ``shutil.rmtree``.

    If the error is due to an access error (read only file)
    it attempts to add write permission and then retries.

    If the error is for another reason it re-raises the error.

    Usage : ``shutil.rmtree(path, onerror=onerror)``
    """
    import stat
    if not os.access(path, os.W_OK):
        # Is the error an access error ?
        os.chmod(path, stat.S_IWUSR)
        func(path)
    else:
        raise


def str2bool(v):
    """
    I can't believe this isn't built in
    
    https://stackoverflow.com/a/43357954
    
    """
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

        
if __name__ == "__main__":
    os.system("cls")
    log.info("#"*85)
    log.info("dcc_venvs setup")
    log.info("#"*85)
    sys.stdout.write("\n{} \n\n".format("-"*100))
    
    func_map = {"install": install_venv,
                "update": update_venv,
                "uninstall": uninstall_venv}
                
    import argparse
    parser = argparse.ArgumentParser("venv handler")
    parser.add_argument("type", type=str, help="install or uninstall")
    parser.add_argument("-dev", type=str2bool, help="use edit install for git packages under '# DEV' tag")
    parser.add_argument("-dccs", default=(), nargs="+", help="specific dccs")
    args = parser.parse_args()
    
    func = func_map.get(args.type)
    func(args.dccs, args.dev)
    os.system("pause")
    











    
