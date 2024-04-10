
conda info --envs
conda deactivate
conda config --set auto_update_conda true
conda config --set report_errors false
conda clean --all --yes
conda update --all --yes
npm cache verify
npm install -g npm
npm update -g
cd /mnt/c/Users/daveb/OneDrive/Documents/GitHub/job-hunting/
conda create --name jh_env --channel conda-forge python jupyterlab nodejs --yes
conda activate jh_env
conda info --envs
cd /home/dbabbitt/anaconda3/envs/jh_env
bin/python --version
bin/python -m ipykernel install --user --name jh_env --display-name "Job Hunting (Python 3.12.2)"
cat /home/dbabbitt/.local/share/jupyter/kernels/jh_env/kernel.json
jupyter-lab clean
jupyter-lab build