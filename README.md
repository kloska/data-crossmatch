# Data Crossmatch

Script for taking a standardized Oracle PMS export (for this use-case) as the first input data and a generated wifi data export as the second input file.

The output file is a copy of the PMS data with email addresses and/or mobile numbers copied from the wifi data.

## Prerequisites


### Input

The input files are expected to be located in the `/in` subfolder. 

Structure of the PMS data (for this use-case):

```
['ARRIVAL DATE', 'ROOM NO ', 'VIP CODE', 'MEMBERSHIP TYPE', 'LAST NAME', 'FIRST NAME', 'TITLE', 'COMPANY/AGENT', 'ARRIVAL DATE2', 'DEPARTURE DATE', 'ARRIVAL TIME', 'ROOM TYPE', 'ADULTS', 'CHILD','VISITS', 'EMAIL ', 'CONFIRMATION NUMBER', 'PHONE NUMBER', 'PHONE NUMBER', 'RATE CODE', 'SPECIAL CODES', 'SPECIAL CODES', 'SPECIAL CODES']
```

Structure of the Wifi data:
```
['first_name', 'last_name', 'email', 'mobile_number', 'first_wifi_session_date']
```

### Approximate Name Matching

Contact information are only merged and assumed as a match if:
 * Unique record in the Wifi data exists for matching only with one person (first name and last name) of the PMS data
 * First Wifi Session Date matches with the arrival date of the pms data
 * Eventually contains parts of the first name and last name in the email address
