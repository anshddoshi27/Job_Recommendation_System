

import requests
from bs4 import BeautifulSoup
import pandas as pd 
import seaborn as sns
import numpy as np 
import matplotlib as plt
import re
import json









#built-in-nyc
def get_built_in_nyc_data(base_url="https://www.builtinnyc.com/jobs"):
    built_in_nyc=requests.get(base_url)
    html=built_in_nyc.text
    with open("built_in_nyc_html.txt","w") as file:
        file.write(html)
    #soup=BeautifulSoup(html,"html.parser")
    
    #pagination
        
    #pages=soup.find(id="pagination")
    #num_pages=int(soup.find("a","page-link border rounded fw-bold border-0").text)
     
    fp_data_complete=[]
    all_titles=[]
    all_descriptions=[]
    
    with open("built_in_nyc_html.txt","r") as file:
        html_test=file.read()
    


    
    #
    for page in range(1,71):
        url=f"{base_url}?page={page}"
        built_in_nyc_p=requests.get(url)
        html_p=built_in_nyc_p.text
        soup_p=BeautifulSoup(html_p,"html.parser")
        #get the tags for top and bottom section results
        top_job_lists=soup_p.find(id="search-results-top")
        bottom_job_lists=soup_p.find(id="search-results-bottom")

        #find all header tags in each section as they contain the job-titles
        headers_top=top_job_lists.find_all("h2")
        headers_bottom=bottom_job_lists.find_all("h2")
        headers_top_mains=top_job_lists.find_all(class_="row",id="main") # filter each section before getting all tags with the data as the <div> outside of the main contained repeating data for some reason, part of the link perhaps
        headers_bottom_mains=bottom_job_lists.find_all(class_="row",id="main")
        
         
        
        
        #extract titles
        titles_top=[]
        titles_bottom=[]
        for title in headers_top:
            titles_top.append(title.find("a",class_="card-alias-after-overlay hover-underline link-visited-color text-break").text)
        for title in headers_bottom:
            titles_bottom.append(title.find("a",class_="card-alias-after-overlay hover-underline link-visited-color text-break").text)
        
        
        titles=titles_top
        titles+=titles_bottom
        all_titles.append(titles)
    
    
    
        
    
        
        #extract data by filtering each section to its "main" tags to then find all the span tags that contain the time posted, location, type of work setting, size of company, and average salary data
        
        
        
        header_mains=headers_top_mains
        header_mains+=headers_bottom_mains
        #fetch all the data and then iterate the created nested list with all the data tags and convert them to only show it's text content
        fp_data=[] #front page data
        for data in header_mains: 
            fp_data.append(data.find_all("span","font-barlow text-gray-03"))
    
            
        for data_set in range(len(fp_data)):
            for data in range(len(fp_data[data_set])):
                fp_data[data_set][data]=fp_data[data_set][data].text
        
        #reorder data
        
        
        for dset in range(len(fp_data)):
            set_i=fp_data[dset]
            if len(set_i)<6:
                for empty in range(6-len(set_i)):
                    set_i.append("")
        
        #for dset in fp_data:
          #  print(dset,"\n")
        
        
    
        fp_data_new=[]
        for dset in range(len(fp_data)):
            dset_new={"Time Posted":'',"Location":'',"Job Environment":'',"Company Size":'',"Salary":'',"Years of Experience":''}
            for dp in range(len(fp_data[dset])):
                if "Hours" in fp_data[dset][dp]:
                    dset_new["Time Posted"]=fp_data[dset][dp]
                elif "NY" in fp_data[dset][dp]:
                    dset_new["Location"]=fp_data[dset][dp]
                elif "Remote" in fp_data[dset][dp]:
                    dset_new["Job Environment"]=fp_data[dset][dp]
                elif "Hybrid" in fp_data[dset][dp]: 
                    if fp_data[dset][2]=="Remote":
                        dset_new["Job Environment"]="Both"
                    else:
                        dset_new["Job Environment"]=fp_data[dset][dp]
                elif "Employees" in fp_data[dset][dp]:
                    dset_new["Company Size"]=fp_data[dset][dp]
                elif "Annually" in fp_data[dset][dp]:
                    dset_new["Salary"]=fp_data[dset][dp]
                elif "Experience" in fp_data[dset][dp]:
                    dset_new["Years of Experience"]=fp_data[dset][dp]
            fp_data_new.append(dset_new)
        fp_data_complete.append(fp_data_new)
    
    # get all description links
        top_search_results_d=soup_p.find(class_="job-board bg-gray-01").find(id="jobs-list").find(class_="container").find(id="search-results-top")
        bottom_search_results_d=soup_p.find(class_="job-board bg-gray-01").find(id="jobs-list").find(class_="container").find(id="search-results-bottom")

        top_jobs_d=top_search_results_d.find_all("h2")
        bottom_jobs_d=bottom_search_results_d.find_all("h2")
        top_jobs_d+=bottom_jobs_d
        jobs_d=top_jobs_d
    
        hrefs=[]
        for header in jobs_d:
            links = header.find_all("a")
            for link in links:
             hrefs.append(link.get('href'))
        descriptions=[]
        for href in hrefs:
            link="https://builtinnyc.com"+str(href)
            descriptions.append(description_getter(link))
        all_descriptions.append(descriptions)
    
    
    
    
    
    
    
    
    #add the page's job data and titles to the final list
    
    
    #######################        
    #add titles
    
               
# flatten all data so its just lists of jobs data or titles    
    fp_data_complete_flattened=[] 
    for p in fp_data_complete:
        for job in p:
            fp_data_complete_flattened.append(job)
    all_titles_flattened=[]
    for ts in all_titles:
        for t in ts:
            all_titles_flattened.append(t)
    all_descriptions_flattened=[]
    for dl in all_descriptions:
        for l in dl:
            all_descriptions_flattened.append(l)
    
            
    
#merge data and tiltes

    for i in range(len(fp_data_complete_flattened)):   
        dset=fp_data_complete_flattened[i]
        dset["Title"]=all_titles_flattened[i]
    
    
    

    
    for i in range(len(fp_data_complete_flattened)):
        dset=fp_data_complete_flattened[i]
        dset["Description"]=all_descriptions_flattened[i]
    
    with open("job_data_base.json","w") as f2:
        json.dump(fp_data_complete_flattened,f2)
    
        
    
        
       
    built_in_nyc_dataframe=pd.DataFrame(fp_data_complete_flattened)
    #built_in_nyc_dataframe.to_csv("built_in_nyc_front_page_data.csv")

    return built_in_nyc_dataframe
             
        
        
     #test case : hours, ny, employe,salary,exp           
        
    #now all data is saved in 2 nested lists, data_top and data_bottom
        
        
    
    
        #for s in range(len(data_top))
    

def update_data_built_in_nyc():
    
    both_frames=pd.concat([pd.read_csv("built_in_nyc_data_base.csv"),get_built_in_nyc_data()],ignore_index=True)
    both_frames.to_csv("built_in_nyc_data_base.csv",index=False)
    drop_duplicates_for_csv_file("built_in_nyc_data_base.csv")
    print("Data Updated") 
    
def initialize_a_data_base_built_in_nyc():
    get_built_in_nyc_data().to_csv("built_in_nyc_data_base.csv",index=False)
    print("initialized")
        
def test_duplicate():
    existing_data = pd.read_csv("built_in_nyc_data_base.csv")
    
    # Define new rows as dictionaries
    d1 = {"Time Posted": '3 Hours Ago', "Location": 'New York, NY', "Job Environment": 'Hybrid', "Company Size": '16,000 Employees', "Salary": '59K-60K Annually', "Years of Experience": '1-3 Years of Experience', "Title": "Wholesale Planning Analyst - Amazon"}
    d2 = {"Time Posted": '23 Hours Ago', "Location": 'New York, NY', "Job Environment": 'Hybrid', "Company Size": '16,000 Employees', "Salary": '68K-90K Annually', "Years of Experience": '1-3 Years of Experience', "Title": "Sr. Analyst, Sustainability Trade Compliance - Coachtopia"}
    
    # Convert dictionaries to DataFrames without specifying index
    new_data = pd.DataFrame([d1, d2])
    
    # Concatenate with existing data
    test_frame = pd.concat([existing_data, new_data],ignore_index=True)
    
    # Save the concatenated DataFrame to the CSV
    test_frame.to_csv("built_in_nyc_data_base.csv",index=False)
    
    print("Data Updated")
    
def drop_duplicates_for_csv_file(csv_file):
    duplicateless=pd.read_csv(csv_file).drop_duplicates(subset=["Title","Salary","Years of Experience"])
    duplicateless.to_csv(csv_file,index=False)

def eliminate_index():
    index_data_frame=pd.read_csv("built_in_nyc_data_base.csv")
    #index_less_frame=index_data_frame.
    index_data_frame.to_csv('built_in_nyc_data_base.csv', index=False)

def read_as_df_built_in_nyc():
    return pd.read_csv("built_in_nyc_data_base.csv")

def check_duplicates():
    duplicates=pd.read_csv("built_in_nyc_data_base.csv").duplicated(subset=["Title","Salary","Years of Experience"])
    for value in duplicates:
        if value==True:
            verdict="Duplicate Found!"
            break
        else:
            verdict="No Duplicates!"
            continue
    print(verdict)
        
    
def descriptions_getter_tester(html_file='built_in_nyc_html.txt'):
    with open(html_file,"r") as f:
        content=f.read()
    return content

def description_getter(url_d):
    job_url_html=requests.get(url_d).text
    with open("built_in_nyc_html.txt","r") as file:
        html_test=file.read()
    soup_description=BeautifulSoup(job_url_html,"html5lib")
    container=soup_description.find(class_="container py-lg").find(class_="col-12 col-lg-6 mb-sm mb-lg-0").find(class_="fs-md fw-regular mb-md html-parsed-content")
    sets_of_bp=container.find_all("ul")
    qualification_list=[]
    for i in sets_of_bp:
        qualification_list.append(i.find_all("li"))
        
    
    
    cleaned_qualifications=[]
    for qualification_set in qualification_list:
        cleaned_qualification_set=[]
        for item in qualification_set:
        
            bp = str(item)  # Convert the item to a string
            bp = re.sub('<.*?>', '', bp)  # Remove all HTML tags]
            cleaned_qualification_set.append(bp.strip())
        cleaned_qualifications.append(cleaned_qualification_set)  # Add the cleaned string to the list
            

    return cleaned_qualifications
        
    
    
      
          


    

    
    
    

        
    


                












    
    
    
    
    
