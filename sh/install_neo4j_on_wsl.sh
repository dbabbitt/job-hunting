

ls
cd ../; ls
cd mnt; ls
cd c; ls
cd Users; ls
cd daveb; ls
cd OneDrive; ls
cd Documents; ls
cd GitHub/; ls
cd job-hunting/; ls
cd django/; ls
which python
echo $PATH
sudo apt update
sudo apt upgrade
wget https://repo.anaconda.com/archive/Anaconda3-2024.02-1-Linux-x86_64.sh
ls
bash Anaconda3-2024.02-1-Linux-x86_64.sh
source ~/.bashrc
ls
cd ../; ls
cd mnt; ls
cd c; ls
cd Users; ls
cd daveb/; ls
ls -l
jupyter notebook --generate-config
ls
cd /home/dbabbitt; ls
ls -a
cd /mnt/c/Users/daveb; ls -a
cd .jupyter/; ls
ls /mnt/c/Users/daveb/.jupyter/
ls /home/dbabbitt/.jupyter
jupyter lab --generate-config
which python
conda list
clear
conda --envs
conda envs -h
conda list --envs
conda list --help
conda --help
conda info --help
conda info --envs
conda deactivate
conda config --set auto_update_conda true
conda config --set report_errors false
conda clean --all --yes
conda update --all --yes
npm cache clean
npm cache verify
npm install -g npm
npm update -g
ls /mnt/c/Users/daveb/OneDrive/Document
ls /mnt/c/Users/daveb/OneDrive/Documents
ls /mnt/c/Users/daveb/OneDrive/Documents/GitHub/job-hunting/jh_env/
cd /mnt/c/Users/daveb/OneDrive/Documents/GitHub/job-hunting/
ls
conda env update --prefix /mnt/c/Users/daveb/OneDrive/Documents/GitHub/job-hunting/jh_env --file environment.yml --prune
conda env update --file environment.yml --prune
conda env update --name jh_env --file /mnt/c/Users/daveb/OneDrive/Documents/GitHub/job-hunting/environment.yml --prune
conda env update --name jh_env
conda --help
conda env create --name jh_env --file /mnt/c/Users/daveb/OneDrive/Documents/GitHub/job-hunting/environment.yml --prune
conda env create --name jh_env --file /mnt/c/Users/daveb/OneDrive/Documents/GitHub/job-hunting/environment.yml
clear
conda create --help
conda create --name jh_env --channel conda-forge python jupyterlab nodejs --yes
conda activate jh_env
conda info --envs
conda env update --name jh_env --file /mnt/c/Users/daveb/OneDrive/Documents/GitHub/job-hunting/environment.yml --prune
cd /home/dbabbitt/anaconda3/envs/jh_env
ls
ls bin
$PATH
echo $PATH
bin/python --version
bin/python -m ipykernel install --user --name jh_env --display-name "Job Hunting (Python 3.12.2)"
ls /home/dbabbitt/.local/share/jupyter/kernels/jh_env
cat kernel.json
cat /home/dbabbitt/.local/share/jupyter/kernels/jh_env/kernel.json
jupyter-lab clean
jupyter-lab build
history
curl -fsSL https://packages.redis.io/gpg | sudo gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/redis.list
sudo apt-get update
echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/redis.list
sudo apt-get install redis
echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/redis.list
deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb jammy main
sudo service redis-server start
redis-cli
sudo apt install libcairo2-dev  # Installs Cairo development headers
/home/dbabbitt/anaconda3/envs/jh_env/bin/python -m pip install pycairo --upgrade
sudo apt-get update
sudo apt-get install pkg-config
/home/dbabbitt/anaconda3/envs/jh_env/bin/python -m pip install pycairo --upgrade
sudo apt-get update
sudo apt-get install build-essential
/home/dbabbitt/anaconda3/envs/jh_env/bin/python -m pip install pycairo --upgrade
/home/dbabbitt/anaconda3/envs/jh_env/bin/python -m pip install pygobject --upgrade
sudo apt-get update
sudo apt-get install libgirepository1.0-dev
/home/dbabbitt/anaconda3/envs/jh_env/bin/python -m pip install pygobject --upgrade
sudo ufw app list  # List all applications allowed by ufw
sudo ufw status   # Check the current firewall status (enabled/disabled)
sudo iptables -L INPUT  # List firewall rules for the INPUT chain (incoming traffic)
sudo iptables -L OUTPUT # List firewall rules for the OUTPUT chain (outgoing traffic)
which nc
nc -z localhost 7474
nc -z localhost 7687
nc -z localhost 7473
sudo apt-get update
sudo apt-get install unixodbc unixodbc-dev
clear
cd /mnt/; ls
cd c; ls
cd Users/; ls
cd daveb/; ls
cd Downloads/; ls
mv geckodriver-v0.34.0-linux64.tar.gz /usr/local/bin/
ls /usr/local/bin/
ls /usr/local/
sudo mv geckodriver-v0.34.0-linux64.tar.gz /usr/local/bin/
cd /usr/local/bin/; ls
tar -xvzf geckodriver-v0.34.0-linux64.tar.gz
sudo tar -xvzf geckodriver-v0.34.0-linux64.tar.gz
ls
ls -a -l
cd geckodriver
chmod +x geckodriver
echo $PATH
rm geckodriver-v0.34.0-linux64.tar.gz
sudo rm geckodriver-v0.34.0-linux64.tar.gz
ls
geckodriver --version
sudo apt update
sudo apt install firefox
sudo apt update
sudo apt upgrade
sudo apt install libx11-dev libxrender-dev libgconf-2-dev libnss3-dev libgtk2.0-dev
sudo apt install libx11-dev libxrender-dev libgirepository1.0-dev libnss3-dev libgtk2.0-dev
sudo apt install xvfb-run
sudo apt-cache search xvfb
sudo apt install xdg-utils  # This should install xdg-settings
firefox
sudo firefox
sudo snap remove firefox
sudo apt update && sudo apt install firefox
firefox
snap install firefox
sudo snap install firefox
firefox
netstat -aon | findstr 7687
sudo apt install net-tools
netstat -aon | findstr 7687
sudo apt install findstr
ss -aln | grep 7687
ps -ef | grep neo4j
sudo apt update
sudo apt install snapd
sudo snap install neo4j
ls /
ls /mnt/c/
ls /mnt/c/Users/
ls /mnt/c/Users/daveb/
ls /mnt/c/Users/daveb/Downloads/
chmod +x /mnt/c/Users/daveb/Downloads/neo4j-desktop-1.5.9-x86_64.AppImage
/mnt/c/Users/daveb/Downloads/neo4j-desktop-1.5.9-x86_64.AppImage
sudo add-apt-repository universe
sudo apt install libfuse2
/mnt/c/Users/daveb/Downloads/neo4j-desktop-1.5.9-x86_64.AppImage
/mnt/c/Users/daveb/Downloads/neo4j-desktop-1.5.9-x86_64.AppImage --appimage-extract
ls
ls squashfs-root/
ls squashfs-root/ -a -l
ls /mnt/c/Users/daveb/Downloads/ -a -l
squashfs-root/neo4j-desktop
sudo apt update
sudo apt install libgbm-dev
squashfs-root/neo4j-desktop
sudo apt update
sudo apt install libasound2
squashfs-root/neo4j-desktop
sudo apt install openjdk-11-jre-headless
wget -O - https://debian.neo4j.com/neotechnology.gpg.key | sudo apt-key add -
echo 'deb https://debian.neo4j.com stable latest' | sudo tee -a /etc/apt/sources.list.d/neo4j.list
sudo apt-get update
apt list -a neo4j
sudo apt-get install neo4j=1:5.19.0
sudo service neo4j start
sudo service --status-all | grep neo4j
sudo service neo4j status
ip addr
sudo ss -tlnp | grep -E '(7474|7687)'
sudo systemctl stop neo4j.service