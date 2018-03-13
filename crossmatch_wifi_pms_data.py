"""
crossmatch_wifi_pms_data.py

Script for taking an standardized Oracle PMS export as the source input and a SQL query generated csv file consisting of names, dates, email addresses and mobile numbers as a second input file.
The output file is a copy of the PMS data with email addresses and/or mobile numbers merged from the WiFI signup data. 
Contact information are only merged and assumed as a match if:
 (1) Unique record in the Wifi data exists for matching only with one person (first name and last name) of the PMS data
 (2) First Wifi Session Date matches with the arrival date of the pms data
 (3) Eventually contains parts of the first name and last name in the email address
  
Assumption: Wifi login data ordered alphabetically 
"""

import csv
from Levenshtein import jaro_winkler
from prettytable import PrettyTable

# If no prefix weight is explicitly specified then 0.1 is the default
# to consider the strings *identical*
def calculate_similarity(string_1, string_2):
 return jaro_winkler(string_1, string_2) 

def is_empty(string):
 return not bool(string.strip()) 

def write_plotting_data(data):
 with open('plotting.csv','w', newline='') as plotting_file:
  fieldnames = list(data[0].keys())

  writer = csv.DictWriter(plotting_file, fieldnames = fieldnames)
 
  writer.writeheader()
  writer.writerows(data)

# Specify input name for PMS data source
pms_input_filename = 'SENT_PA_2702_v0.1.csv'

# Specify input name for Wifi signup data
wifi_input_filename = 'Sentosa_First_Wifi_session_data_27.02.csv'

print("Start program...")

# List with similarity measures for plotting
sim_plotting_list = []

table = PrettyTable(['pms_first_name', 'pms_last_name','sim_first_name','sim_last_name','sim_firsname_to_email','sim_lastname_to_email'])

with open(pms_input_filename, newline='') as pms_data:
 pms_file_reader = csv.DictReader(pms_data)
 print("Working with following PMS header set: \n {}".format(pms_file_reader.fieldnames))

 for reservation in pms_file_reader: 
  pms_first_name = reservation['FIRST NAME']
  pms_last_name = reservation['LAST NAME']
  pms_email = reservation['EMAIL '].strip()

  if is_empty(pms_email):
   with open(wifi_input_filename, newline='') as wifi_data:
    wifi_file_reader = csv.DictReader(wifi_data)
    
    for wifi_record in wifi_file_reader:
     wifi_first_name = wifi_record['first_name']
     wifi_last_name = wifi_record['last_name']
     email_at_index = wifi_record['email'].find('@')
     wifi_email_username = wifi_record['email'][0:email_at_index]

     # Calculate similarity measures
     sim_first_name =  calculate_similarity(pms_first_name, wifi_first_name)
     sim_last_name =  calculate_similarity(pms_last_name, wifi_last_name)
     sim_firstname_to_username =  calculate_similarity(pms_first_name, wifi_email_username)
     sim_lastname_to_username = calculate_similarity(pms_last_name, wifi_email_username)

     sim_mean = (sim_first_name + 
           	sim_last_name + 
          	sim_firstname_to_username) / 3

     #print('Similarity Measure between first name {} and {} : {}'.format(pmsFirstName, wifiFirstName, simPmsXWifiFirstName))     
     #print('Similarity Measure between last name {} and {} : {}'.format(pmsLastName, wifiLastName,simPmsXWifiLastName)) 
    # print('Similarity Measure between username {} and {} : {}'.format(pmsFirstName, wifiEmailUsername, simPmsXWifiUsername ))
     
     if sim_mean >= 0.65:
      #print('Identified record for {} with a mean similarity measure of : {}'.format(pms_first_name, sim_mean))
      
      table.add_row([pms_first_name, pms_last_name,sim_first_name,sim_last_name,sim_firstname_to_username,sim_lastname_to_username])      

      # Build data for plotting
      plotting_record = {}
      plotting_record['pms_first_name'] = pms_first_name
      plotting_record['pms_last_name'] = pms_last_name
      plotting_record['wifi_first_name'] = wifi_first_name
      plotting_record['wifi_last_name'] = wifi_last_name
      plotting_record['wifi_email_username'] = wifi_email_username
      plotting_record['sim_first_name'] = sim_first_name
      plotting_record['sim_last_name'] = sim_last_name
      plotting_record['sim_first_name_to_email'] = sim_firstname_to_username
      plotting_record['sim_last_name_to_email'] = sim_lastname_to_username
      plotting_record['sim_mean_value'] = sim_mean

      sim_plotting_list.append(plotting_record)

print(table)

# Write Plotting CSV
write_plotting_data(sim_plotting_list)

print('End of program')

