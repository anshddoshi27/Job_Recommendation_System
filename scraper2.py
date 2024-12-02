import requests
from bs4 import BeautifulSoup
import pandas as pd 
import seaborn as sns
import numpy as np 
import matplotlib as plt
import re
import json


#built-in-nyc
def get_tech_nyc_jobs_scraper(base_url="https://motionrecruitment.com/tech-jobs?__hstc=149880873.f22ad4e11e4b7189b2a4e837e1817d57.1732757146459.1732757146459.1732757146459.1&__hssc=149880873.1.1732757146459&__hsfp=810579359"):
    #built_in_nyc=requests.get(base_url)
    #html=built_in_nyc.text
   # with open("tmotion","w") as file:
        #file.write(html)
    #soup=BeautifulSoup(html,"html.parser")
    
    #pagination
        
    #pages=soup.find(id="pagination")
    #num_pages=int(soup.find("a","page-link border rounded fw-bold border-0").text)
     
    fp_data_complete=[]
    all_descriptions=[]
    
    
    
    for page in range(0,60): # 60 pages 
        
        page_url_number=0
        if page_url_number==0:
            pageurl=base_url
        else:
            additional_url=f"&start={page_url_number}"
            pageurl=base_url+additional_url
            page_url_number+=20
    
        ###### Get page html parsed #####
        #  real_code      html_content_file=requests.get(pageurl).text
        with open("tmotion.txt","r") as file:
            html_content_file=file.read()
        
        
        ##### get links from page ####
        
        soup=BeautifulSoup(html_content_file,"html.parser")
        job_container=soup.find(class_="JobsList_list__oxiOj")
        job_cards=job_container.find_all(class_="JobItem_jobItem__IZ5bL")
        job_cards_attribute_tag=[i.find("a") for i in job_cards]
        job_links=[i.get("href") for i in job_cards_attribute_tag]
        
        ##### store links in links_for_page ###
        links_for_page=[]
        for link in job_links:
            links_for_page.append(link)
            
        #### scraping job data from each link
        fp_data=[]    # list of job data dicts for the page that the for loop is iterating on
        def description_getter():
            """ gets titles and it's respective set of bullet points and formats them together 

            Returns:
                list: _description_
            """
            sets_bullet_points=job_soup.find(class_="Job_jobDescription__oK2XH").find_all("ul") # gets containers that has all the bullet points for each title
            description=[] # list of title with bullet points for each part of the description
            cleaned_qualifications=[]
            for qualification_set in sets_bullet_points: # iterates through each container and extracts bullet points and cleans them
                qualification_set=qualification_set.find_all("li") #modifies list to be just a list of lists of bullet points
                cleaned_qualification_set=[]
                for item in qualification_set:
                    bp = str(item)  # Convert the item to a string
                    bp = re.sub('<.*?>', '', bp)  # Remove all HTML tags]
                    cleaned_qualification_set.append(bp.strip())
                cleaned_qualifications.append(cleaned_qualification_set)  # Add the cleaned string to the list
                                    
                description.append(str(cleaned_qualifications)) # merges title with the according set of bps and adds that to a list
            
            
                    
            return cleaned_qualifications
        for job_card_link in links_for_page:
            job_site_html=requests.get("https://motionrecruitment.com"+job_card_link).text # get html for the joblink
            job_soup=BeautifulSoup(job_site_html,"html.parser") # get the html's soup
            dset={"Job Title":"","Location":"","Job Environment":"","Salary":"","Description":""} # initialize a dict that will hold the job data and all its parameters
            dset["Job Title"]=job_soup.find(class_="Job_jobInfo___HBWC").find("h1").text # find job title
            dset["Location"]=job_soup.find(class_="JobDetails_jobDetailsWrapper__SJAAi").find(class_="JobDetailsItem_jobDetailsText__TwBM4").text # add location
            dset["Job Environment"]= job_soup.find(class_="JobDetails_jobDetailsWrapper__SJAAi").find(class_="JobDetails_jobDetails__uN5Zr").find("b").text # add job tytpe
            job_detail_container = job_soup.find(class_="JobDetails_jobDetailsWrapper__SJAAi").find(class_="JobDetails_jobDetails__uN5Zr").find_all(class_="JobDetailsItem_jobDetails__Ft9g4")
            salary=False
            for i in job_detail_container:
                if "$" in i.find(class_="JobDetailsItem_jobDetailsText__TwBM4").text:
                    salary=True
                else:
                    continue
            if salary == True:
                salary=i.find(class_="JobDetailsItem_jobDetailsText__TwBM4").text
            else:
                salary="Not Specified"
            dset["Salary"]=salary# add salary
            dset["Description"]=description_getter() # saves whole description with right format
            job_data=dset.copy()
            fp_data.append(job_data)
        
    #fp_data has a list of all job data on a page
    
        fp_data_complete.append(fp_data)
    
    #fp_data_complete_is a list of lists of job data for all pages
    
    fp_data_complete_flattened=[] 
    for p in fp_data_complete:
        for job in p:
            fp_data_complete_flattened.append(job)
        
    with open("job_data_base.json","w") as f2:
        json.dump(fp_data_complete_flattened,f2)

       
    tmotion_data_frame=pd.DataFrame(fp_data_complete_flattened)
    

    
    return tmotion_data_frame
            
            
            
            
            
   #print data to csv 

get_tech_nyc_jobs_scraper().to_csv("tmotion_data.csv")  
