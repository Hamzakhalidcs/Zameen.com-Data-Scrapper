import requests
import time
import unicodecsv as csv
from bs4 import BeautifulSoup

data_list = []

try:
    for i in range(1, 5):  
        url = "https://www.zameen.com/Residential_Plots/Islamabad-3-{}.html".format(i)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        listings = soup.find_all("li", attrs={"aria-label": "Listing"})
        print("Total Listings...", len(listings))
        count = 0
        for listing in listings:
            if listing:
                price_element = listing.find("span", attrs={"aria-label": "Price"})
                location_element = listing.find("div", attrs={"aria-label": "Location"})
                property_link_element = listing.find("a")
                if property_link_element:
                    property_link = property_link_element["href"]
                    property_title = property_link_element["title"]
                if price_element:
                    price = price_element.text.strip()
                if location_element:
                    location = location_element.text.strip()
                    print("Property Title: ", property_title)
                    print("Price: ", price)
                    print("Location: ", location)
                    print("*" * 60)
                    
                    data_list.append([property_title, price, location])
            count += 1
        print("End of Page {}".format(i))


except Exception as e:
    print(str(e))
    print('Check the Given URL')

file = open('export_data.csv', 'w')
writer = csv.writer(file)
headers = ['Property Title', 'Price', 'Location']
writer.writerow(headers)
writer.writerows(data_list)
print('File  process complete')