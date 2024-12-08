from flask import Flask, request, jsonify
from openpyxl import Workbook, load_workbook
import os
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
CORS(app)

# Route for receiving form data
@app.route('/submit', methods=['POST'])
def submit_form():
    try:
        # Get form data
        name = request.form.get('name')
        email = request.form.get('email')
        voertuigen = request.form.get('voertuigen')
        personen = request.form.get('personen')
        adres = request.form.get('adres')
        gsm = request.form.get('gsm')
        merk_voertuig = request.form.get('merk_voertuig')
        nr_plaat = request.form.get('nr_plaat')

        # Check required fields
        if not name or not email or not personen or not nr_plaat:
            return jsonify({"status": "error", "message": "Alle velden moeten worden ingevuld!"})

        # Define file path
        file_path = "Excel/formdata.xlsx"
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Open or create Excel file
        if os.path.exists(file_path):
            wb = load_workbook(file_path)
        else:
            wb = Workbook()
            sheet = wb.active
            # Add headers for a new workbook
            sheet.append(["Name", "Email", "Voertuigen", "Personen", "Adres", "GSM", "Merk voertuig", "Nummerplaat"])

        # Get active sheet
        sheet = wb.active

        # Append data as new row
        sheet.append([name, email, voertuigen, personen, adres, gsm, merk_voertuig, nr_plaat])
        wb.save(file_path)

        # Success response
        return jsonify({"status": "success", "message": "Data succesvol opgeslagen!"})

    except Exception as e:
        # Error response
        return jsonify({"status": "error", "message": f"Er is iets fout gegaan: {str(e)}"})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)