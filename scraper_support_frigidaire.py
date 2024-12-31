import json
import os
import random
import re
import time
import requests
from lxml import html
import pandas as pd

def scrape_product_support_frigidaire(model_name,all_url):
    username = "####################"
    password = "####################"
    proxy = "pr.oxylabs.io:7777"

    # Create the proxies dictionary for both HTTP and HTTPS
    proxies = {
        'http': f'http://{username}:{password}@{proxy}',
        'https': f'http://{username}:{password}@{proxy}'
    }
    model_name = str(model_name)
    if not os.path.exists("output_frigidaire"):
        os.makedirs("output_frigidaire")
    output_directory = os.path.join(os.getcwd(), 'output_frigidaire')

    if not os.path.exists("response"):
        os.makedirs("response")
    response_directory = os.path.join(os.getcwd(), 'response')
    print(all_url)
    for source_url in all_url:

        if "www.frigidaire.ca" in source_url or "support.frigidaire.com" in source_url:
            data_dict = {}
            print(model_name)
            data_dict['model_name'] = model_name
            data_dict['source'] = ""
            try:
                data_dict['source'] = source_url
            except:
                data_dict['source'] = ""
            print("source", data_dict['source'])
            data_dict['brand'] = "frigidaire"

            payload = {}
            headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
            }

            product_data = ""
            tree =""
            try:
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
                # response = requests.request("POST", url=data_dict['source'],proxies=proxies, headers=headers, data=payload)
                model_name_file = re.sub(r'[<>:"/\\|?*]', '_', model_name)
                Product_html = os.path.join(response_directory, f"Product{model_name_file.replace("/", "_")}.html")
                with open(Product_html, "w", encoding="utf-8") as file:
                    file.write(product_data) 
                tree = html.fromstring(product_data)
            except:
                product_data = ""
                tree =""
            data_dict['name'] = ""
            try:
                data_dict['name'] = tree.xpath('string(//div[@id="pdp-sku"]/text())')
                print(data_dict['name'])
            except:
                data_dict['name'] = ""
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
            data_dict['image_url'] = ""
            try:
                data_dict['image_url'] = tree.xpath('string(//div[@id="pdp-sku"]/parent::div/parent::div/following-sibling::div/img/@src)')
            except:
                data_dict['image_url'] = ""
            print("image",data_dict['image_url'])
            data_dict['user_manual'] = ""
            try:
                data_dict['user_manual'] = tree.xpath('string(//p[contains(text(), "Complete Owner\'s Guide")]/parent::div/following-sibling::div/p[contains(text(), "English")]//parent::div/parent::div/parent::a/@href)')
            except:
                data_dict['user_manual'] = ""
            
            if data_dict['user_manual'] == "":
                try:
                    data_dict['user_manual'] = tree.xpath('string(//p[contains(text(), "Installation Instructions")]/parent::div/following-sibling::div/p[contains(text(), "English")]//parent::div/parent::div/parent::a/@href)')
                except:
                    data_dict['user_manual'] = ""
            print('user_manual',data_dict['user_manual'])
            data_dict['Warranty_Guide'] = ""
            data_dict['Energy_Guide'] = ""
            try:
                data_dict['Energy_Guide'] = tree.xpath('string(//p[contains(text(), "Energy Guide")]/parent::div/following-sibling::div/p[contains(text(), "English")]//parent::div/parent::div/parent::a/@href)')
            except:
                data_dict['Energy_Guide'] = ""
            print('Energy_Guide',data_dict['Energy_Guide'])
            print(data_dict)
            # model_name_file = re.sub(r'[<>:"/\\|?*]', '_', model_name)
            # model_dir_path = os.path.join(output_directory, model_name_file.replace("/", "_"))
            # if not os.path.exists(model_dir_path):
            #     os.makedirs(model_dir_path)
            # output_data = os.path.join(model_dir_path, f"{model_name_file.replace("/", "_")} output_data.xlsx")
            # df = pd.DataFrame([data_dict])
            # df.to_excel(output_data, index=False)

            return data_dict
            # break

    return {}

# scrape_product_support_frigidaire("FGBM19WNVFB")