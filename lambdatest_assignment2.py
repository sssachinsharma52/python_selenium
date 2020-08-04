#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 01:11:16 2020

@author: sachin
"""

import time
import urllib
import requests
import os
from selenium import webdriver
from PIL import Image


url=input("Enter a valid url :")
#url="https://www.facebook.com/"

#to get the status of url
status_code = requests.get(url).status_code
print (status_code)

desiredCapabilities_firefox={
    "browserName":"firefox"
}

desiredCapabilities_chrome={
    "browserName":"chrome"
}


#function to create selenium grid
def selenium_grid_create():

    #Creating selenium grid
    print ("Creating Selenium grid with hub and nodes . . . ")

    #creating container for hub
    resp = "docker run -d -p 4444:4444 --shm-size=2g --name hub  selenium/hub"
    resp_data = os.popen(resp)
    output = resp_data.read()
    print (output)


    #node-chrome
    resp1 = "docker run -d  -p 5551:4444 --name chrome_latest --link hub:hub selenium/node-chrome"
    resp_data1 = os.popen(resp1)
    output1 = resp_data1.read()
    print (output1)

    #node-firefox
    resp2 = "docker run -d  -p 5552:4444 --name firefox_latest --link hub:hub selenium/node-firefox"
    resp_data2 = os.popen(resp2)
    output2 = resp_data2.read()
    print (output2)


def selenium_grid_destroy():

    #delete hub
    print ("Deleting Selenium grid with hub and nodes . . . ")
    resp = "docker container kill hub && docker container rm hub"
    resp_data = os.popen(resp)
    output = resp_data.read()
    print (output)


    #node-chrome
    resp1 = "docker container kill chrome_latest && docker container rm chrome_latest"
    resp_data1 = os.popen(resp1)
    output1 = resp_data1.read()
    print (output1)

    #node-firefox
    resp2 = "docker container kill firefox_latest && docker container rm firefox_latest"
    resp_data2 = os.popen(resp2)
    output2 = resp_data2.read()
    print (output2)






#function name should start with test to work with pytest selenium
def test_chrome_browser(url):


    #logic to click screenshot
    driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub',desired_capabilities = desiredCapabilities_chrome)
    driver.get(url)
    driver.save_screenshot("image_chrome.png")
    image_chrome = Image.open("image_chrome.png")
    image_chrome.show()
    driver.quit()


    #uploading the image to s3 bucket
    print ("uploading screenshot to s3 bucket . . .")
    resp2 = "aws s3 cp image_chrome.png  s3://test-suite-test/ --profile default"
    resp_data2 = os.popen(resp2)
    output2 = resp_data2.read()
    print(output2)

    #presigned url to download the image
    print ("Presigned URL to download the image is given below, link will expire in 30 mins")
    resp3 = "aws s3 presign s3://test-suite-test/image_chrome.png --expires-in 1800 --profile default"
    resp_data3 = os.popen(resp3)
    output3 = resp_data3.read()
    print(output3)

#
#
#
def test_firefox_browser(url):


    driver1 = webdriver.Remote(command_executor='http://localhost:4444/wd/hub',desired_capabilities = desiredCapabilities_firefox)
    driver1.get(url)
    driver1.save_screenshot("image_firefox.png")
    image_chrome = Image.open("image_firefox.png")
    image_chrome.show()
    driver1.quit()


    print ("uploading screenshot to s3 bucket . . .")
    resp2 = "aws s3 cp image_firefox.png  s3://test-suite-test/ --profile default"
    resp_data2 = os.popen(resp2)
    output2 = resp_data2.read()
    print(output2)

    print ("Presigned URL to download the image is given below, link will expire in 30 mins")
    resp3 = "aws s3 presign s3://test-suite-test/image_firefox.png --expires-in 1800 --profile default"
    resp_data3 = os.popen(resp3)
    output3 = resp_data3.read()
    print(output3)



if status_code ==200:

    #Calling function to create hub
    selenium_grid_create()

    time.sleep(10)

    #parallely executing
    from pexecute.process import ProcessLoom
    loom = ProcessLoom(max_runner_cap=4)
    work = [(test_chrome_browser, [url]), (test_firefox_browser, [url])]
    loom.add_work(work)
    output = loom.execute()


    time.sleep(10)

    #calling function to destroy grid
    selenium_grid_destroy()

else:
    try:
        print ("Please enter correct URL, status of url is not 200")
    except ValueError as e:
        print (e)
