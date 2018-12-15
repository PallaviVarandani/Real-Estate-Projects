####Mecklenburg County###
###Below Code is written using Selenium Web Crawler, other method to scrape data is using the request function###
##By Pallavi Varandani


###importing packages###

from selenium import webdriver
from bs4 import BeautifulSoup
import time
import re
import pymysql
import csv


###Setting the Chromedriver Path######

path_to_chromedriver = '/Users/pallavivarandani/Documents/Top Agents/chromedriver/chromedriver'  #path to the Selenium chrome driver
driver = webdriver.Chrome(executable_path=path_to_chromedriver)
Root = 'https://property.spatialest.com/nc/mecklenburg/'

###Calling the Web Page###
driver.get(Root)
print("Connecting to the Website...")

###Filtering the Search by SINGLE FAMILY RESEDENTIAL PROPERTY####

driver.find_element_by_xpath('//*[@id="secondarySearchButton"]/span/span').click()
time.sleep(2)
driver.find_element_by_xpath('//*[@id="luc_text"]/option[32]').click()
time.sleep(2)
driver.find_element_by_xpath('//*[@id="main-app"]/div/div[1]/div/div/div[1]/div/a').click()

####Getting the Second Page Links####
##This section fetches the Page URL which have detailed information of on each of the property####

links = []
for i in range(1,41):
    Page = 'https://property.spatialest.com/nc/mecklenburg/#/search/R100_luc/'
    driver.get(Page+str(i))
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    time.sleep(1)
    for j in range(len(soup.find('div', attrs={'class':'results-list'}).find_all('div', attrs={'class':'has-image resultItem'}))):
        links.append(soup.find('div', attrs={'class':'results-list'}).find_all('div', attrs={'class':'has-image resultItem'})[j].find('li').find('a').get('href'))
        print("Page" + str(i)+"link" + str(j)) ##Printing the Index to get the track of progress
time.sleep(10)

###Extracting data of each property####
###Using the linkes extracted above, we scrape all the property related information for each property using the following set of codes####

for i in range(len(links)):
    driver.get(Root+links[i])  ###Calling each Page URL
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    time.sleep(1)

    ###Getting all the parameter/variable information of the properties####

    ListingUrl = str(Root+links[i])
    try:
       ParcelID =  str(soup.find_all('div',attrs={'class':'data-list-section'})[0].find(text = re.compile(r'Parcel ID')).findNext().text.strip())
    except:
        ParcelID = ''
    try:
        AccountNo = str(soup.find_all('div',attrs={'class':'data-list-section'})[0].find(text = re.compile(r'Account No')).findNext().text.strip())
    except:
        AccountNo = ''
    try:
        LocationAddress = str(soup.find_all('h4', attrs={'class': 'featurette-heading'})[1].findNext().find('strong').text.strip())
    except:
        LocationAddress = ''
    try:
        CurrentOwner1 = str(soup.find_all('div', attrs={'class':'data-list-section'})[2].find_all('span', attrs = {'class':'value'})[0].find('strong').text.strip())
    except:
        CurrentOwner1 = ''
    try:
        CurrentOwner2 = str(soup.find_all('div', attrs={'class':'data-list-section'})[2].find_all('span', attrs = {'class':'value'})[1].find('strong').text.strip())
    except:
        CurrentOwner2 = ''
    try:
        MailingAddress = str(soup.find_all('div', attrs={'class':'data-list-section'})[3].find('span', attrs = {'class':'value'}).text.strip())
    except:
        MailingAddress = ''
    try:
        LandUseCode = str(soup.find_all('div', attrs={'class':'data-list-section'})[4].find(text= re.compile(r'Land Use Code')).findNext().text.strip())
    except:
        LandUseCode = ''
    try:
        LandUseDesc = str(soup.find_all('div', attrs={'class':'data-list-section'})[4].find(text= re.compile(r'Land Use Desc')).findNext().text.strip())
    except:
        LandUseDesc = ''
    try:
        ExemptionOrDeferment = str(soup.find_all('div', attrs={'class':'data-list-section'})[4].find(text= re.compile(r'Exemption/Deferment')).findNext().text.strip())
    except:
        ExemptionOrDeferment = ''
    try:
        Neighborhood = str(soup.find_all('div', attrs={'class':'data-list-section'})[4].find(text= re.compile(r'Neighborhood')).findNext().text.strip())
    except:
        Neighborhood = ''
    try:
        LegalDescription = str(soup.find_all('div', attrs={'class':'data-list-section'})[4].find(text= re.compile(r'Legal Description')).findNext().text.strip())
    except:
        LegalDescription = ''
    try:
        Land = str(soup.find_all('div', attrs={'class':'data-list-section'})[4].find(text= re.compile(r'Last Sale Date')).findPrevious().findPrevious().findPrevious().text.strip())
    except:
        Land = ''
    try:
        LastSaleDate = str(soup.find_all('div', attrs={'class':'data-list-section'})[4].find(text= re.compile(r'Last Sale Date')).findNext().text.strip())
    except:
        LastSaleDate = ''
    try:
        LastSalePrice = str(soup.find_all('div', attrs={'class':'data-list-section'})[4].find(text= re.compile(r'Last Sale Price')).findNext().text.strip())
    except:
        LastSalePrice = ''
    try:
        LandValue = str(soup.find_all('div', attrs={'class':'data-list-section'})[5].find(text= re.compile(r'Land Value')).findNext().text.strip())
    except:
        LandValue = ''
    try:
        BuildingValue = str(soup.find_all('div', attrs={'class':'data-list-section'})[5].find(text= re.compile(r'Building Value')).findNext().text.strip())
    except:
        BuildingValue = ''
    try:
        Features = str(soup.find_all('div', attrs={'class':'data-list-section'})[5].find(text= re.compile(r'Features')).findNext().text.strip())
    except:
        Features = ''
    try:
        TotalAppraisedValue = str(soup.find('div', attrs={'class':'total-valuation-block row'}).find(text= re.compile(r'Total Appraised Value')).findNext().text.split(' ')[0].strip())
    except:
        TotalAppraisedValue = ''
    try:
        HeatedArea = str(soup.find_all('div', attrs={'class':'data-list-section'})[6].find(text= re.compile(r'Heated Area')).findNext().text.strip())
    except:
        HeatedArea = ''
    try:
        Heat = str(soup.find_all('div', attrs={'class':'data-list-section'})[6].find(text= re.compile(r'Year Built')).findPrevious().findPrevious().findPrevious().text.strip())
    except:
        Heat = ''
    try:
        YearBuilt = str(soup.find_all('div', attrs={'class':'data-list-section'})[6].find(text= re.compile(r'Year Built')).findNext().text.strip())
    except:
        YearBuilt = ''
    try:
        Story = str(soup.find_all('div', attrs={'class': 'data-list-section'})[6].find(text=re.compile(r'Story')).findNext().text.strip())
    except:
        Story = ''
    try:
        BuiltUseorStyle = str(soup.find_all('div', attrs={'class': 'data-list-section'})[6].find(text=re.compile(r'Built Use / Style')).findNext().text.strip())
    except:
        BuiltUseorStyle = ''
    try:
        Fuel = str(soup.find_all('div', attrs={'class': 'data-list-section'})[6].find(text=re.compile(r'Fuel')).findNext().text.strip())
    except:
        Fuel = ''
    try:
        Foundation = str(soup.find_all('div', attrs={'class': 'data-list-section'})[6].find(text=re.compile(r'Foundation')).findNext().text.strip())
    except:
        Foundation = ''
    try:
        ExternalWall = str(soup.find_all('div', attrs={'class': 'data-list-section'})[6].find(text=re.compile(r'Ex')).findNext().text.strip())
    except:
        ExternalWall = ''
    try:
        FirePlaces = str(soup.find_all('div', attrs={'class': 'data-list-section'})[6].find(text=re.compile(r"Fireplace")).findNext().text.strip())
    except:
        FirePlaces = ''
    try:
        HalfBaths = str(soup.find_all('div', attrs={'class': 'data-list-section'})[6].find(text=re.compile(r"Half Bath")).findNext().text.strip())
    except:
        HalfBaths = ''
    try:
        FullBaths = str(soup.find_all('div', attrs={'class': 'data-list-section'})[6].find(text=re.compile(r"Full Bath")).findNext().text.strip())
    except:
        FullBaths = ''
    try:
        Bedrooms = str(soup.find_all('div', attrs={'class': 'data-list-section'})[6].find(text=re.compile(r"Bedroom")).findNext().text.strip())
    except:
        Bedrooms = ''
    try:
        TotalSqFt = str(soup.find_all('div', attrs={'class': 'data-list-section'})[6].find(text=re.compile(r"SqFt")).findNext().text.strip())
    except:
        TotalSqFt = ''
    try:
        Units = str(soup.find_all('div',attrs={'class':'data-list-section'})[7].find(text=re.compile(r'Units')).findNext().text.strip())
    except:
        Units = ''

    ###Storing as a local CSV file#####
    #### Below we Store the data extracted in CSV format###

    rows = [ListingUrl,ParcelID,AccountNo,LocationAddress,CurrentOwner1,CurrentOwner2,MailingAddress,LandUseCode,LandUseDesc,ExemptionOrDeferment,Neighborhood,LegalDescription,Land,
            LastSaleDate,LastSalePrice,LandValue,BuildingValue,Features,TotalAppraisedValue,HeatedArea,Heat,YearBuilt,Story,BuiltUseorStyle,Fuel,Foundation,ExternalWall,
            FirePlaces,HalfBaths,FullBaths,Bedrooms,TotalSqFt,Units]
    with open('/Users/pallavivarandani/Documents/Landis/Mecklenburg.csv','a') as outfile:
        writer = csv.writer(outfile)
        if (i == 0):
            writer.writerow(
                ['ListingUrl', 'ParcelID', 'AccountNo', 'LocationAddress', 'CurrentOwner1', 'CurrentOwner2', 'MailingAddress',
                 'LandUseCode', 'LandUseDesc', 'ExemptionOrDeferment', 'Neighborhood', 'LegalDescription', 'Land',
                 'LastSaleDate', 'LastSalePrice', 'LandValue', 'BuildingValue', 'Features', 'TotalAppraisedValue', 'HeatedArea', 'Heat',
                 'YearBuilt', 'Story', 'BuiltUseorStyle', 'Fuel', 'Foundation', 'ExternalWall',
                 'FirePlaces', 'HalfBaths', 'FullBaths', 'Bedrooms', 'TotalSqFt', 'Units'])
        writer.writerow(rows)
        print("index = " + str(i) + "local") ##Printing the Index to get the track of progress

    ###Loading into the MySQL Database####
    ####Here, we Load the data being scraped into the localhost SQL Database####

    t = (ListingUrl, ParcelID, AccountNo, LocationAddress,CurrentOwner1,CurrentOwner2,MailingAddress,LandUseCode,LandUseDesc,
         ExemptionOrDeferment,Neighborhood,LegalDescription,Land,LastSaleDate,LastSalePrice,LandValue,BuildingValue,Features,
         TotalAppraisedValue,HeatedArea,Heat,YearBuilt,Story,BuiltUseorStyle,Fuel,Foundation,ExternalWall,FirePlaces,HalfBaths,FullBaths,Bedrooms,TotalSqFt,Units)
    con = pymysql.connect(host='localhost',
                          user='root',
                          password='Vansh@1234',
                          autocommit=True,
                          local_infile=1,
                          db='landis')
    print('Connected to DB: {}'.format('localhost'))
    # Create cursor and execute Load SQL
    cursor = con.cursor()
    cursor.execute('INSERT INTO Mecklenburg(ListingUrl,ParcelID, AccountNo, '
                   'LocationAddress,CurrentOwner1,CurrentOwner2,MailingAddress,'
                   'LandUseCode,LandUseDesc,ExemptionOrDeferment,Neighborhood,LegalDescription,Land,LastSaleDate,LastSalePrice,'
                   'LandValue,BuildingValue,Features,TotalAppraisedValue,HeatedArea,Heat,YearBuilt,Story,BuiltUseorStyle,Fuel,Foundation,'
                   'ExternalWall, FirePlaces,HalfBaths,FullBaths,Bedrooms,TotalSqFt,Units) '
                   'VALUES ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s",'
                   '"%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")', t)
    print('Succuessfully loaded the data.')
    con.close()
    print("index = " + str(i) + "database") ##Printing the Index to get the track of progress




