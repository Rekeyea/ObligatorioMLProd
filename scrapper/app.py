import os
import requests
import json
import time
import unicodedata
import csv
import pandas as pd
import shutil
from bs4 import BeautifulSoup


def scraper_shopify(web):
    product_list = []

    # Initialize page variable for pagination
    page = 1
    # Maximum number of pages
    max_pages = 8

    while page <= max_pages:
        # Add page parameter with the current page number
        url = f'{web}/products.json?limit=250&page={page}'
        r = requests.get(url)
        data = r.json()

        # Check if the 'products' field in the JSON response is empty, and break the loop if it is
        if len(data['products']) == 0:
            break
            
        for item in data['products']:
            title = item['title']
            raw_body_html = item['body_html']

            # Remove HTML tags from body_html using BeautifulSoup
            no_ufeff= raw_body_html.replace('\ufeff', '')
            no_xao = unicodedata.normalize("NFKD", no_ufeff)
            soup = BeautifulSoup(no_xao, 'html.parser')
            body_html = soup.get_text()

            # Remove newline characters and replace them with spaces
            body_html = body_html.replace('\n', ' ').strip()

            # Get up to 3 images for the product
            images = item['images']
            image_list = []
            for i in range(min(3, len(images))):
                image_list.append(images[i]['src'])
            
            # Get the price and availability of the first variant
            first_variant = item['variants'][0] if item['variants'] else None
            price = first_variant['price'] if first_variant else 'N/A'
            available = first_variant['available'] if first_variant else False

            product = {
                'title': title,
                'description': body_html,
                'images': image_list,
                'price': price
            }

            product_list.append(product)

        # Increment the page number to fetch the next page
        page += 1
        # Add a short delay to avoid overloading the server with requests
        time.sleep(1)

    print(len(product_list))
    return product_list


def save_to_csv(product_list, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['title', 'description', 'images', 'price']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for product in product_list:
            # Join images list into a single string
            product['images'] = ', '.join(product['images'])

            writer.writerow(product)


def merge_csv_files(filenames):
    dataframes = []

    for filename in filenames:
        df = pd.read_csv(filename)
        dataframes.append(df)

    merged_df = pd.concat(dataframes, ignore_index=True)
    return merged_df

def download_image(url, path):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(path, 'wb') as file:
            shutil.copyfileobj(response.raw, file)

        print(f"Image downloaded: {path}")
        return True
    except Exception as e:
        print(f"Failed to download image: {url}. Error: {str(e)}")
        return False

def download_images_from_csv(csv_file, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    with open(csv_file, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            images = row['images'].split(', ')

            for image_url in images:
                # Extract the image filename from the URL
                image_filename = image_url.split('/')[-1]

                # Check if the file is already downloaded
                output_path = os.path.join(output_folder, image_filename)
                if os.path.exists(output_path):
                    print(f"Skipping image {output_path}: already exists")
                    continue

                # Download the image
                download_image(image_url, output_path)


## Examples to run the functions

## Scrapping to csv
example = "https://www.tupperware.com.mx/"
scrapped = scraper_shopify(example)
save_to_csv(scrapped, 'products_tupperware.csv')

## Merging multiple csv into one

filenames = [
    'products_tupperware.csv',
    'products_newera.csv',
    'products_allnutrition.csv',
    'products_grandvision.csv',
    'products_kitchencenter.csv',
    'products_chemist.csv',
    'products_pocho.csv'
]
merged_df = merge_csv_files(filenames)
merged_df.to_csv('merged_products.csv', index=False)

### Download images from csv, arguments fro download_images_from_csv are csv file and destiny folder

download_images_from_csv('products_tupperware.csv', 'img_tupperware')