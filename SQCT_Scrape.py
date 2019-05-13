import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
from time import sleep
import re
import matplotlib.pyplot as plt
import numpy as np
import csv

def ScrapeSQCT(username, password, departments_list, year, webdriver_path):
    """
    A function that will scrape the SQCT website and return a CSV file.
    The SQCT website is is locked behind a login, so a UWO username and password is requried. 
    Note: The file will be overwritten if a search is repeated
    
    """
    #Initialize browser
    browser = webdriver.Chrome(webdriver_path)
    
    browser.get('https://sqct.uwo.ca/results/login.cfm')
    
    #Entering username
    username_loc = browser.find_element_by_name('txtUsername')
    time.sleep(1)
    username_loc.send_keys(username)
    
    #Entering password
    password_loc = browser.find_element_by_name('txtPassword')
    time.sleep(1)
    password_loc.send_keys(password)
    
    #Clicking sign in button
    sign_in = browser.find_element_by_xpath('//*[@id="loginForm"]/button')
    sign_in.click()
    time.sleep(2)
        
    #Setup CSV file and headers before adding anything to CSV file
    with open('teacher_file.csv', mode='w', newline = '') as teacher_file:
        average_writer = csv.writer(teacher_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        average_writer.writerow(['Professor_Name', 'Average_Rating', 'Department'])
    
    for department in departments_list:
        
        #Moving to search page for SQCT database
        browser.get('https://sqct.uwo.ca/results/search.cfm')
        
        #Search for department
        search_department_loc = browser.find_element_by_name('teachingDept')
        time.sleep(2)
        search_department_loc.send_keys(department)
        
        #Selecting the year to search
        year_select = Select(browser.find_element_by_id('acadYear'))
        year_select.select_by_visible_text(year)
        
        #Submitting search
        search_button = browser.find_element_by_xpath('/html/body/div/div[5]/form/div[10]/div/button[1]')
        search_button.click()
        
        #Now at list of instructors
        
        #Count how many courses are in department
        number_of_courses = len(browser.find_elements_by_xpath('/html/body/div/table/tbody/tr'))
        
        #Init a list for storing list of links to teacher's SQCT results
        list_of_teacher_links = []
        
        #Init list that will contain tuples containing the teacher name, average, department 
        teacher_averages = []
        
        #tr starts at 1, and don't want first tr (so start at 2)
        
        for course_index in range(2,number_of_courses + 1):
    
            #Getting link to teacher's page
            teacher_element = browser.find_element_by_xpath('/html/body/div/table/tbody/tr['+str(course_index)+']/td[1]/a')
            teacher_link = teacher_element.get_attribute('href')
            #Storing link in list
            list_of_teacher_links.append(teacher_link) #Adding links to all teacher to a list
            
        #Now have built a list of links to teachers pages, will go to each one
        for website in list_of_teacher_links:
            #Go to teachers page
            time.sleep(5)
            browser.get(website)
            
            #Grab mean value and clean up data
            teacher_mean = browser.find_element_by_xpath('/html/body/div/table[2]/tbody/tr[11]/td[10]')
            teacher_mean = teacher_mean.get_attribute('innerHTML')
            teacher_mean = re.sub('[^0-9^.]', '', teacher_mean)
            
            #Grab professor name
            teacher_name = browser.find_element_by_xpath('/html/body/div/table[1]/tbody/tr[2]/td[1]')
            teacher_name = teacher_name.get_attribute('innerHTML')
            
            #Add name, mean, department to list of teacher averages
            teacher_averages.append((teacher_name, float(teacher_mean), department))
        
        #Will be adding each tuple in list as a row in a CSV file
        with open('teacher_file.csv', mode='a', newline = '') as teacher_file:
            average_writer = csv.writer(teacher_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            #Write entry for each class taught to csv file, there will be duplicate professors with different averages if more than one class is taught by them
            for item in teacher_averages:
                average_writer.writerow([item[0], item[1], item[2]])
            #Redundant, but for some reason CSV file considered to be open unless I put this in
            teacher_file.close()
    
    #Print Done when data is scraped and saved to csv
    print("Done")
    
    
#Example test code to search departements
username = 'Put UWO username here'
password = 'Put UWO password here'
departments = ['Chemistry','Biology','Physics', 'Biochemistry','Applied Mathematics', 'Computer Science', 'Statistics & Actuarial Science', 'Political Science', 'Economics']
year = '2018 Fall/Winter'
webdriver_path = 'C:\\Users\\chromedriver.exe'

ScrapeSQCT(username,password,departments,year,webdriver_path)
    