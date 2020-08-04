#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 16:23:08 2020

@author: sachin
"""
import time
import requests
#import urllib.request
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

#function name should start with test to work with pytest selenium
def test_chrome_browser(url):

    #creating disposable container
    print ("Creating container for chrome . . . ")
    resp = "docker run -d -p 4444:4444 --name chrome --shm-size=2g  selenium/standalone-chrome "
    resp_data = os.popen(resp)
    output = resp_data.read()
    print("container_id:" + output)

    #waiting for sometime so that the page loads properly
    time.sleep(10)

    #logic to click screenshot
    driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub',desired_capabilities = desiredCapabilities_chrome)
    driver.get(url)
    driver.save_screenshot("image_chrome.png")
    image_chrome = Image.open("image_chrome.png")
    image_chrome.show()
    driver.quit()

    #deleting container
    print ("Deleting container")
    resp1 = "docker container kill chrome && docker container rm chrome "
    resp_data1 = os.popen(resp1)
    output1 = resp_data1.read()
    print("container_id:" + output1)

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

    print ("Creating container for firefox . . . ")
    resp = "docker run -d -p 4445:4444 --name firefox --shm-size 2g selenium/standalone-firefox"
    resp_data = os.popen(resp)
    output = resp_data.read()
    print ("container_id:" + output)

    time.sleep(10)


    driver1 = webdriver.Remote(command_executor='http://localhost:4445/wd/hub',desired_capabilities = desiredCapabilities_firefox)
    driver1.get(url)
    driver1.save_screenshot("image_firefox.png")
    image_chrome = Image.open("image_firefox.png")
    image_chrome.show()
    driver1.quit()

    print("Deleting container . . .")
    resp1 = "docker container kill firefox && docker container rm firefox"
    resp_data1 = os.popen(resp1)
    output1 = resp_data1.read()
    print("container_id:" + output1)

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


#finally running the code

if status_code ==200:

    #parallely executing
    from pexecute.process import ProcessLoom
    loom = ProcessLoom(max_runner_cap=4)
    work = [(test_chrome_browser, [url]), (test_firefox_browser, [url])]
    loom.add_work(work)
    output = loom.execute()

else:
    try:

        print ("Please enter correct URL, status of url ")
    except ValueError as e:
        print ("Please enter correct URL, status of url ")
        print (e)
