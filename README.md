This program manages a data base of the most popular tech jobs listed on the internet, gathering each Job's title, Environment, Size, Avg. Salary, Years of Experience required, and it's description & qualifications.

THE DATA IS TOO LARGE SO HERE ARE THE LINKS TO THE DATABASE LAST UPDATED IN OCTOBER (CSV AND JSON): 
  Csv: https://drive.google.com/file/d/1z-Up9mLEg26Qrx_B85lLlfjPWmDP-TIV/view?usp=sharing
  Json: https://drive.google.com/file/d/1G1aHo84T3VDsPBkLzxPuXrJhDw-A5pwk/view?usp=sharing

This program:

              - Scrapes Job Data from websites (as of now, just https://motionrecruitment.com)
              - Interfaces User by displaying different job's and their description and qualification to then ask what skills the user has from the listed qualifications
              - Keeps userskills in memory to then generate list of all jobs ranked based on the percentage of skills the user has the job.

scaper2.py contains the functions that gather all the job data
main_code is the main program.

