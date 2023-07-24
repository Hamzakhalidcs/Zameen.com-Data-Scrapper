import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

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
            for i in range(1, 20):
                try:
                    url = "https://www.zameen.com/Rentals_Residential_Plots/{}-{}-{}.html".format(NUM_TO_CITY_MAPPING.get(num),num, i)
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
                            
                            if property_link_element:
                                property_link = property_link_element["href"]
                                property_title = property_link_element["title"]
                            
                            if price_element:
                                price = price_element.text.strip()
                            
                            if location_element:
                                location = location_element.text.strip()
    
                                
                            data_list.append({
                                "property_title" : property_title,
                                "price" : price,
                                "location" : location,
                                "city" : NUM_TO_CITY_MAPPING.get(num),
                                "property_link" : property_link,
                                "area" : area_span
                            }
                            )
                        count += 1
                    
                        print('{} page is append to list'.format(i))
                        print("End of Page {}".format(i))
                    print("End for the {} area".format(NUM_TO_CITY_MAPPING.get(num)))
                except Exception as exp:
                    print(f"Exception while looping on pages on city : {NUM_TO_CITY_MAPPING.get(num)}. Exception message | {exp}")
            
        except Exception as exp:
            print(f"Exception while looping on cities. Exception message | {exp}")
except Exception as e:
    print(str(e))
    print('Check the Given URL')


try:
    # Step 1: Establish a connection to the MongoDB server running on localhost port:no 27017
    client = MongoClient('localhost', 27017)

    # Step 2: Choose a database and collection to store the data
    db = client['zameen']  
    collection = db['rental_plots_data'] 

    resp = collection.insert_many(data_list)
    print (resp.inserted_ids[:5])
        # print("RESULT: ",resp)

    # Close the connection to the MongoDB server
    client.close()

    print("Data inserted into MongoDB successfully!")

except Exception as e:
    print(str(e))
    print('Error inserting data into MongoDB.')
