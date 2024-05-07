import requests
from bs4 import BeautifulSoup
import urllib.request
import os
import csv
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Airtable personal access token and base information
AIRTABLE_ACCESS_TOKEN = os.getenv('AIRTABLE_ACCESS_TOKEN')
AIRTABLE_BASE_ID = os.getenv('AIRTABLE_BASE_ID')
AIRTABLE_TABLE_NAME = os.getenv('AIRTABLE_TABLE_NAME')

# Change as needed
CSV_DIRECTORY = os.getenv('CSV_DIRECTORY')

# Function to upload image metadata to Airtable
def upload_image_metadata_to_airtable(image_name, image_url, image_link):
    # Airtable API endpoint URL
    endpoint_url = f'https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_NAME}'

    # Prepare data to be sent to Airtable
    data = {
        "fields": {
            "Name": image_name,
            "Image File": [{"url": image_url}],
            "URL": image_link,
            "Note": 'N/A'
        }
    }

    # Set up headers with access token for authorization
    headers = {
        'Authorization': f'Bearer {AIRTABLE_ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }

    try:
        # Make POST request to Airtable API to create a new record
        response = requests.post(endpoint_url, json=data, headers=headers)

        # Check if request was successful
        if response.status_code == 200:
            successful = "Success"
        else:
            print(f"Failed to upload image metadata to Airtable. Status code: {response.status_code}")
            print(f"Response content: {response.content}")
    except Exception as e:
        print(f"Error uploading image metadata to Airtable: {e}")
        print(f"Response content: {response.content}")


def save_first_image_to_airtable(keyword):
    # Construct the URL based on the keyword
    url = f"https://unsplash.com/s/photos/{keyword}"
    source_code = requests.get(url)
    plain_text = source_code.text

    # Parse HTML response to find image URL
    soup = BeautifulSoup(plain_text, 'html.parser')
    img_tags = soup.find_all('img')

    if img_tags:
        # Get the source URL of the first image found
        first_image_src = img_tags[2].get("src")
        if first_image_src:
            # Generate a name for the image
            image_name = keyword

            try:

                # Upload image metadata to Airtable
                image_description = f"Image of {keyword}"
                upload_image_metadata_to_airtable(image_name, first_image_src, first_image_src)
            except Exception as e:
                print(f"Error uploading image metadata to Airtable: {e}")
        else:
            print("No image source found on the webpage.")
    else:
        print("No images found on the webpage.")

if __name__ == "__main__":
    # Open CSV file and read food names from 'foodName' column
    csv_file = CSV_DIRECTORY
    with open(csv_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            food_name = row['foodName']

            # Call the function to save the first image metadata to Airtable for each food name
            save_first_image_to_airtable(food_name)

