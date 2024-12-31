import os
import re
import pandas as pd
from flask import Flask, render_template, request, jsonify
from scraper_ajmadison import scrape_product_data_ajmadison
from scraper_homedepot import scrape_product_data_homedepot
from scraper_support_frigidaire import scrape_product_support_frigidaire
from scraper_products_geappliances import scrape_product_data_geappliances

app = Flask(__name__)

# add error handling and logging
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'xls', 'xlsx'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route to render the frontend HTML
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle the file upload
@app.route('/upload', methods=['POST'])
def upload_file():
    print("request  ", request)
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    sheet_name = request.form.get('sheet_name')
    domain_name = request.form.get('domain_name')
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file and allowed_file(file.filename):
        # Save the file
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        
        try:
            xl = pd.ExcelFile(filename)
            
            # Check if sheet name exists
            if sheet_name and sheet_name not in xl.sheet_names:
                return jsonify({"error": f"Sheet '{sheet_name}' not found. Available sheets: {', '.join(xl.sheet_names)}"}), 400
            
            # If sheet_name is provided, use it; otherwise, use the first sheet by default
            if sheet_name:
                df = xl.parse(sheet_name)
            else:
                df = xl.parse(0)  # First sheet by default
            
            # Select only the "Model Name" column
            if 'Model Name' not in df.columns:
                return jsonify({"error": "Column 'Model Name' not found in the sheet"}), 400

            # Extract only the "Model Name" column and remove duplicates
            model_names = df['Model Name'].dropna().drop_duplicates().tolist()  # Drop NaN and duplicates, then convert to list
            results = []
            if "www.ajmadison.com" == domain_name:
                file_number = 1
                for model_name in model_names[:]:
                    model_name = str(model_name)
                    
                    scraped_data = scrape_product_data_ajmadison(model_name)
                    if scraped_data:
                        results.append(scraped_data)
                        # break
                        if not os.path.exists(f'{sheet_name}_{domain_name}_file'):
                            os.makedirs(f'{sheet_name}_{domain_name}_file')
                        output_directory = os.path.join(os.getcwd(), f'{sheet_name}_{domain_name}_file')

                        if not os.path.exists(output_directory):
                            os.makedirs(output_directory)
                        output_data = os.path.join(output_directory, f"{file_number}_{sheet_name}_output_{domain_name}_data_all.xlsx")
                        df = pd.DataFrame(results)
                        df.to_excel(output_data, index=False)
                        if len(results) == 100:
                            file_number += 1
                            results = []
                return jsonify({"all data": "successfully scrapped"}), 400
            if "www.homedepot.com" == domain_name:
                for model_name in model_names[:]:
                    model_name = str(model_name)
                    scraped_data = scrape_product_data_homedepot(model_name)
                    if scraped_data:
                        results.append(scraped_data)
                        # break
                        if not os.path.exists(f'All_product_{domain_name}_file'):
                            os.makedirs(f'All_product_{domain_name}_file')
                        output_directory = os.path.join(os.getcwd(), f'All_product_{domain_name}_file')

                        if not os.path.exists(output_directory):
                            os.makedirs(output_directory)
                        output_data = os.path.join(output_directory, f"output_{domain_name}_data_all.xlsx")
                        df = pd.DataFrame(results)
                        df.to_excel(output_data, index=False)
                return jsonify({"all data": "successfully scrapped"}), 400
            print(results)
            if "products.geappliances.com" == domain_name:
                for model_name in model_names[:]:
                    model_name = str(model_name)
                    # model_name = "R BS330DR3WW"
                    scraped_data = scrape_product_data_geappliances(model_name)
                    if scraped_data:
                        results.append(scraped_data)
                        # break
                        if not os.path.exists(f'All_product_{domain_name}_file'):
                            os.makedirs(f'All_product_{domain_name}_file')
                        output_directory = os.path.join(os.getcwd(), f'All_product_{domain_name}_file')

                        if not os.path.exists(output_directory):
                            os.makedirs(output_directory)
                        output_data = os.path.join(output_directory, f"output_{domain_name}_data_all.xlsx")
                        df = pd.DataFrame(results)
                        df.to_excel(output_data, index=False)
                return jsonify({"all data": "successfully scrapped"}), 400
            print(results)
            if "www.frigidaire.ca" == domain_name:
                for model_name in model_names[:]:
                    model_name = str(model_name)
                    
                    scraped_data = scrape_product_support_frigidaire(model_name)
                    if scraped_data:
                        results.append(scraped_data)
                        # break
                        if not os.path.exists(f'All_product_{domain_name}_file'):
                            os.makedirs(f'All_product_{domain_name}_file')
                        output_directory = os.path.join(os.getcwd(), f'All_product_{domain_name}_file')
                        if not os.path.exists(output_directory):
                            os.makedirs(output_directory)
                        output_data = os.path.join(output_directory, f"output_{domain_name}_data_all.xlsx")
                        df = pd.DataFrame(results)
                        df.to_excel(output_data, index=False)
                return jsonify({"all data": "successfully scrapped"}), 400
            print(results)
        except Exception as e:
            return jsonify({"error": f"Error reading the Excel file: {str(e)}"}), 500
    
    return jsonify({"error": "Invalid file type"}), 400

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    
    app.run(debug=True)
