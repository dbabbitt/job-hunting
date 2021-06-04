
# C:\Users\DaveBabbitt\.jupyter\jupyter_notebook_config.py

import os

# To create a jupyter_notebook_config.py file, with all the defaults commented out,
# you can use the following command line:
# $ jupyter notebook --generate-config

# Make sure that the path to your repositories and anaconda installation is correct
environ_dict = dict(os.environ)
home_dir = environ_dict['USERPROFILE']
repo_dir = os.path.join(home_dir, 'Documents', 'GitHub')
if 'CONDA_PREFIX' in environ_dict:
	anaconda_dir = environ_dict['CONDA_PREFIX']
else:
	anaconda_dir = os.path.join(home_dir, 'anaconda3')

# Configuration file for jupyter-notebook
c.ContentsManager.root_dir = repo_dir
c.ContentsManager.untitled_directory = '_Untitled_Folder_'
c.ContentsManager.untitled_file = '_untitled_'
c.ContentsManager.untitled_notebook = '_Untitled_'
c.EnvironmentKernelSpecManager.conda_env_dirs=[os.path.join(repo_dir, 'job-hunting'), os.path.join(anaconda_dir, 'envs')]
c.FileContentsManager.root_dir = repo_dir
c.LabBuildApp.dev_build = False
c.LabBuildApp.minimize = False
c.MappingKernelManager.root_dir = repo_dir

# The port the notebook server will listen on –
# 'port' – has moved from NotebookApp to ServerApp
c.ServerApp.port = 8888

# The IP address the notebook server will listen on –
# 'ip' – has moved from NotebookApp to ServerApp
c.ServerApp.ip = 'localhost'

# The directory to use for notebooks and kernels –
# notebook_dir is deprecated, use root_dir
c.ServerApp.notebook_dir = repo_dir
# 'notebook_dir' – has moved from NotebookApp to ServerApp
c.ServerApp.root_dir = repo_dir

# The 'min_open_files_limit' trait of a ServerApp
# instance expected an int, not the NoneType None
c.ServerApp.min_open_files_limit = 0

# Whether to open in a browser after starting –
# 'open_browser' – has moved from NotebookApp to ServerApp
c.ServerApp.open_browser = False
# But apparently is ignored
c.NotebookApp.open_browser = False

# Hashed password to use for web authentication –
# 'password' – has moved from NotebookApp to ServerApp
c.ServerApp.password = u''

# Forcing users to use a password for the Notebook server –
# 'password_required' – has moved from NotebookApp to ServerApp
c.ServerApp.password_required = False

# [LabApp] The 'kernel_spec_manager_class' trait of <jupyterlab.labapp.LabApp object> instance must be a type,
# but 'environment_kernels.EnvironmentKernelSpecManager' could not be imported
#c.NotebookApp.kernel_spec_manager_class = 'environment_kernels.EnvironmentKernelSpecManager'
c.NotebookApp.nbserver_extensions = {'jupyterlab': True}
