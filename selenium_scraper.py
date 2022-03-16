# -*- coding: utf-8 -*-
"""
Created on Sat Mar 12 22:45:16 2022

@author: Osman
"""
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def job_scraper(number_of_page, path, keyword):

    url = "https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword="+keyword+"&sc.keyword="+keyword+"&locT=&locId=&jobType="    
    driver = webdriver.Chrome(executable_path=path)
    #driver.maximize_window()
    driver.get(url)

    page = 1

    company_name = []
    job_title = []
    job_description = []
    salary_estimate = []
    #publish_date = []
    while page < int(number_of_page) + 1:
        print("Page: {}".format("" + str(page) + '/'+ str(number_of_page)))
        #element =driver.find_element_by_xpath('//article[@id="MainCol"]/div[2]/div[1]/div[2]').text
        #print(element)
        
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="MainCol"]/div[1]/ul/li')))
        job_buttons = driver.find_elements_by_xpath('//*[@id="MainCol"]/div[1]/ul/li')  #jl for Job Listing. These are the buttons we're going to click.
        i = 1

        for job_button in job_buttons:  
            print("Progress: {}".format("" + str(i) + '/'+ str(len(job_buttons))))

            job_button.click()  #You might 
            time.sleep(1)
            i = i+1


            try:
                driver.find_element_by_css_selector('[alt="Close"]').click() #clicking to the X.
                #print(' x out worked')
            except NoSuchElementException:
                #print(' x out failed')
                pass


            try:
                name = driver.find_element_by_xpath('//article[@class="scrollable active css-1ctl34j ead8scz3"]/div[1]/div[1]/div[1]/div[1]/div[1]/div[3]/div[1]/div').text
                company_name.append(name)
            except:
                time.sleep(5)
                company_name.append(' ')

            try:
                title = driver.find_element_by_xpath("//article[@class='scrollable active css-1ctl34j ead8scz3']/div[1]/div[1]/div[1]/div/div/div/div/div[@class='css-1j389vi e1tk4kwz2']").text
                job_title.append(title)
            except:
                time.sleep(5)
                job_title.append(' ')

            try:
                description = driver.find_element_by_xpath("//article[@class='scrollable active css-1ctl34j ead8scz3']/div[1]/div[2]/div[1]/div[1]/div[@id='JobDescriptionContainer']/div/div[@class='jobDescriptionContent desc']").text
                job_description.append(description)
            except:
                time.sleep(5)
                job_description.append(' ')

            # try:  
            #     publish_date = driver.find_element_by_xpath("//*[@id='MainCol']/div[1]/ul/li/div[2]/div[2]/div[1]/div[2]").text
            # except:
            #     publish_date = ' '

            try:
                estimation = driver.find_element_by_xpath("//article[@class='scrollable active css-1ctl34j ead8scz3']/div[1]/div[1]/div[1]/div[1]/div[1]/div[3]/div[1]/div[4]/span[1]").text
                salary_estimate.append(estimation)
            except:
                try:
                    estimation = driver.find_element_by_xpath("//article[@class='scrollable active css-1ctl34j ead8scz3']/div[1]/div[1]/div[1]/div[1]/div[1]/div[3]/div[1]/div[4]/span[1]/span[1]").text
                    salary_estimate.append(estimation)
                except:
                    salary_estimate.append(0)


        try:
            driver.find_element_by_xpath('.//*[@alt="next-icon"]').click()
            page = page + 1
        except NoSuchElementException:
            print("Scraping terminated before reaching target number of jobs. got {}.".format(page))
        driver.refresh()
        

 

    jobs = pd.DataFrame({"Job Title" : job_title,
    "Salary Estimate" : salary_estimate,
    "Job Description" : job_description,
    #"Publish Date" : publish_date,             
    "Company Name" : company_name})

    return jobs