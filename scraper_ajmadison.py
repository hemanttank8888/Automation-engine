import json
import os
import random
import re
import time
import requests
from lxml import html
import pandas as pd
from scraper_homedepot import scrape_product_data_homedepot
from scraper_products_geappliances import scrape_product_data_geappliances
from scraper_support_frigidaire import scrape_product_support_frigidaire
from www_samsung_us_com import scrape_product_samsung_us


def scrape_product_data_ajmadison(model_name):
    username = "####################"
    password = "####################"
    proxy = "pr.oxylabs.io:7777"

    # Create the proxies dictionary for both HTTP and HTTPS
    proxies = {
        'http': f'http://{username}:{password}@{proxy}',
        'https': f'http://{username}:{password}@{proxy}'
    }
    model_name = str(model_name)
    if not os.path.exists("ajmadison_com"):
        os.makedirs("ajmadison_com")
    output_directory = os.path.join(os.getcwd(), 'ajmadison_com')

    if not os.path.exists("response"):
        os.makedirs("response")
    response_directory = os.path.join(os.getcwd(), 'response')
    if model_name is not None:
        # time.sleep(random.uniform(20, 25))
        api_response = ""
        tree = ""
        all_url_ajmadison = []
        all_url_homedepot = []
        all_url_geappliances = []
        all_url_frigidaire_ca = []
        all_url_frigidaire_com = []
        all_url_samsung_us = []
        for i in range(0, 5):
            # time.sleep(random.uniform(20, 25))
            new_string = model_name[:-i]
            if i == 0:
                new_string = model_name
            # url = f"https://www.google.com/search?q={new_string}"
            print(new_string)

            try:
                payload = {
                            'source': 'google_search',
                            'query': new_string,
                            }
                # api_response = requests.get(url, proxies=proxies)
                api_response_json = requests.request(
                                            'POST',
                                            'https://realtime.oxylabs.io/v1/queries',
                                            auth=('####################', '####################'),
                                            json=payload,
                                            )
                api_response = api_response_json.json()['results'][0]['content']
                # api_response = requests.post(
                #     "https://api.zyte.com/v1/extract",
                #     auth=("43544ed2b7944a5c9ecada56b3c12426", ""),
                #     json={
                #         "url": url,
                #         "browserHtml": True,
                #     },
                # )
                # browser_html: str = api_response.json()["browserHtml"]
                tree = html.fromstring(api_response)
                try:
                    all_url_ajmadison = tree.xpath('//a[contains(@href, "www.ajmadison.com")]/@href')
                except:
                    all_url_ajmadison = []
                try:
                    all_url_homedepot = tree.xpath('//a[contains(@href, "www.homedepot.com")]/@href')
                except:
                    all_url_homedepot = []
                try:
                    all_url_frigidaire_ca = tree.xpath('//a[contains(@href, "www.frigidaire.ca")]/@href')
                except:
                    all_url_frigidaire_ca = []
                try:
                    all_url_frigidaire_com = tree.xpath('//a[contains(@href, "support.frigidaire.com")]/@href')
                except:
                    all_url_frigidaire_com = []
                try:
                    all_url_samsung_us = tree.xpath('//a[contains(@href, "www.samsung.com/us")]/@href')
                except:
                    all_url_samsung_us = []
                try:
                    all_url_geappliances = tree.xpath('//a[contains(@href, "https://products.geappliances.com/appliance/gea-specs")]/@href')
                except:
                    all_url_geappliances = []
                model_name_file = re.sub(r'[<>:"/\\|?*]', '_', model_name)
                url_l_html = os.path.join(response_directory, f"URL_{model_name_file.replace("/", "_")}.html")
                with open(url_l_html, "w", encoding="utf-8") as file:
                    file.write(api_response)
                if "www.homedepot.com" in api_response:
                    print("homedepot.com  AAAAAAAAAAAAAAAAAAAAAA")
                    print(all_url_homedepot, "all_url_homedepot")
                    return scrape_product_data_homedepot(model_name, all_url_homedepot)
                if "https://products.geappliances.com/appliance/gea-specs" in api_response:
                    print("https://products.geappliances.com/appliance/gea-specs  AAAAAAAAAAAAAAAAAAAAAA")
                    print(all_url_geappliances, "all_url_geappliances")
                    return scrape_product_data_geappliances(model_name, all_url_geappliances)
                if "www.frigidaire.ca" in api_response:
                    print("www.frigidaire.ca  AAAAAAAAAAAAAAAAAAAAAA")
                    return scrape_product_support_frigidaire(model_name, all_url_frigidaire_ca)
                if "support.frigidaire.com" in api_response:
                    print("support.frigidaire.com  AAAAAAAAAAAAAAAAAAAAAA")
                    return scrape_product_support_frigidaire(model_name, all_url_frigidaire_com)
                if "www.samsung.com/us" in api_response:
                    print("www.samsung.com/us  AAAAAAAAAAAAAAAAAAAAAA")
                    return scrape_product_samsung_us(model_name, all_url_samsung_us)
                if "www.ajmadison.com" in api_response:
                    break
            except:
                api_response = ""
                tree = ""

        print(all_url_ajmadison)
        for source_url in all_url_ajmadison:
            if "www.ajmadison.com" in source_url:
                data_dict = {}
                data_dict['model_name'] = model_name
                print("all_url", all_url_ajmadison)
                data_dict['source'] = ""
                try:
                    source = source_url
                    data_dict['source'] = source
                except:
                    data_dict['source'] = ""
                # payload = {}
                headers = {
                        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                        'accept-language': 'en-US,en;q=0.9',
                        'cache-control': 'max-age=0',
                        'priority': 'u=0, i',
                        'referer': 'https://www.google.com/',
                        'sec-ch-ua-mobile': '?0',
                        'sec-ch-ua-platform': '"Windows"',
                        'sec-fetch-dest': 'document',
                        'sec-fetch-mode': 'navigate',
                        'sec-fetch-site': 'cross-site',
                        'sec-fetch-user': '?1',
                        'upgrade-insecure-requests': '1',
                        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',                }

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
                    # product_data = requests.request("GET", url=data_dict['source'], proxies=proxies, headers=headers, data=payload)
                    # api_response = requests.post(
                    #     "https://api.zyte.com/v1/extract",
                    #     auth=("43544ed2b7944a5c9ecada56b3c12426", ""),
                    #     json={
                    #         "url": source,
                    #         "browserHtml": True,
                    #     },
                    # )
                    # product_data: str = api_response.json()["browserHtml"]
                    tree = html.fromstring(product_data)
                    model_name_file = re.sub(r'[<>:"/\\|?*]', '_', model_name)
                    Product_html = os.path.join(response_directory, f"Product{model_name_file.replace("/", "_")}.html")
                    with open(Product_html, "w", encoding="utf-8") as file:
                        file.write(product_data)

                except:
                    tree = ""
                    product_data = ""
                data_dict["brand"] = ""
                try:
                    brand = tree.xpath('string(//h1/div[1]/text())').replace("\n", "").replace("\t", "").strip()
                    data_dict["brand"] = brand.replace("\n", "").replace("\t", "").strip()
                    print("brand", brand)
                except:
                    data_dict["brand"] = None
                data_dict["name"] = ""
                try:
                    data_dict["name"] = tree.xpath('string(//h1/div[3]/text())').replace("\n", "").replace("\t", "").strip()
                    data_dict["name"] = data_dict["name"].split(",")[0]
                except:
                    data_dict["name"] = data_dict["name"]
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
                    data_dict["image_url"] = tree.xpath('string(//h1/parent::div/parent::div/parent::div/preceding-sibling::div//a/img/@src)')
                    print("image_url", data_dict["image_url"])
                except:
                    data_dict["image_url"] = ""
                data_dict["user_manual"] = ""
                try:
                    data_dict["user_manual"] = tree.xpath('string(//div[contains(text(), "User Manual")]/parent::a/@href | //div[contains(text(), "Use and Care")]/parent::a/@href | //div[contains(text(), "Care Manual")]/parent::a/@href | //div[contains(text(), "User Guide")]/parent::a/@href)')
                    print(data_dict["user_manual"], "UUUUUU")
                    if data_dict["user_manual"] == "":
                        data_dict["user_manual"] = tree.xpath("string(//div[contains(text(), 'Use and Care')]/parent::a/@href | //div[contains(text(), 'Manual')]/parent::a/@href | //div[contains(text(), 'Care Guide')]/parent::a/@href | //div[contains(text(), 'Use, Care, and Installation Guide')]/parent::a/@href | //div[contains(text(), 'Use and Care Guide')]/parent::a/@href)")

                    if data_dict["user_manual"] == "":
                        data_dict["user_manual"] = tree.xpath("string(//div[contains(text(), 'Owners Guide')]/parent::a/@href | //div[contains(text(), 'Owners Manual')]/parent::a/@href | //div[contains(text(), 'Owner')]/parent::a/@href)")
                    if data_dict["user_manual"] == "":
                        data_dict["user_manual"] = tree.xpath("string(//div[contains(text(), 'Installation Instructions')]/parent::a/@href | //div[contains(text(), 'User Instructions')]/parent::a/@href | //div[contains(text(), 'Installation Guide')]/parent::a/@href | //div[contains(text(), 'Install Guide')]/parent::a/@href)")
                    print(model_name, data_dict["user_manual"] ,"OOOOOOOOOOO")

                except:
                    data_dict["user_manual"] = ""
                data_dict["Warranty_Guide"] = ""
                try:
                    data_dict["Warranty_Guide"] = tree.xpath('string(//div[contains(text(), "Warranty")]/parent::a/@href)')
                    print("Warranty_Guide", model_name,data_dict["Warranty_Guide"])
                except:
                    data_dict["Warranty_Guide"] = ""
                data_dict["Energy_Guide"] = ""
                try:
                    data_dict["Energy_Guide"] = tree.xpath('string(//div[contains(text(), "Energy Guide")]/parent::a/@href)')
                    print("Energy_Guide", model_name,data_dict["Energy_Guide"]) 
                except:
                    data_dict["Energy_Guide"] = "" 
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
    else:
        return {}

# scrape_product_data_ajmadison("RF23DB9900QDAC")
# python scraper_ajmadison.py