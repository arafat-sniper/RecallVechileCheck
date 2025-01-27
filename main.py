import csv
import os
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

data_file = 'sample_data.csv'

# Create the CSV file with headers if it doesn't exist
if not os.path.exists(data_file):
    with open(data_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Chassis Number', 'Contact Number', 'Dealership Name'])

# Serve the main page
@app.route('/')
def index():
    return render_template('index.html')

# Lookup VIN number
@app.route('/lookup', methods=['GET'])
def lookup_vin():
    vin = request.args.get('vin')
    with open(data_file, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header row
        for row in reader:
            if row[0] == vin:
                return jsonify({
                    'status': 'success', 
                    'message': 'Match found! Kindly enter the customer contact number and your dealership name.'
                })
    return jsonify({'status': 'error', 'message': 'No match found'})

# Submit contact number and dealership name
@app.route('/submitDetails', methods=['POST'])
def submit_details():
    details = request.get_json()
    vin = details.get('vin')
    contact_number = details.get('contactNumber')
    dealership_name = details.get('dealershipName')

    # Update the CSV file with the contact and dealership details
    updated_rows = []
    with open(data_file, 'r', newline='') as f:
        reader = csv.reader(f)
        headers = next(reader)
        updated_rows.append(headers)

        for row in reader:
            if row[0] == vin:
                row[1] = contact_number
                row[2] = dealership_name
            updated_rows.append(row)

    with open(data_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(updated_rows)

    return jsonify({'status': 'success', 'message': 'Thank you for submitting your details! Your information has been saved.'})

# Serve the CSV file for download
@app.route('/downloadData', methods=['GET'])
def download_data():
    if os.path.exists(data_file):
        return app.send_static_file(data_file)
    else:
        return jsonify({'status': 'error', 'message': 'No data available for download'})

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=3000)
