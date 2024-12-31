import json
import os
import re
import time
import requests
from lxml import html
import pandas as pd

def scrape_product_samsung_us(model_name, all_url):
    model_name = str(model_name)
    username = "####################"
    password = "####################"
    proxy = "pr.oxylabs.io:7777"

    # Create the proxies dictionary for both HTTP and HTTPS
    proxies = {
        'http': f'http://{username}:{password}@{proxy}',
        'https': f'http://{username}:{password}@{proxy}'
    }
    if not os.path.exists("samsung_us"):
        os.makedirs("samsung_us")
    output_directory = os.path.join(os.getcwd(), 'samsung_us')

    if not os.path.exists("response"):
        os.makedirs("response")
    response_directory = os.path.join(os.getcwd(), 'response')
    print(all_url)
    for source_url in all_url:

        if "www.samsung.com/us" in source_url:
            data_dict = {}
            data_dict['model_name'] = model_name
            data_dict['source'] = ""
            try:
                data_dict['source'] = source_url
            except Exception as e:
                print(f"error in {e}")
            print(data_dict['source'])
            data_dict["brand"] = "samsung"
            product_data = ""
            tree = ""
            # payload = {}
            # headers = {
            # 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
            # }
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
                with open(Product_html, "w", encoding="utf-8") as file:
                    file.write(product_data)
                tree = html.fromstring(product_data)
            except Exception as e:
                product_data = ""
                tree = ""
                print(f"error in {e}")
            data_dict["name"] = ""
            try:
                data_dict["name"] = tree.xpath("string(//h1[@class='product-top-nav__font-name']/text())")
            except Exception as e:
                print(f"error in {e}")
            print("name", data_dict["name"])
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
            data_dict["image_url"] = ""
            try:
                data_dict["image_url"] = tree.xpath('string(//div[@class="product-details__photo"]/div/div/picture/img/@src)')
            except Exception as e:
                print(f"error in {e}")
            print("image_url", data_dict["image_url"])
            data_dict["user_manual"] = ""
            try:
                data_dict["user_manual"] = tree.xpath("string(//h3[contains(text(), 'User Manual')]/parent::div/following::div[1]/a/@href)")
            except Exception as e:
                print(f"errro in {e}")
            data_dict["Warranty_Guide"] = ""
            data_dict["Energy_Guide"] = "" 
            try:
                data_dict["Energy_Guide"] = tree.xpath("string(//h3[contains(text(), 'Energy Guide')]/parent::div/following-sibling::div/a/@href)")
            except Exception as e:
                print(f"error in {e} ")
            print(data_dict["Energy_Guide"], "AAAAAAAAA")
            print(data_dict)
            return data_dict
    return {}