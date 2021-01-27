
# C:\Users\dev\.jupyter\jupyter_notebook_config.py

import os

# To create a jupyter_notebook_config.py file, with all the defaults commented out,
# you can use the following command line:
# $ jupyter notebook --generate-config

# Make sure that the path to your repositories is correct
environ_dict = dict(os.environ)
home_dir = environ_dict['USERPROFILE']
repo_dir = os.path.join(home_dir, 'Documents', 'Repositories')
if 'CONDA_PREFIX' in environ_dict:
	anaconda_dir = environ_dict['CONDA_PREFIX']
else:
	anaconda_dir = os.path.join(home_dir, 'anaconda3')

# Configuration file for jupyter-notebook.
c.ContentsManager.root_dir = repo_dir
c.ContentsManager.untitled_directory = '_Untitled_Folder_'
c.ContentsManager.untitled_file = '_untitled_'
c.ContentsManager.untitled_notebook = '_Untitled_'
c.EnvironmentKernelSpecManager.conda_env_dirs=[os.path.join(repo_dir, 'job-hunting'), os.path.join(anaconda_dir, 'envs')]
c.FileContentsManager.root_dir = repo_dir
c.LabBuildApp.dev_build = False
c.LabBuildApp.minimize = False
c.MappingKernelManager.root_dir = repo_dir
c.NotebookApp.ip = 'localhost'
c.NotebookApp.open_browser = False
c.NotebookApp.password = u''
c.NotebookApp.password_required = False
c.NotebookApp.port = 8888

# [LabApp] The 'kernel_spec_manager_class' trait of <jupyterlab.labapp.LabApp object> instance must be a type,
# but 'environment_kernels.EnvironmentKernelSpecManager' could not be imported
#c.NotebookApp.kernel_spec_manager_class = 'environment_kernels.EnvironmentKernelSpecManager'
c.NotebookApp.nbserver_extensions = {'jupyterlab': True}
