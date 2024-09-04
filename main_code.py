import json
import pandas as pd
import requests
import re
from bs4 import BeautifulSoup








with open("/Users/3017387smacbookm/Documents/Python/Python_Project_Files/JOB_VACANCY_SOURCING_PROJECT/job_data_base.json","r") as file:  
    data_base=json.load(file)



description_dict=[]
# make description subdata with priprity p initialied


        
#test_description=["python","c","java"] # comapny_data["Description"] should be a list of descriptions


for company_data in data_base:
    dset_new={"Company":"","Description":[],"Priority_Percentage":0}
    dset_new["Company"]=str(company_data["Title"])
    dset_new["Description"]=company_data["Description"]
    description_dict.append(dset_new)
    


userskills=[]
#skills_lacking_list=[]
#main code

skillset=[]


# user clicking qualifications and data being generated -> lists userskills, and skills_lacking list

for cc_number,company_card in enumerate(description_dict):
    print(f"{company_card["Company"]}\n")
    for set_index,set_skill in enumerate(company_card["Description"]):
        print(set_index)
        for index,skill in enumerate(set_skill):
            print(index,skill)
        print()
            

    which_set=int(input("Which set are the skills:"))
    for index,skill in enumerate(company_card["Description"][which_set]):
        print(index,skill)
    
    print("\n")
    
    numbers=input("Press the numbers of the skills you attain: ")
    if numbers=="escape":
        break
    elif numbers=="delete":
        data_base.remove(data_base[cc_number])
        
        continue
        
    else:
        numbers=numbers.split(",")
    
        #numbers=[int(digit) for digit in str(numbers)]  
        for i in description_dict:
            i["Priority_Percentage"]=len(numbers)/len(i["Description"][which_set])

        company_description=company_card["Description"]
        for n in numbers:
            skillset.append(company_description[which_set][int(n)])
        #skills_lacking=set(skillset) ^ set(i) #get the uncommon stuff
        
        userskills.append(skillset)
        #skills_lacking_list.append(skills_lacking)


    
    
    
    print("\n--------------------------------------------------------------------------------------------------------------------\n")
    
    
    
       
        


    
    

companies_ranked2 = []
percentages = []
maxy = 0
seen_companies = set()  # Set to track companies already added

# Iterate over description_dict to populate companies_ranked2
for company_data in description_dict:
    dset_new = {"Company": "", "Priority_Percentage": ""}
    percentage = company_data["Priority_Percentage"]

    if percentage > maxy:
        maxy = percentage
        dset_new["Company"] = company_data["Company"]
        dset_new["Priority_Percentage"] = company_data["Priority_Percentage"]
        if dset_new["Company"] not in seen_companies:
            companies_ranked2.append(dset_new)
            seen_companies.add(dset_new["Company"])
    elif percentage == maxy:
        # Add company only if it hasn't been added already
        if company_data["Company"] not in seen_companies:
            dset_new["Company"] = company_data["Company"]
            dset_new["Priority_Percentage"] = company_data["Priority_Percentage"]
            companies_ranked2.append(dset_new)
            seen_companies.add(company_data["Company"])
companies_ranked2.reverse()

#update data for next run

with open("/Users/3017387smacbookm/Documents/Python/Python_Project_Files/JOB_VACANCY_SOURCING_PROJECT/job_data_base.json","w") as file:
    json.dump(data_base,file)

    
      

# Create DataFrame and save to CSV
user_priority_jobs = pd.DataFrame(companies_ranked2)
user_priority_jobs.to_csv("/Users/3017387smacbookm/Documents/Python/Python_Project_Files/user_priority_jobs.csv",index=False)

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
   
   
   
   
   
   
   
   
   









