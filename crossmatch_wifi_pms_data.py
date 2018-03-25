"""
crossmatch_wifi_pms_data.py
"""

import csv
from Levenshtein import jaro_winkler
from prettytable import PrettyTable
import datetime


"""
GLOBAL VARIABLES
"""
# Define genuine match threshold
match_threshold = 0.8


# If no prefix weight is explicitly specified then 0.1 is the default
# to consider the strings *identical*
def calculate_similarity(string_1, string_2):
 return jaro_winkler(string_1, string_2) 

def is_empty(string):
 return not bool(string.strip()) 

def write_data_csv(data, filename):
 with open(filename,'w', newline='') as plotting_file:
  fieldnames = list(data[0].keys())

  writer = csv.DictWriter(plotting_file, fieldnames = fieldnames)
 
  writer.writeheader()
  writer.writerows(data)

def add_timestamp():
 return datetime.datetime.now().strftime('%Y%m%d%H%M%S')

def analyse_similarity_data(pms_input_filename, wifi_input_filename):
 # List with similarity measures for plotting
 sim_analysis_list = []
 
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
		 sim_last_name) / 2
  
      if sim_mean >= match_threshold:
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

       sim_analysis_list.append(plotting_record)

      elif sim_mean < match_threshold and sim_mean >= 0.5:
       if sim_firstname_to_username >= 0.75 or sim_lastname_to_username >= 0.75:       
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

        sim_analysis_list.append(plotting_record)
 
 return sim_analysis_list

def crossmatch_data(pms_input_filename, wifi_input_filename):
 # PrettyTable for Console Output
 table = PrettyTable(['pms_first_name', 'pms_last_name','sim_mean', 'name_matched'])

 # List with reservation records and merged email address
 merged_output = []

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
		 sim_last_name) / 2
  
      if sim_mean >= match_threshold:
       tmp_reservation = reservation
       tmp_reservation['EMAIL '] = wifi_record['email']
       merged_output.append(tmp_reservation)

       table.add_row([pms_first_name, pms_last_name,sim_mean,'straight_match'])      

      elif sim_mean < match_threshold and sim_mean >= 0.5:
       if sim_firstname_to_username >= 0.75 or sim_lastname_to_username >= 0.75:       
        tmp_reservation = reservation
        tmp_reservation['EMAIL '] = wifi_record['email']
        merged_output.append(tmp_reservation)

        table.add_row([pms_first_name, pms_last_name,sim_mean,'email_weight'])      

 print(table)
 
 return merged_output

if __name__ == "__main__":
 print("Start program...")
 # Specify input name for PMS data source
 pms_input_filename = 'in/SENT_PA_2702_v0.1.csv'

 # Specify input name for Wifi signup data
 wifi_input_filename = 'in/Sentosa_First_Wifi_session_data_27.02.csv'

 # Write Plotting CSV
 #sim_plotting_list = analyse_similarity_data(pms_input_filename, wifi_input_filename)
 #write_data_csv(sim_plotting_list,'out/plotting{}.csv'.format(add_timestamp()))

 # Write Output CSV
 merged_output = crossmatch_data(pms_input_filename, wifi_input_filename)
 write_data_csv(merged_output,'out/merged_output{}.csv'.format(add_timestamp()))

 print('End of program')
