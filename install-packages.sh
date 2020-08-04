
#install docker
sudo apt-get update
sudo apt-get remove docker docker-engine docker.io
sudo apt install docker.io
sudo systemctl start docker
sudo systemctl enable docker
docker --version
sudo groupadd docker
sudo usermod -aG docker $USER


#pull docker images
docker pull selenium/hub
docker pull selenium/node-chrome
docker pull selenium/node-firefox
docker pull selenium/standalone-chrome
docker pull selenium/standalone-firefox



#install python 3.7.3 and pip 
sudo apt install python3.7
alias python=python3
python --version 

sudo apt install python3-pi
sudo apt install python-pip
alias pip=pip3
alias python=python3

pip install parallel-execute
pip install selenium
pip install requests
pip install Pillow
pip install py-execute


#install awscli
sudo apt install awscli