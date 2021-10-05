#New Stock Simulator - With industries and stock prices retrieved via web-scraping

import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import yfinance as yf
from datetime import datetime, date, time, timedelta
import webbrowser
import matplotlib.pyplot as plt
import os.path

file_exists = os.path.isfile('user_data.csv')
with open ('user_data.csv', 'a') as csvfile:
    headers = ['Date of Account Creation', 'Time of Account Creation', 'Username', 'Password']
    writer = csv.DictWriter(csvfile, delimiter = ',', lineterminator = '\n', fieldnames = headers)

    if not file_exists:
        writer.writeheader()
        
    else:
        pass

while True:
    try:
        account = input("""Hello! Welcome to the stock simulator!
[L] - Log In
[S] - Sign Up: """)

        if account == "S":
            while True:
                try:            
                    filename = "user_data.csv"
                    username = input("""We're glad to see your interest in signing up!
Please enter your desired username (Minimum 4 characters & Case-Sensitive)
Alternatively, press B to go back: """)
                
                    if username.upper() == "B":
                        break
                    
                    elif len(username) <4:
                        print()
                        print("Please enter a minimum of 4 characters!")
                        continue
                   
                    else:
                        usernames_df = pd.read_csv("user_data.csv")
                        list_of_usernames = usernames_df['Username'].tolist()
                        list_of_passwords = usernames_df['Password'].tolist()
                        
                        if username in list_of_usernames:
                            print()
                            print("""Sorry, that username has already been taken.
If it is yours, please choose the login option, or select a different username: """)
                            continue
                                
                        else:
                            print()
                            confirm_username = input(f"""Username '{username}' is available!
[C] - To confirm selection
[D] - To enter a different username: """).upper()
                
                            if confirm_username == "D":
                                continue
                            
                            elif confirm_username == "C":
                                while True:
                                    try:
                                        print()
                                
                                        password = input("Please choose a password for this account: ")
                                
                                        confirm_password = input(f"""Please confirm that you'd like to go with {password} as your password
[Y] - Yes
[N] - No: """).upper()
                                
                                        if confirm_password == "Y":
                                            moment = datetime.now()
                                            datenow = moment.strftime("%d/%m/%y")
                                            timenow = moment.strftime("%H:%M")
                                        
                                            with open(filename, "a", newline="") as file_pointer:
                                                csv_pointer = csv.writer(file_pointer)
                                                row = [datenow, timenow, username, password]
                                                csv_pointer.writerow(row)
                                                
                                            print("Your account has been sucessfully created! You can start trading now")
                                            break_to_start = 1
                                            break
                                     
                                        elif confirm_password == "N":
                                            print()
                                            print("No worries, please enter your desired password now: ")
                                            continue
                                        
                                        if break_to_start == 1:
                                            break
                                        
                                    except:
                                        print()
                                        print("Your input is unsupported. Please provide a proper input")
                
                    if break_to_start == 1:
                        break
                    
                except:
                    print()
                    print("Invalid input, please try again")
        
        elif account == "L":
            while True:
                try:
                    username_login = input("""Glad to see you're back! Please enter your username.
Alternatively, press [B] to go back: """)
                    
                    usernames_df = pd.read_csv("user_data.csv")
                    list_of_usernames = usernames_df['Username'].tolist()
                    list_of_passwords = usernames_df['Password'].tolist()
                    
                    if username_login.upper() == "B":
                        break
                    
                    elif len(username_login) < 4:
                        print()
                        print("Usernames with less than 4 characters are not allowed, please try again!")
                        continue
                    
                    elif username_login not in list_of_usernames:
                        print()
                        print("That username was not found. Please re-enter a correct one, or sign up!")
                        continue
                    
                    else:
                        print()
                        password_login = input(f"""Welcome back {username_login}!
Please enter your password: """)
        
                        if password_login == list_of_passwords[list_of_usernames.index(username_login)]:
                            print()
                            print("Your password matches! Welcome")
                            print("Loading...")
                            break_to_start = 1
                            break                                
                            
                        else:
                            print()
                            print("Your entered password is incorrect, please try again")
                            continue
                    if break_to_start == 1:
                        break
                    
                except:
                    print()
                    print("Please enter a valid input")
        
        if break_to_start == 1:
            break
        
        else:
            print()
            print("Please choose only from [L] or [S]")    
        
    except:
        print()
        print("Please choose only from [S] or [L]!")

pd.options.display.float_format = '{:,.2f}'.format
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

today = date.today() 

portfolio_value = 25000 #Starting Amount
money_change_long = 0
money_change_short = 0

c=0 #To know which iteration of the simulator we're in
break_to_main_menu = 0 #Used to break between loops, ignore
exit_short_to_main_menu = 0
exit_long_to_main_menu = 0

exit_initial_choice = 0

#For industry choice 1 - Energy
prices1 = []
tickers1 = []
names1 = []
changes1 = []
percentChanges1 = []
marketCaps1 = []
totalVolumes1 = []

EnergyUrl = "https://sg.finance.yahoo.com/industries/energy"
r = requests.get(EnergyUrl)
data = r.text
soup = BeautifulSoup(data, features = "lxml")
 
counter = 40
for i in range(40, 404, 14):
    for listing in soup.find_all('tr'):
        for ticker in listing.find_all('td', attrs = {'aria-label': 'Symbol'}):
            tickers1.append(ticker.text)
        for name in listing.find_all('td', attrs = {'aria-label': 'Name'}):
            names1.append(name.text)
        for price in listing.find_all('td', attrs = {'aria-label': 'Last price'}):
            prices1.append(price.text)
        for change in listing.find_all('td', attrs = {'aria-label': 'Change'}):
            changes1.append(change.text)
        for pchange in listing.find_all('td', attrs = {'aria-label': '% change'}):
            percentChanges1.append(pchange.text)
        for cap in listing.find_all('td', attrs = {'aria-label': 'Market cap'}):
            marketCaps1.append(cap.text)
        for volume in listing.find_all('td', attrs = {'aria-label': 'Volume'}):
            totalVolumes1.append(volume.text)

#For industry choice 2 - Financial Services
prices2 = []
tickers2 = []
names2 = []
changes2 = []
percentChanges2 = []
marketCaps2 = []
totalVolumes2 = []
 
FinancialUrl = "https://sg.finance.yahoo.com/industries/financial"
r = requests.get(FinancialUrl)
data = r.text
soup = BeautifulSoup(data, features = "lxml")
 
counter = 40
for i in range(40, 404, 14):
    for listing in soup.find_all('tr'):
        for ticker in listing.find_all('td', attrs = {'aria-label': 'Symbol'}):
            tickers2.append(ticker.text)
        for name in listing.find_all('td', attrs = {'aria-label': 'Name'}):
            names2.append(name.text)
        for price in listing.find_all('td', attrs = {'aria-label': 'Last price'}):
            prices2.append(price.text)
        for change in listing.find_all('td', attrs = {'aria-label': 'Change'}):
            changes2.append(change.text)
        for pchange in listing.find_all('td', attrs = {'aria-label': '% change'}):
            percentChanges2.append(pchange.text)
        for cap in listing.find_all('td', attrs = {'aria-label': 'Market cap'}):
            marketCaps2.append(cap.text)
        for volume in listing.find_all('td', attrs = {'aria-label': 'Volume'}):
            totalVolumes2.append(volume.text)


#For industry choice 3 - Healthcare
prices3 = []
tickers3 = []
names3 = []
changes3 = []
percentChanges3 = []
marketCaps3 = []
totalVolumes3 = []

HealthUrl = "https://sg.finance.yahoo.com/industries/healthcare"
r = requests.get(HealthUrl)
data = r.text
soup = BeautifulSoup(data, features = "lxml")
 
counter = 40
for i in range(40, 404, 14):
    for listing in soup.find_all('tr'):
        for ticker in listing.find_all('td', attrs = {'aria-label': 'Symbol'}):
            tickers3.append(ticker.text)
        for name in listing.find_all('td', attrs = {'aria-label': 'Name'}):
            names3.append(name.text)
        for price in listing.find_all('td', attrs = {'aria-label': 'Last price'}):
            prices3.append(price.text)
        for change in listing.find_all('td', attrs = {'aria-label': 'Change'}):
            changes3.append(change.text)
        for pchange in listing.find_all('td', attrs = {'aria-label': '% change'}):
            percentChanges3.append(pchange.text)
        for cap in listing.find_all('td', attrs = {'aria-label': 'Market cap'}):
            marketCaps3.append(cap.text)
        for volume in listing.find_all('td', attrs = {'aria-label': 'Volume'}):
            totalVolumes3.append(volume.text)
                        

#For industry choice 4 - Business Services
prices4 = []
tickers4 = []
names4 = []
changes4 = []
percentChanges4 = []
marketCaps4 = []
totalVolumes4 = []

bizUrl = "https://sg.finance.yahoo.com/industries/business_services"
r = requests.get(bizUrl)
data = r.text
soup = BeautifulSoup(data, features = "lxml")
 
counter = 40
for i in range(40, 404, 14):
    for listing in soup.find_all('tr'):
        for ticker in listing.find_all('td', attrs = {'aria-label': 'Symbol'}):
            tickers4.append(ticker.text)
        for name in listing.find_all('td', attrs = {'aria-label': 'Name'}):
            names4.append(name.text)
        for price in listing.find_all('td', attrs = {'aria-label': 'Last price'}):
            prices4.append(price.text)
        for change in listing.find_all('td', attrs = {'aria-label': 'Change'}):
            changes4.append(change.text)
        for pchange in listing.find_all('td', attrs = {'aria-label': '% change'}):
            percentChanges4.append(pchange.text)
        for cap in listing.find_all('td', attrs = {'aria-label': 'Market cap'}):
            marketCaps4.append(cap.text)
        for volume in listing.find_all('td', attrs = {'aria-label': 'Volume'}):
            totalVolumes4.append(volume.text)
                        

#For industry choice 5 - Telecoms & Utilities
prices5 = []
tickers5 = []
names5 = []
changes5 = []
percentChanges5 = []
marketCaps5 = []
totalVolumes5 = []

TelcoUrl = "https://sg.finance.yahoo.com/industries/telecom_utilities"
r = requests.get(TelcoUrl)
data = r.text
soup = BeautifulSoup(data, features = "lxml")
 
counter = 40
for i in range(40, 404, 14):
    for listing in soup.find_all('tr'):
        for ticker in listing.find_all('td', attrs = {'aria-label': 'Symbol'}):
            tickers5.append(ticker.text)
        for name in listing.find_all('td', attrs = {'aria-label': 'Name'}):
            names5.append(name.text)
        for price in listing.find_all('td', attrs = {'aria-label': 'Last price'}):
            prices5.append(price.text)
        for change in listing.find_all('td', attrs = {'aria-label': 'Change'}):
            changes5.append(change.text)
        for pchange in listing.find_all('td', attrs = {'aria-label': '% change'}):
            percentChanges5.append(pchange.text)
        for cap in listing.find_all('td', attrs = {'aria-label': 'Market cap'}):
            marketCaps5.append(cap.text)
        for volume in listing.find_all('td', attrs = {'aria-label': 'Volume'}):
            totalVolumes5.append(volume.text)

#For industry choice 6 - Computer Hardware & Electronics
prices6 = []
tickers6 = []
names6 = []
changes6 = []
percentChanges6 = []
marketCaps6 = []
totalVolumes6 = []

HWEUrl = "https://sg.finance.yahoo.com/industries/hardware_electronics"
r = requests.get(HWEUrl)
data = r.text
soup = BeautifulSoup(data, features = "lxml")
 
counter = 40
for i in range(40, 404, 14):
    for listing in soup.find_all('tr'):
        for ticker in listing.find_all('td', attrs = {'aria-label': 'Symbol'}):
            tickers6.append(ticker.text)
        for name in listing.find_all('td', attrs = {'aria-label': 'Name'}):
            names6.append(name.text)
        for price in listing.find_all('td', attrs = {'aria-label': 'Last price'}):
            prices6.append(price.text)
        for change in listing.find_all('td', attrs = {'aria-label': 'Change'}):
            changes6.append(change.text)
        for pchange in listing.find_all('td', attrs = {'aria-label': '% change'}):
            percentChanges6.append(pchange.text)
        for cap in listing.find_all('td', attrs = {'aria-label': 'Market cap'}):
            marketCaps6.append(cap.text)
        for volume in listing.find_all('td', attrs = {'aria-label': 'Volume'}):
            totalVolumes6.append(volume.text)


#For industry choice 7 - Computer Software & Services
prices7 = []
tickers7 = []
names7 = []
changes7 = []
percentChanges7 = []
marketCaps7 = []
totalVolumes7 = []

CSSUrl = "https://sg.finance.yahoo.com/industries/software_services"
r = requests.get(CSSUrl)
data = r.text
soup = BeautifulSoup(data, features = "lxml")
 
counter = 40
for i in range(40, 404, 14):
    for listing in soup.find_all('tr'):
        for ticker in listing.find_all('td', attrs = {'aria-label': 'Symbol'}):
            tickers7.append(ticker.text)
        for name in listing.find_all('td', attrs = {'aria-label': 'Name'}):
            names7.append(name.text)
        for price in listing.find_all('td', attrs = {'aria-label': 'Last price'}):
            prices7.append(price.text)
        for change in listing.find_all('td', attrs = {'aria-label': 'Change'}):
            changes7.append(change.text)
        for pchange in listing.find_all('td', attrs = {'aria-label': '% change'}):
            percentChanges7.append(pchange.text)
        for cap in listing.find_all('td', attrs = {'aria-label': 'Market cap'}):
            marketCaps7.append(cap.text)
        for volume in listing.find_all('td', attrs = {'aria-label': 'Volume'}):
            totalVolumes7.append(volume.text)

#For industry choice 8 - Manufacturing & Materials
prices8 = []
tickers8 = []
names8 = []
changes8 = []
percentChanges8 = []
marketCaps8 = []
totalVolumes8 = []

ManuUrl = "https://sg.finance.yahoo.com/industries/manufacturing_materials"
r = requests.get(ManuUrl)
data = r.text
soup = BeautifulSoup(data, features = "lxml")
 
counter = 40
for i in range(40, 404, 14):
    for listing in soup.find_all('tr'):
        for ticker in listing.find_all('td', attrs = {'aria-label': 'Symbol'}):
            tickers8.append(ticker.text)
        for name in listing.find_all('td', attrs = {'aria-label': 'Name'}):
            names8.append(name.text)
        for price in listing.find_all('td', attrs = {'aria-label': 'Last price'}):
            prices8.append(price.text)
        for change in listing.find_all('td', attrs = {'aria-label': 'Change'}):
            changes8.append(change.text)
        for pchange in listing.find_all('td', attrs = {'aria-label': '% change'}):
            percentChanges8.append(pchange.text)
        for cap in listing.find_all('td', attrs = {'aria-label': 'Market cap'}):
            marketCaps8.append(cap.text)
        for volume in listing.find_all('td', attrs = {'aria-label': 'Volume'}):
            totalVolumes8.append(volume.text)

#For industry choice 9 - Consumer Products & Media
prices9 = []
tickers9 = []
names9 = []
changes9 = []
percentChanges9 = []
marketCaps9 = []
totalVolumes9 = []

CPMUrl = "https://sg.finance.yahoo.com/industries/consumer_products_media"
r = requests.get(CPMUrl)
data = r.text
soup = BeautifulSoup(data, features = "lxml")
 
counter = 40
for i in range(40, 404, 14):
    for listing in soup.find_all('tr'):
        for ticker in listing.find_all('td', attrs = {'aria-label': 'Symbol'}):
            tickers9.append(ticker.text)
        for name in listing.find_all('td', attrs = {'aria-label': 'Name'}):
            names9.append(name.text)
        for price in listing.find_all('td', attrs = {'aria-label': 'Last price'}):
            prices9.append(price.text)
        for change in listing.find_all('td', attrs = {'aria-label': 'Change'}):
            changes9.append(change.text)
        for pchange in listing.find_all('td', attrs = {'aria-label': '% change'}):
            percentChanges9.append(pchange.text)
        for cap in listing.find_all('td', attrs = {'aria-label': 'Market cap'}):
            marketCaps9.append(cap.text)
        for volume in listing.find_all('td', attrs = {'aria-label': 'Volume'}):
            totalVolumes9.append(volume.text)

#For industry choice 10 - Industrials
prices10 = []
tickers10 = []
names10 = []
changes10 = []
percentChanges10 = []
marketCaps10 = []
totalVolumes10 = []

IndUrl = "https://sg.finance.yahoo.com/industries/industrials"
r = requests.get(IndUrl)
data = r.text
soup = BeautifulSoup(data, features = "lxml")
 
counter = 40
for i in range(40, 404, 14):
    for listing in soup.find_all('tr'):
        for ticker in listing.find_all('td', attrs = {'aria-label': 'Symbol'}):
            tickers10.append(ticker.text)
        for name in listing.find_all('td', attrs = {'aria-label': 'Name'}):
            names10.append(name.text)
        for price in listing.find_all('td', attrs = {'aria-label': 'Last price'}):
            prices10.append(price.text)
        for change in listing.find_all('td', attrs = {'aria-label': 'Change'}):
            changes10.append(change.text)
        for pchange in listing.find_all('td', attrs = {'aria-label': '% change'}):
            percentChanges10.append(pchange.text)
        for cap in listing.find_all('td', attrs = {'aria-label': 'Market cap'}):
            marketCaps10.append(cap.text)
        for volume in listing.find_all('td', attrs = {'aria-label': 'Volume'}):
            totalVolumes10.append(volume.text)

#For industry choice 11 - Diversified Businesses
prices11 = []
tickers11 = []
names11 = []
changes11 = []
percentChanges11 = []
marketCaps11 = []
totalVolumes11 = []

DivBizUrl = "https://sg.finance.yahoo.com/industries/diversified_business"
r = requests.get(DivBizUrl)
data = r.text
soup = BeautifulSoup(data, features = "lxml")
 
counter = 40
for i in range(40, 404, 14):
    for listing in soup.find_all('tr'):
        for ticker in listing.find_all('td', attrs = {'aria-label': 'Symbol'}):
            tickers11.append(ticker.text)
        for name in listing.find_all('td', attrs = {'aria-label': 'Name'}):
            names11.append(name.text)
        for price in listing.find_all('td', attrs = {'aria-label': 'Last price'}):
            prices11.append(price.text)
        for change in listing.find_all('td', attrs = {'aria-label': 'Change'}):
            changes11.append(change.text)
        for pchange in listing.find_all('td', attrs = {'aria-label': '% change'}):
            percentChanges11.append(pchange.text)
        for cap in listing.find_all('td', attrs = {'aria-label': 'Market cap'}):
            marketCaps11.append(cap.text)
        for volume in listing.find_all('td', attrs = {'aria-label': 'Volume'}):
            totalVolumes11.append(volume.text)

#For industry choice 12 - Retail & Hospitality
prices12 = []
tickers12 = []
names12 = []
changes12 = []
percentChanges12 = []
marketCaps12 = []
totalVolumes12 = []

RetHosUrl = "https://finance.yahoo.com/screener/unsaved/94b4b343-4d5f-47c3-8b3a-9c0064048a41?dependentField=sector&dependentValues=Technology&offset=0&count=100"
r = requests.get(RetHosUrl)
data = r.text
soup = BeautifulSoup(data, features = "lxml")
 
counter = 40
for i in range(40, 404, 14):
    for listing in soup.find_all('tr'):
        for ticker in listing.find_all('td', attrs = {'aria-label': 'Symbol'}):
            tickers12.append(ticker.text)
        for name in listing.find_all('td', attrs = {'aria-label': 'Name'}):
            names12.append(name.text)
        for price in listing.find_all('td', attrs = {'aria-label': 'Last price'}):
            prices12.append(price.text)
        for change in listing.find_all('td', attrs = {'aria-label': 'Change'}):
            changes12.append(change.text)
        for pchange in listing.find_all('td', attrs = {'aria-label': '% change'}):
            percentChanges12.append(pchange.text)
        for cap in listing.find_all('td', attrs = {'aria-label': 'Market cap'}):
            marketCaps12.append(cap.text)
        for volume in listing.find_all('td', attrs = {'aria-label': 'Volume'}):
            totalVolumes12.append(volume.text)
       
#The combined list of stocks, to facilitate choosing by stock ticker
prices_all = prices1 + prices2 + prices3 + prices4 + prices5 + prices6 + prices7 + prices8 + prices9 + prices10 + prices11 + prices12
tickers_all = tickers1 + tickers2 + tickers3 + tickers4 + tickers5 + tickers6 + tickers7 + tickers8 + tickers9 + tickers10 + tickers11 + tickers12 
names_all = names1 + names2 + names3 + names4 + names5 + names6 + names7 + names8 + names9 + names10 + names11 + names12
changes_all = changes1 + changes2 + changes3 + changes4 + changes5 + changes6 + changes7 + changes8 + changes9 + changes10 + changes11 + changes12
percentChanges_all = percentChanges1 + percentChanges2 + percentChanges3 + percentChanges4 + percentChanges5 + percentChanges6 + percentChanges7 + percentChanges8 + percentChanges9 + percentChanges10 + percentChanges11 + percentChanges12
marketCaps_all = marketCaps1 + marketCaps2 + marketCaps3 + marketCaps4 + marketCaps5 + marketCaps6 + marketCaps7 + marketCaps8 + marketCaps9 + marketCaps10 + marketCaps11 + marketCaps12
totalVolumes_all = totalVolumes1 + totalVolumes2 + totalVolumes3 + totalVolumes4 + totalVolumes5 + totalVolumes6 + totalVolumes7 + totalVolumes8 + totalVolumes9 + totalVolumes10 + totalVolumes11 + totalVolumes12        

complete_list = pd.DataFrame({"Ticker": tickers_all,
                                      "Name": names_all, 
                                      "Price": prices_all,
                                      "Market Cap": marketCaps_all})
                        
complete_list = complete_list[complete_list.Price != "N/A"]
complete_list.drop_duplicates(inplace = True, ignore_index = True)                        

while True:
    try:
        initial = input("""Would you like to browse stocks by industry, or do you have a specific stock ticker you'd like to look at?
[I] - Browse by Industry
[S] - Specific Stock Ticker: """).upper()
    
        if initial == "I":
            while True:
                try:
                    industry = int(input("""Which industry would you like to look at?
[1] - Energy
[2] - Financial Services
[3] - Healthcare
[4] - Business Services
[5] - Telecoms & Utilities
[6] - Computer Hardware & Electronics
[7] - Computer Software & Services
[8] - Manufacturing & Materials
[9] - Consumer Products & Media
[10] - Industrials
[11] - Diversified Businesses
[12] - Retail & Hospitality: """))
                    
                    if industry == 1:
                        
                        list_of_companies = pd.DataFrame({"Ticker": tickers1,
                                      "Name": names1, 
                                      "Price": prices1,
                                      "Market Cap": marketCaps1})
                        
                        list_of_companies = list_of_companies[list_of_companies.Price != '-']
                        list_of_companies.drop_duplicates(inplace = True, ignore_index = True)
                        
                        print() 
                        print(list_of_companies)
                        
                        while True:
                            try:
                                company = input("Please enter the ticker of the company you'd like to see: ").upper()
                        
                                df_yahoo = yf.download(company,
                                                       start = '2015-01-01', 
                                                       end = '2015-01-02',
                                                       progress=False)
                                df_yahoo = df_yahoo.drop(['Open', 'High', 'Low', 'Adj Close', 'Volume'], axis = 1)
                                
                                if df_yahoo.empty == True:
                                    print()
                                    raise Exception("Please recheck the ticker!")
                                    continue
                                #Try to ensure that there is nothing printed (Failed download etc) when ticker is incorrectly entered
                                
                                elif company not in list_of_companies.values:
                                    print("Please enter a ticker from the list of companies provided above, or select a different industry")
                                
                                else:
                                    print(f"You have chosen {list_of_companies[list_of_companies.Ticker == company].loc[:,'Name']}")
                                    
                                    confirm = input("""Would you now like to proceed to the simulator?
[Y] - Yes
[N] - No: """).upper()
                                    if confirm == "Y":
                                        break_to_main_menu = 1
                                        break
                                    
                                    elif confirm == "N":
                                        continue
                                    
                            except:
                                print("** There is no data on this ticker. The server may not possess it, or you may have entered an incorrect ticker. Please recheck **")
                    
                    elif industry == 2:
                        
                        list_of_companies = pd.DataFrame({"Ticker": tickers2,
                                      "Name": names2, 
                                      "Price": prices2,
                                      "Market Cap": marketCaps2})
                        
                        list_of_companies= list_of_companies[list_of_companies.Price != '-']
                        list_of_companies.drop_duplicates(inplace = True, ignore_index = True)
                        
                        print() 
                        print(list_of_companies)
                        
                        while True:
                            try:
                                company = input("Please enter the ticker of the company you'd like to see: ").upper()
                        
                                df_yahoo = yf.download(company,
                                                       start = '2015-01-01', 
                                                       end = '2015-01-02',
                                                       progress=False)
                                df_yahoo = df_yahoo.drop(['Open', 'High', 'Low', 'Adj Close', 'Volume'], axis = 1)
                                
                                if df_yahoo.empty == True:
                                    print()
                                    raise Exception("Please recheck the ticker!")
                                    continue
                                #Try to ensure that there is nothing printed (Failed download etc) when ticker is incorrectly entered
                                
                                elif company not in list_of_companies.values:
                                    print("Please enter a ticker from the list of companies provided above, or select a different industry")
                                
                                else:
                                    print(f"You have chosen {list_of_companies[list_of_companies.Ticker == company].loc[:,'Name']}")
                                    
                                    confirm = input("""Would you now like to proceed to the simulator?
[Y] - Yes
[N] - No: """).upper()
                                    if confirm == "Y":
                                        break_to_main_menu = 1
                                        break
                                    
                                    elif confirm == "N":
                                        continue
                                    
                            except:
                                print("** There is no data on this ticker. The server may not possess it, or you may have entered an incorrect ticker. Please recheck **")
            
                    elif industry == 3:
                                             
                        list_of_companies = pd.DataFrame({"Ticker": tickers3,
                                      "Name": names3, 
                                      "Price": prices3,
                                      "Market Cap": marketCaps3})
                        
                        list_of_companies = list_of_companies[list_of_companies.Price != '-']
                        list_of_companies.drop_duplicates(inplace = True, ignore_index = True)
                        
                        print() 
                        print(list_of_companies)
                        
                        while True:
                            try:
                                company = input("Please enter the ticker of the company you'd like to see: ").upper()
                        
                                df_yahoo = yf.download(company,
                                                       start = '2015-01-01', 
                                                       end = '2015-01-02',
                                                       progress=False)
                                df_yahoo = df_yahoo.drop(['Open', 'High', 'Low', 'Adj Close', 'Volume'], axis = 1)
                                
                                if df_yahoo.empty == True:
                                    print()
                                    raise Exception("Please recheck the ticker!")
                                    continue
                                #Try to ensure that there is nothing printed (Failed download etc) when ticker is incorrectly entered
                                
                                elif company not in list_of_companies.values:
                                    print("Please enter a ticker from the list of companies provided above, or select a different industry")
                                
                                else:
                                    print(f"You have chosen {list_of_companies[list_of_companies.Ticker == company].loc[:,'Name']}")
                                    
                                    confirm = input("""Would you now like to proceed to the simulator?
[Y] - Yes
[N] - No: """).upper()
                                    if confirm == "Y":
                                        break_to_main_menu = 1
                                        break
                                    
                                    elif confirm == "N":
                                        continue
                                    
                            except:
                                print("** There is no data on this ticker. The server may not possess it, or you may have entered an incorrect ticker. Please recheck **")
            
            
                    elif industry == 4:
                        
                        list_of_companies = pd.DataFrame({"Ticker": tickers4,
                                      "Name": names4, 
                                      "Price": prices4,
                                      "Market Cap": marketCaps4})
                        
                        list_of_companies = list_of_companies[list_of_companies.Price != '-']
                        list_of_companies.drop_duplicates(inplace = True, ignore_index = True)
                        
                        print() 
                        print(list_of_companies)
                        
                        while True:
                            try:
                                company = input("Please enter the ticker of the company you'd like to see: ").upper()
                        
                                df_yahoo = yf.download(company,
                                                       start = '2015-01-01', 
                                                       end = '2015-01-02',
                                                       progress=False)
                                df_yahoo = df_yahoo.drop(['Open', 'High', 'Low', 'Adj Close', 'Volume'], axis = 1)
                                
                                if df_yahoo.empty == True:
                                    print()
                                    raise Exception("Please recheck the ticker!")
                                    continue
                                #Try to ensure that there is nothing printed (Failed download etc) when ticker is incorrectly entered
                                
                                elif company not in list_of_companies.values:
                                    print("Please enter a ticker from the list of companies provided above, or select a different industry")
                                
                                else:
                                    print(f"You have chosen {list_of_companies[list_of_companies.Ticker == company].loc[:,'Name']}")
                                    
                                    confirm = input("""Would you now like to proceed to the simulator?
[Y] - Yes
[N] - No: """).upper()
                                    if confirm == "Y":
                                        break_to_main_menu = 1
                                        break
                                    
                                    elif confirm == "N":
                                        continue
                                    
                            except:
                                print("** There is no data on this ticker. The server may not possess it, or you may have entered an incorrect ticker. Please recheck **")
            
                    elif industry == 5:
                        
                        list_of_companies = pd.DataFrame({"Ticker": tickers5,
                                      "Name": names5, 
                                      "Price": prices5,
                                      "Market Cap": marketCaps5})
                        
                        list_of_companies = list_of_companies[list_of_companies.Price != '-']
                        list_of_companies.drop_duplicates(inplace = True, ignore_index = True)
                        
                        print() 
                        print(list_of_companies)
                        
                        while True:
                            try:
                                company = input("Please enter the ticker of the company you'd like to see: ").upper()
                        
                                df_yahoo = yf.download(company,
                                                       start = '2015-01-01', 
                                                       end = '2015-01-02',
                                                       progress=False)
                                df_yahoo = df_yahoo.drop(['Open', 'High', 'Low', 'Adj Close', 'Volume'], axis = 1)
                                
                                if df_yahoo.empty == True:
                                    print()
                                    raise Exception("Please recheck the ticker!")
                                    continue
                                #Try to ensure that there is nothing printed (Failed download etc) when ticker is incorrectly entered
                                
                                elif company not in list_of_companies.values:
                                    print("Please enter a ticker from the list of companies provided above, or select a different industry")
                                
                                else:
                                    print(f"You have chosen {list_of_companies[list_of_companies.Ticker == company].loc[:,'Name']}")
                                    
                                    confirm = input("""Would you now like to proceed to the simulator?
[Y] - Yes
[N] - No: """).upper()
                                    if confirm == "Y":
                                        break_to_main_menu = 1
                                        break
                                    
                                    elif confirm == "N":
                                        continue
                                    
                            except:
                                print("** There is no data on this ticker. The server may not possess it, or you may have entered an incorrect ticker. Please recheck **")
                
                
                    elif industry == 6:
                        
                        list_of_companies = pd.DataFrame({"Ticker": tickers6,
                                      "Name": names6, 
                                      "Price": prices6,
                                      "Market Cap": marketCaps6})
                        
                        list_of_companies = list_of_companies[list_of_companies.Price != '-']
                        list_of_companies.drop_duplicates(inplace = True, ignore_index = True)
                        
                        print() 
                        print(list_of_companies)
                        
                        while True:
                            try:
                                company = input("Please enter the ticker of the company you'd like to see: ").upper()
                        
                                df_yahoo = yf.download(company,
                                                       start = '2015-01-01', 
                                                       end = '2015-01-02',
                                                       progress=False)
                                df_yahoo = df_yahoo.drop(['Open', 'High', 'Low', 'Adj Close', 'Volume'], axis = 1)
                                
                                if df_yahoo.empty == True:
                                    print()
                                    raise Exception("Please recheck the ticker!")
                                    continue
                                #Try to ensure that there is nothing printed (Failed download etc) when ticker is incorrectly entered
                                
                                elif company not in list_of_companies.values:
                                    print("Please enter a ticker from the list of companies provided above, or select a different industry")
                                
                                else:
                                    print(f"You have chosen {list_of_companies[list_of_companies.Ticker == company].loc[:,'Name']}")
                                    
                                    confirm = input("""Would you now like to proceed to the simulator?
[Y] - Yes
[N] - No: """).upper()
                                    if confirm == "Y":
                                        break_to_main_menu = 1
                                        break
                                    
                                    elif confirm == "N":
                                        continue
                                    
                            except:
                                print("** There is no data on this ticker. The server may not possess it, or you may have entered an incorrect ticker. Please recheck **")
                
                    elif industry == 7:
                        
                        list_of_companies = pd.DataFrame({"Ticker": tickers7,
                                      "Name": names7, 
                                      "Price": prices7,
                                      "Market Cap": marketCaps7})
                        
                        list_of_companies = list_of_companies[list_of_companies.Price != '-']
                        list_of_companies.drop_duplicates(inplace = True, ignore_index = True)
                        
                        print() 
                        print(list_of_companies)
                        
                        while True:
                            try:
                                company = input("Please enter the ticker of the company you'd like to see: ").upper()
                        
                                df_yahoo = yf.download(company,
                                                       start = '2015-01-01', 
                                                       end = '2015-01-02',
                                                       progress=False)
                                df_yahoo = df_yahoo.drop(['Open', 'High', 'Low', 'Adj Close', 'Volume'], axis = 1)
                                
                                if df_yahoo.empty == True:
                                    print()
                                    raise Exception("Please recheck the ticker!")
                                    continue
                                #Try to ensure that there is nothing printed (Failed download etc) when ticker is incorrectly entered
                                
                                elif company not in list_of_companies.values:
                                    print("Please enter a ticker from the list of companies provided above, or select a different industry")
                                
                                else:
                                    print(f"You have chosen {list_of_companies[list_of_companies.Ticker == company].loc[:,'Name']}")
                                    
                                    confirm = input("""Would you now like to proceed to the simulator?
[Y] - Yes
[N] - No: """).upper()
                                    if confirm == "Y":
                                        break_to_main_menu = 1
                                        break
                                    
                                    elif confirm == "N":
                                        continue
                                    
                            except:
                                print("** There is no data on this ticker. The server may not possess it, or you may have entered an incorrect ticker. Please recheck **")
                
                    elif industry == 8:
                        
                        list_of_companies = pd.DataFrame({"Ticker": tickers8,
                                      "Name": names8, 
                                      "Price": prices8,
                                      "Market Cap": marketCaps8})
                        
                        list_of_companies = list_of_companies[list_of_companies.Price != '-']
                        list_of_companies.drop_duplicates(inplace = True, ignore_index = True)
                        
                        print() 
                        print(list_of_companies)
                        
                        while True:
                            try:
                                company = input("Please enter the ticker of the company you'd like to see: ").upper()
                        
                                df_yahoo = yf.download(company,
                                                       start = '2015-01-01', 
                                                       end = '2015-01-02',
                                                       progress=False)
                                df_yahoo = df_yahoo.drop(['Open', 'High', 'Low', 'Adj Close', 'Volume'], axis = 1)
                                
                                if df_yahoo.empty == True:
                                    print()
                                    raise Exception("Please recheck the ticker!")
                                    continue
                                #Try to ensure that there is nothing printed (Failed download etc) when ticker is incorrectly entered
                                
                                elif company not in list_of_companies.values:
                                    print("Please enter a ticker from the list of companies provided above, or select a different industry")
                                
                                else:
                                    print(f"You have chosen {list_of_companies[list_of_companies.Ticker == company].loc[:,'Name']}")
                                    
                                    confirm = input("""Would you now like to proceed to the simulator?
[Y] - Yes
[N] - No: """).upper()
                                    if confirm == "Y":
                                        break_to_main_menu = 1
                                        break
                                    
                                    elif confirm == "N":
                                        continue
                                    
                            except:
                                print("** There is no data on this ticker. The server may not possess it, or you may have entered an incorrect ticker. Please recheck **")
                
                    elif industry == 9:
                        
                        list_of_companies = pd.DataFrame({"Ticker": tickers9,
                                      "Name": names9, 
                                      "Price": prices9,
                                      "Market Cap": marketCaps9})
                        
                        list_of_companies = list_of_companies[list_of_companies.Price != '-']
                        list_of_companies.drop_duplicates(inplace = True, ignore_index = True)
                        
                        print() 
                        print(list_of_companies)
                        
                        while True:
                            try:
                                company = input("Please enter the ticker of the company you'd like to see: ").upper()
                        
                                df_yahoo = yf.download(company,
                                                       start = '2015-01-01', 
                                                       end = '2015-01-02',
                                                       progress=False)
                                df_yahoo = df_yahoo.drop(['Open', 'High', 'Low', 'Adj Close', 'Volume'], axis = 1)
                                
                                if df_yahoo.empty == True:
                                    print()
                                    raise Exception("Please recheck the ticker!")
                                    continue
                                #Try to ensure that there is nothing printed (Failed download etc) when ticker is incorrectly entered
                                
                                elif company not in list_of_companies.values:
                                    print("Please enter a ticker from the list of companies provided above, or select a different industry")
                                
                                else:
                                    print(f"You have chosen {list_of_companies[list_of_companies.Ticker == company].loc[:,'Name']}")
                                    
                                    confirm = input("""Would you now like to proceed to the simulator?
[Y] - Yes
[N] - No: """).upper()
                                    if confirm == "Y":
                                        break_to_main_menu = 1
                                        break
                                    
                                    elif confirm == "N":
                                        continue
                                    
                            except:
                                print("** There is no data on this ticker. The server may not possess it, or you may have entered an incorrect ticker. Please recheck **")
                
                    elif industry == 10:
                        
                        list_of_companies = pd.DataFrame({"Ticker": tickers10,
                                      "Name": names10, 
                                      "Price": prices10,
                                      "Market Cap": marketCaps10})
                        
                        list_of_companies = list_of_companies[list_of_companies.Price != '-']
                        list_of_companies.drop_duplicates(inplace = True, ignore_index = True)
                        
                        print() 
                        print(list_of_companies)
                        
                        while True:
                            try:
                                company = input("Please enter the ticker of the company you'd like to see: ").upper()
                        
                                df_yahoo = yf.download(company,
                                                       start = '2015-01-01', 
                                                       end = '2015-01-02',
                                                       progress=False)
                                df_yahoo = df_yahoo.drop(['Open', 'High', 'Low', 'Adj Close', 'Volume'], axis = 1)
                                
                                if df_yahoo.empty == True:
                                    print()
                                    raise Exception("Please recheck the ticker!")
                                    continue
                                #Try to ensure that there is nothing printed (Failed download etc) when ticker is incorrectly entered
                                
                                elif company not in list_of_companies.values:
                                    print("Please enter a ticker from the list of companies provided above, or select a different industry")
                                
                                else:
                                    print(f"You have chosen {list_of_companies[list_of_companies.Ticker == company].loc[:,'Name']}")
                                    
                                    confirm = input("""Would you now like to proceed to the simulator?
[Y] - Yes
[N] - No: """).upper()
                                    if confirm == "Y":
                                        break_to_main_menu = 1
                                        break
                                    
                                    elif confirm == "N":
                                        continue
                                    
                            except:
                                print("** There is no data on this ticker. The server may not possess it, or you may have entered an incorrect ticker. Please recheck **")
                
                    elif industry == 11:
                        
                        list_of_companies = pd.DataFrame({"Ticker": tickers11,
                                      "Name": names11, 
                                      "Price": prices11,
                                      "Market Cap": marketCaps11})
                        
                        list_of_companies = list_of_companies[list_of_companies.Price != '-']
                        list_of_companies.drop_duplicates(inplace = True, ignore_index = True)
                        
                        print() 
                        print(list_of_companies)
                        
                        while True:
                            try:
                                company = input("Please enter the ticker of the company you'd like to see: ").upper()
                        
                                df_yahoo = yf.download(company,
                                                       start = '2015-01-01', 
                                                       end = '2015-01-02',
                                                       progress=False)
                                df_yahoo = df_yahoo.drop(['Open', 'High', 'Low', 'Adj Close', 'Volume'], axis = 1)
                                
                                if df_yahoo.empty == True:
                                    print()
                                    raise Exception("Please recheck the ticker!")
                                    continue
                                #Try to ensure that there is nothing printed (Failed download etc) when ticker is incorrectly entered
                                
                                elif company not in list_of_companies.values:
                                    print("Please enter a ticker from the list of companies provided above, or select a different industry")
                                
                                else:
                                    print(f"You have chosen {list_of_companies[list_of_companies.Ticker == company].loc[:,'Name']}")
                                    
                                    confirm = input("""Would you now like to proceed to the simulator?
[Y] - Yes
[N] - No: """).upper()
                                    if confirm == "Y":
                                        break_to_main_menu = 1
                                        break
                                    
                                    elif confirm == "N":
                                        continue
                                    
                            except:
                                print("** There is no data on this ticker. The server may not possess it, or you may have entered an incorrect ticker. Please recheck **")
                
                    elif industry == 12:
                        
                        list_of_companies = pd.DataFrame({"Ticker": tickers12,
                                      "Name": names12, 
                                      "Price": prices12,
                                      "Market Cap": marketCaps12})
                        
                        list_of_companies = list_of_companies[list_of_companies.Price != '-']
                        list_of_companies.drop_duplicates(inplace = True, ignore_index = True)
                        
                        print() 
                        print(list_of_companies)
                        
                        while True:
                            try:
                                company = input("Please enter the ticker of the company you'd like to see: ").upper()
                        
                                df_yahoo = yf.download(company,
                                                       start = '2015-01-01', 
                                                       end = '2015-01-02',
                                                       progress=False)
                                df_yahoo = df_yahoo.drop(['Open', 'High', 'Low', 'Adj Close', 'Volume'], axis = 1)
                                
                                if df_yahoo.empty == True:
                                    print()
                                    raise Exception("Please recheck the ticker!")
                                    continue
                                #Try to ensure that there is nothing printed (Failed download etc) when ticker is incorrectly entered
                                
                                elif company not in list_of_companies.values:
                                    print("Please enter a ticker from the list of companies provided above, or select a different industry")
                                
                                else:
                                    print(f"You have chosen {list_of_companies[list_of_companies.Ticker == company].loc[:,'Name']}")
                                    
                                    confirm = input("""Would you now like to proceed to the simulator?
[Y] - Yes
[N] - No: """).upper()
                                    if confirm == "Y":
                                        break_to_main_menu = 1
                                        break
                                    
                                    elif confirm == "N":
                                        continue
                                    
                            except:
                                print("** There is no data on this ticker. The server may not possess it, or you may have entered an incorrect ticker. Please recheck **")
                
                    if break_to_main_menu == 1:
                        break
                                
                except:
                    print()
                    print("** Please only enter numerical values **")
        
        elif initial == "S":
            while True:
                try:
                    company = input("Please enter the ticker of the company you'd like to see: ").upper()
            
                    df_yahoo = yf.download(company,
                                           start = '2015-01-01', 
                                           end = '2015-01-02',
                                           progress=False)
                    df_yahoo = df_yahoo.drop(['Open', 'High', 'Low', 'Adj Close', 'Volume'], axis = 1)
                    
                    if df_yahoo.empty == True:
                        print()
                        raise Exception("Please recheck the ticker!")
                        continue
                    #Try to ensure that there is nothing printed (Failed download etc) when ticker is incorrectly entered
                    
                    else:
                        print(f"You have chosen {complete_list[complete_list.Ticker == company].loc[:,'Name']}")
                                    
                        confirm = input("""Would you now like to proceed to the simulator?
[Y] - Yes
[N] - No: """).upper()
                        if confirm == "Y":
                            break_to_main_menu = 1
                            break
                        
                        elif confirm == "N":
                            continue
                        
                except:
                    print("** There is no data on this ticker. The server may not possess it, or you may have entered an incorrect ticker. Please recheck **")
        
        else:
            print()
            print("Please choose only from [I] or [S]")
            continue
        
        if break_to_main_menu == 1:
            break
    
    except:
        print()
        print("Please choose only from [I] or [S]")

while True:
    try:
        print()
        print("-- Welcome to the main menu! --")
        
        options = input("""Press 
[C] to change your selected company
[X] to exit the software or
[P] to proceed: """).upper()   

        if options == "X":
            print()
            print("Thanks for using the simulator! We hope you enjoyed it!")
            break
        
        elif options == "C":
            while True:
                try:
                    while True:
                        try:
                            initial = input("""Would you like to browse stocks by industry, or do you have a specific stock ticker you'd like to look at?
[I] - Browse by Industry
[S] - Specific Stock Ticker: """).upper()
                        
                            if initial == "I":
                                while True:
                                    try:
                                        industry = int(input("""Which industry would you like to look at?
[1] - Energy
[2] - Financial Services
[3] - Healthcare
[4] - Business Services
[5] - Telecoms & Utilities
[6] - Computer Hardware & Electronics
[7] - Computer Software & Services
[8] - Manufacturing & Materials
[9] - Consumer Products & Media
[10] - Industrials
[11] - Diversified Businesses
[12] - Retail & Hospitality: """))
                                        
                                        if industry == 1:
                                            
                                            list_of_companies = pd.DataFrame({"Ticker": tickers1,
                                                          "Name": names1, 
                                                          "Price": prices1,
                                                          "Market Cap": marketCaps1})
                                            
                                            list_of_companies = list_of_companies[list_of_companies.Price != '-']
                                            list_of_companies.drop_duplicates(inplace = True, ignore_index = True)
                                            
                                            print() 
                                            print(list_of_companies)
                                            
                                            while True:
                                                try:
                                                    company = input("Please enter the ticker of the company you'd like to see: ").upper()
                                            
                                                    df_yahoo = yf.download(company,
                                                                           start = '2015-01-01', 
                                                                           end = '2015-01-02',
                                                                           progress=False)
                                                    df_yahoo = df_yahoo.drop(['Open', 'High', 'Low', 'Adj Close', 'Volume'], axis = 1)
                                                    
                                                    if df_yahoo.empty == True:
                                                        print()
                                                        raise Exception("Please recheck the ticker!")
                                                        continue
                                                    #Try to ensure that there is nothing printed (Failed download etc) when ticker is incorrectly entered
                                                    
                                                    elif company not in list_of_companies.values:
                                                        print("Please enter a ticker from the list of companies provided above, or select a different industry")
                                                    
                                                    else:
                                                        print(f"You have chosen {list_of_companies[list_of_companies.Ticker == company].loc[:,'Name']}")
                                                        
                                                        confirm = input("""Would you now like to proceed to the simulator?
[Y] - Yes
[N] - No: """).upper()
                                                        if confirm == "Y":
                                                            break_to_main_menu = 1
                                                            break
                                                        
                                                        elif confirm == "N":
                                                            continue
                                                        
                                                except:
                                                    print("** There is no data on this ticker. The server may not possess it, or you may have entered an incorrect ticker. Please recheck **")
                                        
                                        elif industry == 2:
                                            
                                            list_of_companies = pd.DataFrame({"Ticker": tickers2,
                                                          "Name": names2, 
                                                          "Price": prices2,
                                                          "Market Cap": marketCaps2})
                                            
                                            list_of_companies= list_of_companies[list_of_companies.Price != '-']
                                            list_of_companies.drop_duplicates(inplace = True, ignore_index = True)
                                            
                                            print() 
                                            print(list_of_companies)
                                            
                                            while True:
                                                try:
                                                    company = input("Please enter the ticker of the company you'd like to see: ").upper()
                                            
                                                    df_yahoo = yf.download(company,
                                                                           start = '2015-01-01', 
                                                                           end = '2015-01-02',
                                                                           progress=False)
                                                    df_yahoo = df_yahoo.drop(['Open', 'High', 'Low', 'Adj Close', 'Volume'], axis = 1)
                                                    
                                                    if df_yahoo.empty == True:
                                                        print()
                                                        raise Exception("Please recheck the ticker!")
                                                        continue
                                                    #Try to ensure that there is nothing printed (Failed download etc) when ticker is incorrectly entered
                                                    
                                                    elif company not in list_of_companies.values:
                                                        print("Please enter a ticker from the list of companies provided above, or select a different industry")
                                                    
                                                    else:
                                                        print(f"You have chosen {list_of_companies[list_of_companies.Ticker == company].loc[:,'Name']}")
                                                        
                                                        confirm = input("""Would you now like to proceed to the simulator?
[Y] - Yes
[N] - No: """).upper()
                                                        if confirm == "Y":
                                                            break_to_main_menu = 1
                                                            break
                                                        
                                                        elif confirm == "N":
                                                            continue
                                                        
                                                except:
                                                    print("** There is no data on this ticker. The server may not possess it, or you may have entered an incorrect ticker. Please recheck **")
                                
                                        elif industry == 3:
                                                                 
                                            list_of_companies = pd.DataFrame({"Ticker": tickers3,
                                                          "Name": names3, 
                                                          "Price": prices3,
                                                          "Market Cap": marketCaps3})
                                            
                                            list_of_companies = list_of_companies[list_of_companies.Price != '-']
                                            list_of_companies.drop_duplicates(inplace = True, ignore_index = True)
                                            
                                            print() 
                                            print(list_of_companies)
                                            
                                            while True:
                                                try:
                                                    company = input("Please enter the ticker of the company you'd like to see: ").upper()
                                            
                                                    df_yahoo = yf.download(company,
                                                                           start = '2015-01-01', 
                                                                           end = '2015-01-02',
                                                                           progress=False)
                                                    df_yahoo = df_yahoo.drop(['Open', 'High', 'Low', 'Adj Close', 'Volume'], axis = 1)
                                                    
                                                    if df_yahoo.empty == True:
                                                        print()
                                                        raise Exception("Please recheck the ticker!")
                                                        continue
                                                    #Try to ensure that there is nothing printed (Failed download etc) when ticker is incorrectly entered
                                                    
                                                    elif company not in list_of_companies.values:
                                                        print("Please enter a ticker from the list of companies provided above, or select a different industry")
                                                    
                                                    else:
                                                        print(f"You have chosen {list_of_companies[list_of_companies.Ticker == company].loc[:,'Name']}")
                                                        
                                                        confirm = input("""Would you now like to proceed to the simulator?
[Y] - Yes
[N] - No: """).upper()
                                                        if confirm == "Y":
                                                            break_to_main_menu = 1
                                                            break
                                                        
                                                        elif confirm == "N":
                                                            continue
                                                        
                                                except:
                                                    print("** There is no data on this ticker. The server may not possess it, or you may have entered an incorrect ticker. Please recheck **")
                                
                                
                                        elif industry == 4:
                                            
                                            list_of_companies = pd.DataFrame({"Ticker": tickers4,
                                                          "Name": names4, 
                                                          "Price": prices4,
                                                          "Market Cap": marketCaps4})
                                            
                                            list_of_companies = list_of_companies[list_of_companies.Price != '-']
                                            list_of_companies.drop_duplicates(inplace = True, ignore_index = True)
                                            
                                            print() 
                                            print(list_of_companies)
                                            
                                            while True:
                                                try:
                                                    company = input("Please enter the ticker of the company you'd like to see: ").upper()
                                            
                                                    df_yahoo = yf.download(company,
                                                                           start = '2015-01-01', 
                                                                           end = '2015-01-02',
                                                                           progress=False)
                                                    df_yahoo = df_yahoo.drop(['Open', 'High', 'Low', 'Adj Close', 'Volume'], axis = 1)
                                                    
                                                    if df_yahoo.empty == True:
                                                        print()
                                                        raise Exception("Please recheck the ticker!")
                                                        continue
                                                    #Try to ensure that there is nothing printed (Failed download etc) when ticker is incorrectly entered
                                                    
                                                    elif company not in list_of_companies.values:
                                                        print("Please enter a ticker from the list of companies provided above, or select a different industry")
                                                    
                                                    else:
                                                        print(f"You have chosen {list_of_companies[list_of_companies.Ticker == company].loc[:,'Name']}")
                                                        
                                                        confirm = input("""Would you now like to proceed to the simulator?
[Y] - Yes
[N] - No: """).upper()
                                                        if confirm == "Y":
                                                            break_to_main_menu = 1
                                                            break
                                                        
                                                        elif confirm == "N":
                                                            continue
                                                        
                                                except:
                                                    print("** There is no data on this ticker. The server may not possess it, or you may have entered an incorrect ticker. Please recheck **")
                                
                                        elif industry == 5:
                                            
                                            list_of_companies = pd.DataFrame({"Ticker": tickers5,
                                                          "Name": names5, 
                                                          "Price": prices5,
                                                          "Market Cap": marketCaps5})
                                            
                                            list_of_companies = list_of_companies[list_of_companies.Price != '-']
                                            list_of_companies.drop_duplicates(inplace = True, ignore_index = True)
                                            
                                            print() 
                                            print(list_of_companies)
                                            
                                            while True:
                                                try:
                                                    company = input("Please enter the ticker of the company you'd like to see: ").upper()
                                            
                                                    df_yahoo = yf.download(company,
                                                                           start = '2015-01-01', 
                                                                           end = '2015-01-02',
                                                                           progress=False)
                                                    df_yahoo = df_yahoo.drop(['Open', 'High', 'Low', 'Adj Close', 'Volume'], axis = 1)
                                                    
                                                    if df_yahoo.empty == True:
                                                        print()
                                                        raise Exception("Please recheck the ticker!")
                                                        continue
                                                    #Try to ensure that there is nothing printed (Failed download etc) when ticker is incorrectly entered
                                                    
                                                    elif company not in list_of_companies.values:
                                                        print("Please enter a ticker from the list of companies provided above, or select a different industry")
                                                    
                                                    else:
                                                        print(f"You have chosen {list_of_companies[list_of_companies.Ticker == company].loc[:,'Name']}")
                                                        
                                                        confirm = input("""Would you now like to proceed to the simulator?
[Y] - Yes
[N] - No: """).upper()
                                                        if confirm == "Y":
                                                            break_to_main_menu = 1
                                                            break
                                                        
                                                        elif confirm == "N":
                                                            continue
                                                        
                                                except:
                                                    print("** There is no data on this ticker. The server may not possess it, or you may have entered an incorrect ticker. Please recheck **")
                                    
                                    
                                        elif industry == 6:
                                            
                                            list_of_companies = pd.DataFrame({"Ticker": tickers6,
                                                          "Name": names6, 
                                                          "Price": prices6,
                                                          "Market Cap": marketCaps6})
                                            
                                            list_of_companies = list_of_companies[list_of_companies.Price != '-']
                                            list_of_companies.drop_duplicates(inplace = True, ignore_index = True)
                                            
                                            print() 
                                            print(list_of_companies)
                                            
                                            while True:
                                                try:
                                                    company = input("Please enter the ticker of the company you'd like to see: ").upper()
                                            
                                                    df_yahoo = yf.download(company,
                                                                           start = '2015-01-01', 
                                                                           end = '2015-01-02',
                                                                           progress=False)
                                                    df_yahoo = df_yahoo.drop(['Open', 'High', 'Low', 'Adj Close', 'Volume'], axis = 1)
                                                    
                                                    if df_yahoo.empty == True:
                                                        print()
                                                        raise Exception("Please recheck the ticker!")
                                                        continue
                                                    #Try to ensure that there is nothing printed (Failed download etc) when ticker is incorrectly entered
                                                    
                                                    elif company not in list_of_companies.values:
                                                        print("Please enter a ticker from the list of companies provided above, or select a different industry")
                                                    
                                                    else:
                                                        print(f"You have chosen {list_of_companies[list_of_companies.Ticker == company].loc[:,'Name']}")
                                                        
                                                        confirm = input("""Would you now like to proceed to the simulator?
[Y] - Yes
[N] - No: """).upper()
                                                        if confirm == "Y":
                                                            break_to_main_menu = 1
                                                            break
                                                        
                                                        elif confirm == "N":
                                                            continue
                                                        
                                                except:
                                                    print("** There is no data on this ticker. The server may not possess it, or you may have entered an incorrect ticker. Please recheck **")
                                    
                                        elif industry == 7:
                                            
                                            list_of_companies = pd.DataFrame({"Ticker": tickers7,
                                                          "Name": names7, 
                                                          "Price": prices7,
                                                          "Market Cap": marketCaps7})
                                            
                                            list_of_companies = list_of_companies[list_of_companies.Price != '-']
                                            list_of_companies.drop_duplicates(inplace = True, ignore_index = True)
                                            
                                            print() 
                                            print(list_of_companies)
                                            
                                            while True:
                                                try:
                                                    company = input("Please enter the ticker of the company you'd like to see: ").upper()
                                            
                                                    df_yahoo = yf.download(company,
                                                                           start = '2015-01-01', 
                                                                           end = '2015-01-02',
                                                                           progress=False)
                                                    df_yahoo = df_yahoo.drop(['Open', 'High', 'Low', 'Adj Close', 'Volume'], axis = 1)
                                                    
                                                    if df_yahoo.empty == True:
                                                        print()
                                                        raise Exception("Please recheck the ticker!")
                                                        continue
                                                    #Try to ensure that there is nothing printed (Failed download etc) when ticker is incorrectly entered
                                                    
                                                    elif company not in list_of_companies.values:
                                                        print("Please enter a ticker from the list of companies provided above, or select a different industry")
                                                    
                                                    else:
                                                        print(f"You have chosen {list_of_companies[list_of_companies.Ticker == company].loc[:,'Name']}")
                                                        
                                                        confirm = input("""Would you now like to proceed to the simulator?
[Y] - Yes
[N] - No: """).upper()
                                                        if confirm == "Y":
                                                            break_to_main_menu = 1
                                                            break
                                                        
                                                        elif confirm == "N":
                                                            continue
                                                        
                                                except:
                                                    print("** There is no data on this ticker. The server may not possess it, or you may have entered an incorrect ticker. Please recheck **")
                                    
                                        elif industry == 8:
                                            
                                            list_of_companies = pd.DataFrame({"Ticker": tickers8,
                                                          "Name": names8, 
                                                          "Price": prices8,
                                                          "Market Cap": marketCaps8})
                                            
                                            list_of_companies = list_of_companies[list_of_companies.Price != '-']
                                            list_of_companies.drop_duplicates(inplace = True, ignore_index = True)
                                            
                                            print() 
                                            print(list_of_companies)
                                            
                                            while True:
                                                try:
                                                    company = input("Please enter the ticker of the company you'd like to see: ").upper()
                                            
                                                    df_yahoo = yf.download(company,
                                                                           start = '2015-01-01', 
                                                                           end = '2015-01-02',
                                                                           progress=False)
                                                    df_yahoo = df_yahoo.drop(['Open', 'High', 'Low', 'Adj Close', 'Volume'], axis = 1)
                                                    
                                                    if df_yahoo.empty == True:
                                                        print()
                                                        raise Exception("Please recheck the ticker!")
                                                        continue
                                                    #Try to ensure that there is nothing printed (Failed download etc) when ticker is incorrectly entered
                                                    
                                                    elif company not in list_of_companies.values:
                                                        print("Please enter a ticker from the list of companies provided above, or select a different industry")
                                                    
                                                    else:
                                                        print(f"You have chosen {list_of_companies[list_of_companies.Ticker == company].loc[:,'Name']}")
                                                        
                                                        confirm = input("""Would you now like to proceed to the simulator?
[Y] - Yes
[N] - No: """).upper()
                                                        if confirm == "Y":
                                                            break_to_main_menu = 1
                                                            break
                                                        
                                                        elif confirm == "N":
                                                            continue
                                                        
                                                except:
                                                    print("** There is no data on this ticker. The server may not possess it, or you may have entered an incorrect ticker. Please recheck **")
                                    
                                        elif industry == 9:
                                            
                                            list_of_companies = pd.DataFrame({"Ticker": tickers9,
                                                          "Name": names9, 
                                                          "Price": prices9,
                                                          "Market Cap": marketCaps9})
                                            
                                            list_of_companies = list_of_companies[list_of_companies.Price != '-']
                                            list_of_companies.drop_duplicates(inplace = True, ignore_index = True)
                                            
                                            print() 
                                            print(list_of_companies)
                                            
                                            while True:
                                                try:
                                                    company = input("Please enter the ticker of the company you'd like to see: ").upper()
                                            
                                                    df_yahoo = yf.download(company,
                                                                           start = '2015-01-01', 
                                                                           end = '2015-01-02',
                                                                           progress=False)
                                                    df_yahoo = df_yahoo.drop(['Open', 'High', 'Low', 'Adj Close', 'Volume'], axis = 1)
                                                    
                                                    if df_yahoo.empty == True:
                                                        print()
                                                        raise Exception("Please recheck the ticker!")
                                                        continue
                                                    #Try to ensure that there is nothing printed (Failed download etc) when ticker is incorrectly entered
                                                    
                                                    elif company not in list_of_companies.values:
                                                        print("Please enter a ticker from the list of companies provided above, or select a different industry")
                                                    
                                                    else:
                                                        print(f"You have chosen {list_of_companies[list_of_companies.Ticker == company].loc[:,'Name']}")
                                                        
                                                        confirm = input("""Would you now like to proceed to the simulator?
[Y] - Yes
[N] - No: """).upper()
                                                        if confirm == "Y":
                                                            break_to_main_menu = 1
                                                            break
                                                        
                                                        elif confirm == "N":
                                                            continue
                                                        
                                                except:
                                                    print("** There is no data on this ticker. The server may not possess it, or you may have entered an incorrect ticker. Please recheck **")
                                    
                                        elif industry == 10:
                                            
                                            list_of_companies = pd.DataFrame({"Ticker": tickers10,
                                                          "Name": names10, 
                                                          "Price": prices10,
                                                          "Market Cap": marketCaps10})
                                            
                                            list_of_companies = list_of_companies[list_of_companies.Price != '-']
                                            list_of_companies.drop_duplicates(inplace = True, ignore_index = True)
                                            
                                            print() 
                                            print(list_of_companies)
                                            
                                            while True:
                                                try:
                                                    company = input("Please enter the ticker of the company you'd like to see: ").upper()
                                            
                                                    df_yahoo = yf.download(company,
                                                                           start = '2015-01-01', 
                                                                           end = '2015-01-02',
                                                                           progress=False)
                                                    df_yahoo = df_yahoo.drop(['Open', 'High', 'Low', 'Adj Close', 'Volume'], axis = 1)
                                                    
                                                    if df_yahoo.empty == True:
                                                        print()
                                                        raise Exception("Please recheck the ticker!")
                                                        continue
                                                    #Try to ensure that there is nothing printed (Failed download etc) when ticker is incorrectly entered
                                                    
                                                    elif company not in list_of_companies.values:
                                                        print("Please enter a ticker from the list of companies provided above, or select a different industry")
                                                    
                                                    else:
                                                        print(f"You have chosen {list_of_companies[list_of_companies.Ticker == company].loc[:,'Name']}")
                                                        
                                                        confirm = input("""Would you now like to proceed to the simulator?
[Y] - Yes
[N] - No: """).upper()
                                                        if confirm == "Y":
                                                            break_to_main_menu = 1
                                                            break
                                                        
                                                        elif confirm == "N":
                                                            continue
                                                        
                                                except:
                                                    print("** There is no data on this ticker. The server may not possess it, or you may have entered an incorrect ticker. Please recheck **")
                                    
                                        elif industry == 11:
                                            
                                            list_of_companies = pd.DataFrame({"Ticker": tickers11,
                                                          "Name": names11, 
                                                          "Price": prices11,
                                                          "Market Cap": marketCaps11})
                                            
                                            list_of_companies = list_of_companies[list_of_companies.Price != '-']
                                            list_of_companies.drop_duplicates(inplace = True, ignore_index = True)
                                            
                                            print() 
                                            print(list_of_companies)
                                            
                                            while True:
                                                try:
                                                    company = input("Please enter the ticker of the company you'd like to see: ").upper()
                                            
                                                    df_yahoo = yf.download(company,
                                                                           start = '2015-01-01', 
                                                                           end = '2015-01-02',
                                                                           progress=False)
                                                    df_yahoo = df_yahoo.drop(['Open', 'High', 'Low', 'Adj Close', 'Volume'], axis = 1)
                                                    
                                                    if df_yahoo.empty == True:
                                                        print()
                                                        raise Exception("Please recheck the ticker!")
                                                        continue
                                                    #Try to ensure that there is nothing printed (Failed download etc) when ticker is incorrectly entered
                                                    
                                                    elif company not in list_of_companies.values:
                                                        print("Please enter a ticker from the list of companies provided above, or select a different industry")
                                                    
                                                    else:
                                                        print(f"You have chosen {list_of_companies[list_of_companies.Ticker == company].loc[:,'Name']}")
                                                        
                                                        confirm = input("""Would you now like to proceed to the simulator?
[Y] - Yes
[N] - No: """).upper()
                                                        if confirm == "Y":
                                                            break_to_main_menu = 1
                                                            break
                                                        
                                                        elif confirm == "N":
                                                            continue
                                                        
                                                except:
                                                    print("** There is no data on this ticker. The server may not possess it, or you may have entered an incorrect ticker. Please recheck **")
                                    
                                        elif industry == 12:
                                            
                                            list_of_companies = pd.DataFrame({"Ticker": tickers12,
                                                          "Name": names12, 
                                                          "Price": prices12,
                                                          "Market Cap": marketCaps12})
                                            
                                            list_of_companies = list_of_companies[list_of_companies.Price != '-']
                                            list_of_companies.drop_duplicates(inplace = True, ignore_index = True)
                                            
                                            print() 
                                            print(list_of_companies)
                                            
                                            while True:
                                                try:
                                                    company = input("Please enter the ticker of the company you'd like to see: ").upper()
                                            
                                                    df_yahoo = yf.download(company,
                                                                           start = '2015-01-01', 
                                                                           end = '2015-01-02',
                                                                           progress=False)
                                                    df_yahoo = df_yahoo.drop(['Open', 'High', 'Low', 'Adj Close', 'Volume'], axis = 1)
                                                    
                                                    if df_yahoo.empty == True:
                                                        print()
                                                        raise Exception("Please recheck the ticker!")
                                                        continue
                                                    #Try to ensure that there is nothing printed (Failed download etc) when ticker is incorrectly entered
                                                    
                                                    elif company not in list_of_companies.values:
                                                        print("Please enter a ticker from the list of companies provided above, or select a different industry")
                                                    
                                                    else:
                                                        print(f"You have chosen {list_of_companies[list_of_companies.Ticker == company].loc[:,'Name']}")
                                                        
                                                        confirm = input("""Would you now like to proceed to the simulator?
[Y] - Yes
[N] - No: """).upper()
                                                        if confirm == "Y":
                                                            break_to_main_menu = 1
                                                            break
                                                        
                                                        elif confirm == "N":
                                                            continue
                                                        
                                                except:
                                                    print("** There is no data on this ticker. The server may not possess it, or you may have entered an incorrect ticker. Please recheck **")
                                    
                                        else:
                                            print()
                                            print("** Please enter a number from 1 to 12 **")
                                            continue
                                        
                                        if break_to_main_menu == 1:
                                            break
                                                    
                                    except:
                                        print()
                                        print("** Please only enter numerical values **")
                            
                            elif initial == "S":
                                while True:
                                    try:
                                        company = input("Please enter the ticker of the company you'd like to see: ").upper()
                                
                                        df_yahoo = yf.download(company,
                                                               start = '2015-01-01', 
                                                               end = '2015-01-02',
                                                               progress=False)
                                        df_yahoo = df_yahoo.drop(['Open', 'High', 'Low', 'Adj Close', 'Volume'], axis = 1)
                                        
                                        if df_yahoo.empty == True:
                                            print()
                                            raise Exception("Please recheck the ticker!")
                                            continue
                                        #Try to ensure that there is nothing printed (Failed download etc) when ticker is incorrectly entered
                                        
                                        else:
                                            print(f"You have chosen {complete_list[complete_list.Ticker == company].loc[:,'Name']}")
                                                        
                                            confirm = input("""Would you now like to proceed to the simulator?
[Y] - Yes
[N] - No: """).upper()
                                            if confirm == "Y":
                                                break_to_main_menu = 1
                                                break
                                            
                                            elif confirm == "N":
                                                continue
                                            
                                    except:
                                        print("** There is no data on this ticker. The server may not possess it, or you may have entered an incorrect ticker. Please recheck **")
                        
                            else:
                                print()
                                print("Please choose only from [I] or [S]")
                                continue
                            
                            if break_to_main_menu == 1:
                                break
                        
                        except:
                            print()
                            print("Please choose only from [I] or [S]")
                            
                    if break_to_main_menu == 1:
                        break
                
                except:
                    print("** Please choose only from [I] or [S] **") #TO CHANGE BASED ON THE OUTPUT
        
        elif options == "P":
            while True:
                try:
                    print()
                    print("-- Welcome to the simulator! --")
                    
                    date_entered = input("""Please enter a start date in the format YYYY-MM-DD.
This will be the date from which we'll start showing the stock prices
Alternatively, please press [B] to go back: """)

                    if date_entered.upper() == "B":
                        break_to_main_menu = 1
                        break                    

                    else:
                        date_input = datetime.strptime(date_entered, "%Y-%m-%d").date()
                    
                        company_data = yf.download(company,
                                           start = date_entered, 
                                           end = date.today(),
                                           progress=False)
                    
                        company_data = company_data.reset_index()
                    
                        company_data['Date'] = company_data['Date'].astype(str)
                        date_list = company_data['Date'].tolist()
                        close = company_data['Close'].tolist()
                        
                        #5 days prior
                        date_input_5 = date_input - timedelta(days = 5)
                        date_entered_5 = str(date_input_5)
                        
                        company_data_5 = yf.download(company,
                        start = str(date_input-timedelta(days = 5)), 
                        end = str(date.today()-timedelta(days = 5)),
                        progress=False)
                                            
                        company_data_5 = company_data_5.reset_index()                    
                        company_data_5['Date'] = company_data_5['Date'].astype(str)
                        date_list_5 = company_data_5['Date'].tolist()
                        close_5 = company_data_5['Close'].tolist()  
                        
                        date_list_subset = []
                        close_subset = []
                        
                        date_list_subset.extend(date_list_5[:5])
                        close_subset.extend(close_5[:5])
                        
                        MA_date_list = []
                        MA_close = []
                        
                        MA_date_list.extend(date_list_5[:5])
                        MA_close.extend(close_5[:5])
                        
                        if date_entered[4] != "-" or date_entered[7] != "-":
                            print("The format is incorrect")
                            continue
                        
                        elif date_input > date.today():
                            print()
                            print("The date you have entered is one in the future; Please enter a past date to start the simulator")
                            continue
                        
                        if date_entered not in date_list:
                            print()
                            print("The entered date is a stock market holiday or a weekend. We'll request you to please enter a different date.")
                            continue
                        
                        elif date_entered in date_list:
                            for i,j in zip(date_list[date_list.index(date_entered):], close[date_list.index(date_entered):]):
                                try:
                                    print()
                                    print(f"{i} -- S$ {j:.2f}")
                                    
                                    date_list_subset.append(i)
                                    close_subset.append(j)
                                    
                                    MA_date_list.append(i)
                                    MA_close.append(j)
                                    
                                    stock_df = pd.DataFrame({'Date': date_list_subset, 'Close': close_subset})
                                    MA_df = pd.DataFrame({'Date': MA_date_list, 'Close': MA_close})
                                    MA_df['Weekly_MA'] = MA_df.Close.rolling(window=7).mean()
                                    MA_df['Monthly_MA'] = MA_df.Close.rolling(window=30).mean()
                                    
                                    #Plotting with matplotlib                                                                    
                                    plt.style.use('dark_background')
                                    plt.figure(figsize=(15,7))
                                    plt.plot(stock_df.Date, stock_df.Close, marker = 'o', markersize = 10, markerfacecolor = 'goldenrod', linestyle = 'solid', linewidth = '4', color = 'purple', label = "Price")
                                    plt.plot(MA_df.Date, MA_df.Weekly_MA, linestyle = 'dashed', linewidth = '3', color = 'yellow', label = "Weekly Moving Average")
                                    plt.plot(MA_df.Date, MA_df.Monthly_MA, linestyle = 'dashed', linewidth = '3', color = 'orange', label = "Monthly Moving Average")
                                    plt.legend(loc = 'upper left')
                                    plt.show()
                                    
                                    action = input("""Press:
[S] - Short
[L] - Long 
[I] - learning what "Short" and "Long" mean
[N] - Next Date or 
[B] - Back to the previous menu: """).upper()
                                    
                                    if action == "S":
                                        while True:
                                            try:
                                                short_value = float(input("""Select the portfolio % that you would like to short 
(Please enter only the number, and press 0 to abandon): """))               
                                                if 0 < short_value <=100:
                                                    short_position_value = short_value/100*portfolio_value
                                                    
                                                    while True:
                                                        try:
                                                            a = input(f"""You are going to short {short_value}% of your portfolio, which is S$ {short_position_value:,.2f}
Choose from the functions
[Y] - continue
[N] - no: """).upper()
                                                            
                                                            if a == "Y":
                                                                print(f"Short position for S$ {short_position_value:,.2f} has been successfully taken!")
                                                                print()
                                                                quantity_shorted = short_position_value/close[close.index(j)]
                                                                
                                                                date_list_subset_short = []
                                                                close_subset_short = []
                                                                
                                                                for k, q in zip(date_list[date_list.index(i):], close[close.index(j):]): 
                                                                    try:
                                                                        print(f"Short position for S$ {short_position_value:,.2f} taken on {date_list[date_list.index(i)]} at S$ {close[date_list.index(i)]:,.2f}")
                                                                        print()
                                                                        print(f"Current date & price: {k} -- S$ {q:.2f}")
                                                                        
                                                                        date_list_subset_short.append(k)
                                                                        close_subset_short.append(q)
                                                                        
                                                                        MA_df = pd.DataFrame({'Date': MA_date_list, 'Close': MA_close})
                                                                        MA_date_list.append(k)
                                                                        MA_close.append(q)
                                                                        
                                                                        stock_df_short = pd.DataFrame({'Date': date_list_subset_short, 'Close': close_subset_short})
                                                                        MA_df['Weekly_MA'] = MA_df.Close.rolling(window=7).mean()
                                                                        MA_df['Monthly_MA'] = MA_df.Close.rolling(window=30).mean()
                                                                        
                                                                        cutoff = close_subset[-1]
                                                                        
                                                                        colors = []
                                                                        
                                                                        if stock_df_short.Close.iloc[-1] > cutoff:
                                                                            colors.append('firebrick')
                                                                        elif stock_df_short.Close.iloc[-1] < cutoff:
                                                                            colors.append('mediumseagreen')
                                                                        else:
                                                                            colors.append('grey')
                                                                            
                                                                        #This technique changes the color of the entire line depending on profit or loss
                                                                        #Doesn't bifurcate the line into sections and color each section, but is a significant improvement
                                                                        
                                                                        plt.style.use('dark_background')
                                                                        fig, ax = plt.subplots(figsize = (15, 7))
                                                                        ax = plt.plot(stock_df.Date, stock_df.Close, marker = 'o', markersize = 10, markerfacecolor = 'goldenrod', linestyle = 'solid', linewidth = '4', color = 'purple')
                                                                        ax = plt.axhline(y = close_subset[-1], color = 'white', linestyle = 'dashed')
                                                                        ax = plt.plot(stock_df_short.Date, stock_df_short.Close, marker = 'o', markersize = 10, markerfacecolor = 'goldenrod', linestyle = 'solid', linewidth = '4', color = colors[-1])
                                                                        plt.show()
                                    
                                                                        z = input("""Choose from the functions
[C] - Cover
[Any key] - next: """).upper()
                                                                        print()
                                                                        
                                                                        if z != "C":
                                                                            continue
                                                                            
                                                                        elif z == "C":
                                                                            print("Short position covered")
                                                                            print()
                                                                            money_change_short = quantity_shorted*(close[date_list.index(i)]-close[date_list.index(k)])
                                                                            portfolio_value += money_change_short
                                                                            print("*** Position Summary ***")
                                                                            print()
                                                                            print(f"You made S${money_change_short:,.3f} in this Short")
                                                                            print(f"Your portfolio value is now S$ {portfolio_value:,.2f}")
                                                                            print()
                                                                            exit_short_to_main_menu = 1
                                                                            break
                                                                        
                                                                    except:
                                                                        print("Please enter a supported option")
                                                                                    
                                                            elif a == "N":
                                                                print("Position aborted")
                                                                break
                                                                
                                                            else:
                                                                print("Please choose only from [Y] or [N]")
                                                                continue
                                                            
                                                            if exit_short_to_main_menu == 1:
                                                                break
                                                            
                                                        except:
                                                            print("Please provide a valid input")
                            
                                                elif short_value == 0:
                                                    print("Short position abandoned")
                                                    break
                                                
                                                else:
                                                    print("Please enter a positive number between 0 and 100 ")
                                                    continue
                                            
                                                if exit_short_to_main_menu == 1:
                                                    break
                                            
                                            except:
                                                print("Please enter a numeric value only")
                                
                                    elif action == "L":
                                        while True:
                                            try:
                                                long_value = float(input("""Select the portfolio % that you would like to long 
(Please enter only the number, and press 0 to abandon): """))               
                                                if 0 < long_value <=100:
                                                    long_position_value = long_value/100*portfolio_value
                                                    
                                                    while True:
                                                        try:
                                                            a = input(f"""You are going to long {long_value}% of your portfolio, which is S$ {long_position_value:,.2f}
Choose from the functions
[Y] - continue
[N] - no: """).upper()
                                                            
                                                            if a == "Y":
                                                                print(f"Long position for S$ {long_position_value:,.2f} has been successfully taken!")
                                                                print()
                                                                quantity_longed = long_position_value/close[close.index(j)]
                                                                
                                                                date_list_subset_long = []
                                                                close_subset_long = []
                                                                  
                                                                for k, q in zip(date_list[date_list.index(i):], close[close.index(j):]): 
                                                                    try:
                                                                        print(f"Long position for S$ {long_position_value:,.2f} taken on {date_list[date_list.index(i)]} at S$ {close[date_list.index(i)]:,.2f}")
                                                                        print()
                                                                        print(f"Current date & price: {k} -- S$ {q:.2f}")
                                                                        
                                                                        date_list_subset_long.append(k)
                                                                        close_subset_long.append(q)
                                                                        
                                                                        stock_df_long = pd.DataFrame({'Date': date_list_subset_long, 'Close': close_subset_long})
                                                                        
                                                                        cutoff = close_subset[-1]
                                                                        
                                                                        colors = []
                                                                        
                                                                        if stock_df_long.Close.iloc[-1] > cutoff:
                                                                            colors.append('mediumseagreen')
                                                                        elif stock_df_long.Close.iloc[-1] < cutoff:
                                                                            colors.append('firebrick')
                                                                        else:
                                                                            colors.append('grey')
                                                                            
                                                                        #This technique changes the color of the entire line depending on profit or loss
                                                                        #Doesn't bifurcate the line into sections and color each section, but is a significant improvement
                                                                        
                                                                        plt.style.use('dark_background')
                                                                        fig, ax = plt.subplots(figsize = (15, 7))
                                                                        ax = plt.plot(stock_df.Date, stock_df.Close, marker = 'o', markersize = 10, markerfacecolor = 'goldenrod', linestyle = 'solid', linewidth = '4', color = 'purple')
                                                                        ax = plt.axhline(y = close_subset[-1], color = 'white', linestyle = 'dashed')
                                                                        ax = plt.plot(stock_df_long.Date, stock_df_long.Close, marker = 'o', markersize = 10, markerfacecolor = 'goldenrod', linestyle = 'solid', linewidth = '4', color = colors[-1])
                                                                        plt.show()
                                    
                                                                        
                                                                        z = input("""Choose from the functions
[C] - Cover
[Any key] - next: """).upper()
                                                                        print()
                                                                        
                                                                        if z != "C":
                                                                            continue
                                                                            
                                                                        elif z == "C":
                                                                            print("Long position covered")
                                                                            print()
                                                                            money_change_long = -quantity_longed*(close[date_list.index(i)]-close[date_list.index(k)])
                                                                            portfolio_value += money_change_long
                                                                            print("*** Position Summary ***")
                                                                            print()
                                                                            print(f"You made S$ {money_change_long:,.2f} in this Long")
                                                                            print(f"Your portfolio value is now S$ {portfolio_value:,.2f}")
                                                                            print()
                                                                            exit_long_to_main_menu = 1
                                                                            break
                                                                        
                                                                    except:
                                                                        print("Please enter a supported option")
                                                                                    
                                                            elif a == "N":
                                                                print("Position aborted")
                                                                break
                                                                
                                                            else:
                                                                print("Please choose only from [Y] or [N]")
                                                                continue
                                                            
                                                            if exit_short_to_main_menu == 1 or exit_long_to_main_menu == 1:
                                                                break
                                                            
                                                        except:
                                                            print("Please provide a valid input")
                            
                                                elif long_value == 0:
                                                    print("Long position abandoned")
                                                    break
                                                
                                                else:
                                                    print("Please enter a positive number between 0 and 100")
                                                    continue
                                            
                                                if exit_long_to_main_menu == 1:
                                                    break
                                            
                                            except:
                                                print("Please enter a numeric value only")
                                    
                                    elif action == "N":
                                        continue
                                        
                                    elif action == "B":
                                        break_to_main_menu = 1
                                        #Clear the lists so that if the person goes into another simulation, the prices aren't carried forward
                                        break
                                
                                    elif action == "I":
                                        print("""
Between short selling (Shorting) and long selling (Longing), the latter is a more simple concept to understand.
    
Long-selling (Longing) involves buying a security (in our case, a stock), whose price you expect to rise in value. This is what most people intuitively do in the stock market.
So when you buy the shares of, say, Amazon, and expect to sell them in 6 months at a higher price, you are 'longing' Amazon shares.
In common parlence, saying "I am long Amazon" is essentially saying "I have bought Amazon shares expecting the price to rise"
    
-----
    
Short selling (Shorting) is where things get a bit more complicated. The basic premise to remember is that a person shorting a stock believes its value will fall.
The overall simplified process is:
    1 - An investor borrows a stock
    2 - They sell the stock
    3 - They buy the stock back to return it to the lender
                                                                
We must keep in mind here that when 'borrowing', they are borrowing 'x' shares (at $y each), and not $x*y 'worth' of shares
Ergo, they will simply need to return the 'x' number of shares, at whatever cost
    
Continuing with our Amazon example, if an investor believes the share is overvalued and likely to fall in the coming time, they will borrow 10 shares (At say $650 each)
The investor will sell these 10 shares and earn $6,500
When the price falls, the investor will then re-purchase these 10 shares at the reduced price (Let's say of $600/share)
The investor returns these 10 borrowed shares back to the lender
The investor nets 10*(650 - 600) = $500 in the shorting process""")    
                                    
                                        while True:
                                            try: 
                                                question = input("""Would you like more information on shorting/longing?:
[Y] - Yes
[N] - No: """)
            
                                                if question == "N":                                     
                                                        exit_to_main_menu = 1
                                                        break
                                                
                                                elif question == "Y":
                                                    while True:
                                                        try:
                                                            follow = input("""What do you need help with? [Answer opens up a tab in your web-browser]
[S] - Shorting             
[L] - Longing
[X] - Exit
                    
Please do note that you can come back here and open the other tab if you require!: """)
                                                
                                                            if follow == "S":
                                                                r = requests.get("https://www.investopedia.com/ask/answers/how-does-one-make-money-short-selling/")
                                                                with open("short.html","w") as file:
                                                                    file.write(r.text)
                                                                webbrowser.open_new_tab("short.html")
                                                                continue
                                                            
                                                            elif follow == "L":
                                                                q = requests.get("https://www.investopedia.com/terms/l/long.asp#:~:text=Going%20long%20on%20a%20stock,security%20in%20the%20near%20future.")
                                                                with open("long.html","w") as file:
                                                                    file.write(q.text)
                                                                webbrowser.open_new_tab("long.html")
                                                                continue
                                                            
                                                            elif follow == "X":
                                                                exit_to_main_menu = 1
                                                                break
                                                                
                                                            else:
                                                                print("Your input is unsupported. Please try again from [S], [L] or [X]")
                                                                continue
                                                            
                                                        except:
                                                            print("Please choose only from [S], [L] or [X]")
                                                            
                                                else:
                                                    print("That is not a recognised input. Please try again from [Y] or [N]")
                                                    continue
                                                
                                            except:
                                                print("Please choose only from [Y] or [N]")
    
                                    else:
                                        print()
                                        print("Please choose only from [S] [L] [I] [N] or [B]")
                                        continue
                                
                                    if exit_short_to_main_menu == 1 or exit_long_to_main_menu == 1:
                                        break
    
                                except:
                                    print()
                                    print("Please enter a valid date")

                except:
                    print()
                    print("Please enter a valid date")
        
        else:
            print()
            print("Please choose only from [X] [C] or [P]")
        
    except:
        print()
        print("Please choose only from [C], [X] or [P]")