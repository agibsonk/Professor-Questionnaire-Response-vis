import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
from time import sleep
import re
import matplotlib.pyplot as plt
import numpy as np
import csv


##PROVIDE UWO USERNAME AND PASSWORD HERE, NEEDED TO LOGIN TO SQCT WEBSITE
my_username = ''
my_password = ''

departments_list = ['Chemistry','Biology','Physics', 'Biochemistry','Applied Mathematics', 'Computer Science', 'Statistics & Actuarial Science', 'Political Science', 'Economics']
year = '2018 Fall/Winter'

#Init browser
browser = webdriver.Chrome('C:\\Users\\AG\\Chromedriver\\chromedriver.exe')

browser.get('https://sqct.uwo.ca/results/login.cfm')

#Entering username
username_loc = browser.find_element_by_name('txtUsername')
time.sleep(1)
username_loc.send_keys(my_username)

#Entering password
password_loc = browser.find_element_by_name('txtPassword')
time.sleep(1)
password_loc.send_keys(my_password)

#Clicking sign in button
sign_in = browser.find_element_by_xpath('//*[@id="loginForm"]/button')
sign_in.click()
time.sleep(2)
    
#Setup CSV headers
with open('teacher_file.csv', mode='w', newline = '') as teacher_file:
    average_writer = csv.writer(teacher_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    average_writer.writerow(['Professor_Name', 'Average_Rating', 'Department'])

for department in departments_list:
    
    #Moving to search page
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
    
    dept_search_URL = browser.current_url
    
    #Now at list of instructors
    
    number_of_courses = len(browser.find_elements_by_xpath('/html/body/div/table/tbody/tr'))
    
    list_of_teacher_links = []
    
    teacher_averages = []
    
    #REMEMBER tr starts at 1, and don't want first tr (so start at 2)
    
    for course_index in range(2,number_of_courses + 1):

        #Getting link to teacher
        teacher_element = browser.find_element_by_xpath('/html/body/div/table/tbody/tr['+str(course_index)+']/td[1]/a')
        
        teacher_link = teacher_element.get_attribute('href')
        
        list_of_teacher_links.append(teacher_link) #Adding links to all teacher to a list
        
        
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
        
    
    with open('teacher_file.csv', mode='a', newline = '') as teacher_file:
        average_writer = csv.writer(teacher_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        #Write entry for each class taught to csv file, there will be duplicate professors with different averages if more than one class is taught by them
        for item in teacher_averages:
            average_writer.writerow([item[0], item[1], item[2]])
        #Redundant
        teacher_file.close()


print("Done")