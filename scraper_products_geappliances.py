import json
import os
import random
import re
import time
import requests
from lxml import html
import pandas as pd
import urllib

def scrape_product_data_geappliances(model_name, all_url):
    username = "####################"
    password = "####################"
    proxy = "pr.oxylabs.io:7777"

    # Create the proxies dictionary for both HTTP and HTTPS
    proxies = {
        'http': f'http://{username}:{password}@{proxy}',
        'https': f'http://{username}:{password}@{proxy}'
    }
    model_name = str(model_name)
    if not os.path.exists("output_geappliances"):
        os.makedirs("output_geappliances")
    output_directory = os.path.join(os.getcwd(), 'output_geappliances')

    if not os.path.exists("response"):
        os.makedirs("response")
    response_directory = os.path.join(os.getcwd(), 'response')

    for source_url in all_url:
        if "https://products.geappliances.com/appliance/gea-specs" in source_url:
            data_dict = {}
            data_dict['model_name'] = model_name
            data_dict['source'] = ""
            try:
                data_dict['source'] = source_url
            except:
                data_dict['source'] = ""
            print("source", data_dict['source'])

            payload = {}
            headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
            }

            product_data = ""
            tree = ""
            try:
                # response = requests.request("GET", url=data_dict['source'],proxies=proxies, headers=headers, data=payload)
                payload = {
                        'source': 'universal',
                        'url': data_dict['source'],
                        }
                product_data_json = requests.request(
                'POST',
                'https://realtime.oxylabs.io/v1/queries',
                auth=('####################', '####################'),
                json=payload,
                )
                product_data = product_data_json.json()['results'][0]['content']
                model_name_file = re.sub(r'[<>:"/\\|?*]', '_', model_name)
                Product_html = os.path.join(response_directory, f"Product{model_name_file.replace("/", "_")}.html")
                tree = html.fromstring(product_data)
                with open(Product_html, "w", encoding="utf-8") as file:
                    file.write(product_data)
            except:
                product_data = ""
            data_dict['brand'] = "ge appliances"
            print(data_dict['brand'])
            data_dict['name'] = ""
            try:
                data_dict['name'] = tree.xpath('string(//div[@id="mainContent"]/div[2]/div[2]/h5/text())').replace("\n", "").replace("\t", "").strip()
                data_dict['name'] = data_dict['name'].encode().decode('unicode_escape')
            except:
                data_dict['name'] = ""
            print("name",data_dict['name'])
            data_dict['category'] = ""
            if data_dict['name'] != "":
                if "water heater" in data_dict['name'].lower():
                    data_dict['category'] = "water heater"
                if "condenser" in data_dict['name'].lower():
                    data_dict['category'] = "HVAC"
                if "heat pump" in data_dict['name'].lower():
                    data_dict['category'] = "HVAC"
                if "air handler" in data_dict['name'].lower():
                    data_dict['category'] = "HVAC"
                if "air condenser" in data_dict['name'].lower():
                    data_dict['category'] = "HVAC"
                if "refrigerator" in data_dict['name'].lower():
                    data_dict['category'] = "refrigerator"
                if "freezer" in data_dict['name'].lower():
                    data_dict['category'] = "refrigerator"
                if "washer" in data_dict['name'].lower():
                    data_dict['category'] = "washer and dryer"
                if "dryer" in data_dict['name'].lower():
                    data_dict['category'] = "washer and dryer"
                if "electric range" in data_dict['name'].lower():
                    data_dict['category'] = "stoves & ranges"
                if "gas range" in data_dict['name'].lower():
                    data_dict['category'] = "stoves & ranges"
                if "fuel range" in data_dict['name'].lower():
                    data_dict['category'] = "stoves & ranges"

            print("category", data_dict['category'])
            data_dict['image_url'] = ""
            try:
                data_dict['image_url'] = tree.xpath("string(//div[@id='mainContent']/div[2]/div/img/@src)")
            except:
                data_dict['image_url'] = ""
            print("image", data_dict['image_url'])
            data_dict['user_manual'] = ""
            try:
                data_dict['user_manual'] = tree.xpath('string(//img[contains(@alt, "Owner\'s Manual")]/ancestor::a/@href)')
            except:
                data_dict['user_manual'] = ""
            print("user_manual", data_dict['user_manual'])
            data_dict['Warranty_Guide'] = ""
            data_dict['Energy_Guide'] = ""
            print("data_dict", data_dict)
            return data_dict
    return {}
    
# scrape_product_data_geappliances("GP50T06AVR10")