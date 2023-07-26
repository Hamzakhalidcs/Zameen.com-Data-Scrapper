import requests,os
from bs4 import BeautifulSoup
import pandas as pd
from pymongo import MongoClient

# Function to read the .env file and set the environment variables
def load_env():
    env_file = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_file):
        with open(env_file) as f:
            for line in f:
                key, value = line.strip().split('=', 1)
                os.environ[key] = value

# Load environmental variable from .env file 
load_env()

# Fetch the environment variables
mongo_host = os.environ.get('MONGO_HOST')
mongo_port = int(os.environ.get('MONGO_PORT'))
mongo_db_name = os.environ.get('MONGO_DB_NAME')
mongo_collection_name = os.environ.get('Mongo_Rental_collection')


data_list = []

NUM_TO_CITY_MAPPING = {
    1: "Lahore",
    2: "Karachi",
    3: "Islamabad",
    4: "Lahore",
    5: "Karachi_Clifton"
}

try:
    for num in range(1, 6):
        try:
            for i in range(1, 3):
                try:
                    url = "https://www.zameen.com/Rentals_Houses_Property/{}-{}-{}.html".format(NUM_TO_CITY_MAPPING.get(num), num, i)
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
                            area_element = listing.find("span", attrs={"aria-label": "Area"})
                            beds_element = listing.find("span", attrs={"aria-label": "Beds"})
                            baths_element = listing.find("span", attrs={"aria-label": "Baths"})

                            property_title = property_link_element.get("title") if property_link_element else "N/A"
                            price = price_element.text.strip() if price_element else "N/A"
                            location = location_element.text.strip() if location_element else "N/A"
                            beds = beds_element.text.strip() if beds_element else "N/A"
                            total_baths = baths_element.text.strip() if baths_element else "N/A"
                            area_span = area_element.find("span").text.strip() if area_element else "N/A"

                            data_list.append({
                                "Property Title": property_title,
                                "Price": price,
                                "Location": location,
                                "City": NUM_TO_CITY_MAPPING.get(num),
                                "Total Number of Beds": beds,
                                "Total Number of Baths": total_baths,
                                "Area": area_span
                            })
                            count += 1
                            print('{} page data is appended to list'.format(i))
                            print("End of Page {}".format(i))
                    print("End for the {} area".format(NUM_TO_CITY_MAPPING.get(num)))
                except Exception as exp:
                    print("Exception while looping on pages on city : {}. Exception message | {}".format(NUM_TO_CITY_MAPPING.get(num), exp))

        except Exception as exp:
            print("Exception while looping on cities. Exception message | {}".format(exp))
except Exception as e:
    print(str(e))
    print('Check the Given URL')

print("Total records scraped: ", len(data_list))
print("Sample Data list: ", data_list[:3])


try:
    # Step 1: Establish a connection to the MongoDB server running on localhost
    client = MongoClient(mongo_host, mongo_port)

    # Step 2: Choose a database and collection to store the data
    db = client[mongo_db_name]  
    collection = db[mongo_collection_name]


    # Step 3: Insert data into MongoDB collection
    resp = collection.insert_many(data_list)
    # resp = collection.insert(data_list)
   
    print(resp.inserted_ids[:5])

    # Close the connection to the MongoDB server
    client.close()

    print("Data inserted into MongoDB successfully!")

except Exception as e:
    print(str(e))
    print('Error connecting to MongoDB or inserting data.')



# Convert data_list to a DataFrame
# df = pd.DataFrame(data_list)

# Save DataFrame to CSV file
# df.to_csv('rental_plots_data.csv', index=False)

# print('File process complete.')
