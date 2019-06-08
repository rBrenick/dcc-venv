# dcc-venv
Python virtual environment manager for Digital Content Creation software

This is a collection of .py scripts that will setup a virtual environment for all the DCC configs that can be found in the [dcc_venv](https://github.com/rBrenick/dcc-venv/tree/master/dcc_venv) folder.

![tool header image](docs/header_image.png)

## Latest Update

Now in python and with a UI.


## Currently supported DCCs:
```
Maya
Motionbuilder
```

On DCC startup it will add the venv site-packages folder to the DCC's sys.path


## Requires:
```
Python 3.3 or later (you can use install_python.ps1 to setup an install)
```


## How the configs work

Each *config_* folder in [dcc_venv](https://github.com/rBrenick/dcc-venv/tree/master/dcc_venv) contains
```
requirements.txt
venv_handler.py
```

On install the *requirements.txt* will be added to the virtual environment

The *install* method in *venv_handler.py* will then run to figure out how to add the site-packages to the DCC on startup.


## What is "Setup Environment (Tool Dev)"

When running Setup Environment (Tool Dev), all the packages in requirements.txt below the **# DEV** comment will be pip installed -editable.

