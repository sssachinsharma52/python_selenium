# python_selenium
Run selenium test case in python with disposable containers


## Problem statement
- We need a system where we provide a website link and want to capture the screenshot on chrome & Firefox in Ubuntu.

- Create a script which asks for a website link and spawns 2 containers parallely and opens that link in chrome  and Firefox, capture the screenshot, push them to s3 and provide 2 signed s3 links.

- Links should expire after 30 mins.



## Pre-Requisite 

### Install docker

- sudo apt-get update
- sudo apt-get remove docker docker-engine docker.io
- sudo apt install docker.io
- sudo systemctl start docker
- sudo systemctl enable docker
- docker --version
- sudo groupadd docker
- sudo usermod -aG docker $USER

**It's good to pull these images initially**

- docker pull selenium/hub
- docker pull selenium/node-chrome
- docker pull selenium/node-firefox
- docker pull selenium/standalone-chrome
- docker pull selenium/standalone-firefox



### Install python and pip 

- sudo apt install python3.7
- alias python=python3
- python --version 

- sudo apt install python3-pip
- sudo apt install python-pip
- alias pip=pip3


### Install python dependencies
- pip install parallel-execute
- pip install seleniump
- pip install requests
- pip install Pillow
- pip install py-execute


### Install awscli
- sudo apt install awscli

## Configure awscli 

- aws configure

AWS Access Key ID [None]: ########################\
AWS Secret Access Key [None]: ########################\
Default region name [None]: ap-northeast-1\
Default output format [None]: text


### How to Run script ?
- python3 lambdatest_assignment1.py
- python3 lambdatest_assignment2.py

and when asked for **URL**, paas values like  https://www.facebook.com/ in proper format as mentioned.


## Alternative

### NOTE: You can also install the above pre-requisties using the install_packages.sh script.
Run chmod +x install_packages.sh && ./install_packages.sh 

## Solution:
I have done it in two different ways which are explained below: 


#### Method 1

Creation of disposable containers which will create docker containers of selenium/standalone-chrome and selenium/standalone-firefox images and check the test case parallely.


### Steps of execution:

- Insert proper url.
- Create parallel standalone containers of selenium/standalone-chrome and selenium/standalone-firefox images.
- Take screenshot of the web page after loading
- Delete the container and hence these are disposable containers
- Upload the image to s3
- Provide the presigned URL to download the image which will expire after 30 mins.



**NOTE:** These two test cases are executed parallely. There are different ways of doing them like pytest, process loom etc. I have done this using process loom. 





#### Method 2

Creation of disposable containers which will first create a selenium grid which consists of hub and nodes. Each of the hub, chrome-node and firefox-node are separate docker containers of selenium/hub, selenium/node-chrome and selenium/node-firefox images.


### Steps of execution:

- Insert proper url.
- Create a selenium grid of hub and nodes using docker with each component as a separate container.
- Take a screenshot of the web page after loading on both the browsers parallely.
- Upload the images to s3 and give a presigned url to download the images which will expire after 30 mins.
- Delete the selenium grid after completion of test cases.

**NOTE:** 

- These two test cases are executed parallely after creation of the selenium grid. There are different ways of creating this grid, I have used docker in python so as to keep everything in one python script. We can also create the same using docker compose. 

- Here also I have used processloom for parallel execution. 

- **I have already created s3 bucket and have passed the bucket name in script. You can add your bucket name in the script.** 

**Refer:**

Which docker image ?

- standalone-firefox – Image to create standalone grid
- standalone-firefox-debug – Image to create standalone grid with debugging capability
- node-firefox – Image to create selenium node that can be registered to hub

