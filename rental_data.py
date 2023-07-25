import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import csv

data_list = []

NUM_TO_CITY_MAPPING = {
    1 : "Lahore",
    2 : "Karachi",
    3 : "Islamabad",
    4 : "Lahore",
    5 : "Karachi_Clifton"
}
try:
    for num in range(1,6):
        try:
            for i in range(1, 3):
                try:
                    url = "https://www.zameen.com/Rentals_Houses_Property/{}-{}-{}.html".format(NUM_TO_CITY_MAPPING.get(num),num, i)
                    print(url)
                    response = requests.get(url)

                    soup = BeautifulSoup(response.text, "html.parser")

                    listings = soup.find_all("li", attrs={"aria-label": "Listing"})
                    count = 0

                    for listing in listings:
                        if listing:
                            price_element = listing.find("span", attrs={"aria-label": "Price"})

                            location_element = listing.find("div", attrs={"aria-label": "Location"})
                            
                            property_link_element = listing.find("a")
                            
                            area_element = listing.find("span", attrs = {"aria-label" : "Area"})
                            
                            area_span = area_element.find("span").text.strip()
                            
                            beds_element = listing.find("span", attrs = {"aria-label" : "Beds"})
                            
                            baths_element = listing.find("span", attrs = {"aria-label" : "Baths"})

                            if beds_element:
                                beds = beds_element.text.strip()
                                # print('Number of Beds :', beds)
                            else:
                                beds = "Nan"
                                print("Not Found")

                            if baths_element:
                                total_baths = baths_element.text.strip()
                                # print('Total Baths', total_baths)
                            else:
                                total_baths = "Nan"
                                print("Not Found")
                            
                            if property_link_element:
                                property_link = property_link_element["href"]
                                property_title = property_link_element["title"]
                                # print(property_link)
                                # print(property_title)
                            
                            if price_element:
                                price = price_element.text.strip()
                                # print(price)

                            if location_element:
                                location = location_element.text.strip()
                                print(location)
                                
                            data_list.append({
                                "property_title" : property_title,
                                "price" : price,
                                "location" : location,
                                "city" : NUM_TO_CITY_MAPPING.get(num),
                                "Total Number of Beds" : beds,
                                "Total Number of Baths" : total_baths,
                                "area" : area_span,
                                # "property_link" : property_link
                                
                            }
                            )
                            count += 1
                            print('{} page data is appended to list'.format(i))
                            print("End of Page {}".format(i))
                    print("End for the {} area".format(NUM_TO_CITY_MAPPING.get(num)))
                except Exception as exp:
                    print(f"Exception while looping on pages on city : {NUM_TO_CITY_MAPPING.get(num)}. Exception message | {exp}")
            
        except Exception as exp:
            print(f"Exception while looping on cities. Exception message | {exp}")
except Exception as e:
    print(str(e))
    print('Check the Given URL')

print("Total records scrapped: ",len(data_list))
print("Sample Data list: ", data_list[:3])
target_file = open('rental_data1.csv', 'w')
writer = csv.writer(target_file)
headers = ['Property Title', 'Price', 'Location', 'City', 'Total Number of Beds', 'Total Number of Baths', 'area']
writer.writerow(headers)
writer.writerows(data_list)
target_file.close()

print('File process complete.')


# try:
#     # Step 1: Establish a connection to the MongoDB server running on localhost port:no 27017
#     client = MongoClient('localhost', 27017)

#     # Step 2: Choose a database and collection to store the data
#     db = client['zameen']  
#     collection = db['rental_plots_data'] 

#     resp = collection.insert_many(data_list)
#     print (resp.inserted_ids[:5])
#         # print("RESULT: ",resp)

#     # Close the connection to the MongoDB server
#     client.close()

#     print("Data inserted into MongoDB successfully!")

# except Exception as e:
#     print(str(e))
#     print('Error inserting data into MongoDB.')