# Get product details

## Overview

This script is designed to search with websites for model number of products on user input, and then generate a CSV file containing the model details as image, source url, model name, catagory, name, usermanual, energy guide, warranty guide. The project  is split into two parts.

Frontend : Calls and runs app.py file.
backend: will call by frontend buttons.

## Features
    1. Search for model number based on a query and get url of products.
    2. with using url of product we will get product details
    3. Output details in a CSV format for easy extraction.

## Requirements
we want to also use oxylab proxies for google search and product web site search.
we have Requirements.txt file for install dependencies
Before running the script, ensure you have the following installed
run command for install dependencies   `requirments.txt`

Example command

    ```python
    pip install -r requirements.txt
    ```

## File Structure

    ```bash
    your_script_directory
    │
    ├── app.py          # Main file which executes the program
    ├── scraper_ajmadison.py      # Helper functions for ajmadison site model data
    ├── scraper_homedepot.py      # Helper functions for homedepot site model data
    ├── scraper_products_geappliances.py      # Helper functions for ge appliances site model data
    ├── scraper_support_frigidaire.py      # Helper functions for frigidaire site model data
    ├── www_samsung_us_com.py      # Helper functions for samsung.us  site model data
    ├── output_folder              # Output CSV file containing Lmodel details
    ├── input.csv              # we can select by frontend
    ├── README.md               # for details
    ├── command.txt            # all command one by one for run project
    ├── requirements.txt      # easy to install dependencies
    ```

## How to Use

Clone or Download the Repository from this github url  `url_path`

Run the app.py file to start the process. This file will

Call frontend index.html  from template folder.
on frontend you want fill all details input csv file, sheet name , domain name and click on button scraper. 
project will start scraping model details and store extracted data in csv formate

Example command

    ```python
    python app.py
    ```


How It Works
Main Script (`app.py`)

The app file handles user input, calls the functions from the helper script.

Helper Script (`www_samsung_us_com.py`)

that will scrap samsung websites us  model details 

Helper Script (`scraper_support_frigidaire.py`)

that will scrap  frigidaire  model details

Helper Script (`scraper_products_geappliances.py`)

that will scrap  geappliances  model details

Helper Script (`scraper_homedepot.py`)

that will scrap homedepot model details

Helper Script (`scraper_ajmadison.py`)

that will scrap ajmadison model details
