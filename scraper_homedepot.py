import json
import os
import random
import re
import time
import requests
from lxml import html
import pandas as pd


def scrape_product_data_homedepot(model_name, all_url):
    username = "####################"
    password = "####################"
    proxy = "pr.oxylabs.io:7777"

    # Create the proxies dictionary for both HTTP and HTTPS
    proxies = {
        'http': f'http://{username}:{password}@{proxy}',
        'https': f'http://{username}:{password}@{proxy}'
    }
    model_name = str(model_name)
    if not os.path.exists("homedepot_400"):
        os.makedirs("homedepot_400")
    output_directory = os.path.join(os.getcwd(), 'homedepot_400')

    if not os.path.exists("response"):
        os.makedirs("response")
    response_directory = os.path.join(os.getcwd(), 'response')
    # if model_name is not None:
    #     data_dict = {}
    #     print(model_name)
    #     data_dict['model_name'] = model_name
    #     time.sleep(random.uniform(20, 25))
    #     url = f"https://www.google.com/search?q={model_name}"
    #     google_headers = {
    #                 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    #                 'Authorization': '43544ed2b7944a5c9ecada56b3c12426'
    #             }
    #     response = ""
    #     tree = ""
    #     try:
    #         response = requests.get(url, headers=google_headers)
    #         tree = html.fromstring(response.text)
    #         model_name_file = re.sub(r'[<>:"/\\|?*]', '_', model_name)
    #         url_l_html = os.path.join(response_directory, f"URL_{model_name_file.replace("/", "_")}.html")
    #         with open(url_l_html, "w", encoding="utf-8") as file:
    #             file.write(response.text)
    #     except:
    #         response = ""
    #         tree = ""
    #     all_url = []
    #     try:
    #         all_url = tree.xpath(f'//div[@id="main"]//div[contains(text(),{model_name})]/parent::h3/parent::div/parent::div/parent::a/@href')
    #     except:
    #         try:
    #             all_url = tree.xpath('//a[contains(@href, "www.homedepot.com")]/@href')
    #         except:
    #             all_url = []
    print(all_url)
    for source_url in all_url:
        data_dict = {}
        if "/questions/" in source_url:
            continue
        if "www.homedepot.com" in source_url:
            data_dict['model_name'] = model_name
            data_dict['source'] = ""
            try:
                data_dict['source'] = source_url
            except:
                data_dict['source'] = ""
            print("source", data_dict['source'])

            payload = {}
            headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'priority': 'u=0, i',
            'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
            'Authorization': '43544ed2b7944a5c9ecada56b3c12426'
            }
            product_data = ""
            tree = ""
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
                # response = requests.request("GET", url=data_dict['source'],proxies=proxies, headers=headers, data=payload)
                tree = html.fromstring(product_data)
                model_name_file = re.sub(r'[<>:"/\\|?*]', '_', model_name)
                Product_html = os.path.join(response_directory, f"Product{model_name_file.replace("/", "_")}.html")
                with open(Product_html, "w", encoding="utf-8") as file:
                    file.write(product_data)
            except:
                product_data = ""
                tree = ""
            data_dict['brand'] = ""
            try:
                data_dict['brand'] = tree.xpath('string(//h1/parent::span/parent::div/preceding-sibling::div/div/a/span/div/h2/text())')
            except:
                data_dict['brand'] = ""
            data_dict['name'] = ""
            try:
                data_dict['name'] = tree.xpath('string(//h1/text())')
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


            print("category", data_dict['category'])
            data_dict['image_url'] = ""
            try:
                data_dict['image_url'] = product_data.split('<img data-testid="small-image" src="')[1].split('"')[0]
            except:
                data_dict['image_url'] = ""
            print("image_url" , data_dict['image_url'] )
            print(data_dict['brand'])
            
            print(data_dict['name'])
            data_list = []
            json_string = ""
            try:
                json_string = product_data.split('"infoAndGuides":')[1].split(',"installationAndRentals":')[0]
                data_list = json.loads(json_string)
            except:
                data_list = []
                json_string = ""
            data_dict['user_manual'] = ""
            data_dict['Warranty_Guide'] = ''
            data_dict['Energy_Guide'] = ""
            for document in data_list:
                if 'Energy Guide' in document['name']:
                    data_dict['Energy_Guide'] = document["url"]
                if 'Use and Care Manual' in document['name']:
                    data_dict['user_manual'] = document["url"]
                if 'Warranty' in document['name']:
                    data_dict['Warranty_Guide'] = document["url"]
            if data_dict['user_manual'] == "":
                for document in data_list:
                    if 'Installation Guide' in document['name']:
                        data_dict['user_manual'] = document["url"]

            print(data_dict['user_manual'])
            print("Energy_Guide" , data_dict['Energy_Guide'])
            print(data_dict)
        
            # model_name_file = re.sub(r'[<>:"/\\|?*]', '_', model_name)
            # model_dir_path = os.path.join(output_directory, model_name_file.replace("/", "_"))
            # if not os.path.exists(model_dir_path):
            #     os.makedirs(model_dir_path)
            # output_data = os.path.join(model_dir_path, f"{model_name_file.replace("/", "_")} output_data.xlsx")
            # df = pd.DataFrame([data_dict])
            # df.to_excel(output_data, index=False)
            return data_dict

    return {}

# scrape_product_data_homedepot("XE50T09EL45U1")