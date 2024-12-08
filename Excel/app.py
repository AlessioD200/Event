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
        return f"Data ontvangen: {name}, {email}, {voertuigen}, {personen}, {adres}, {gsm}, {merk_voertuig}, {nr_plaat}"
        print(request.form)
        return "Formulier succesvol verzonden!"
        
        # Check if required fields are filled
        if not name or not email or not personen or not nr_plaat:
            return jsonify({"status": "error", "message": "Alle velden moeten worden ingevuld!"})

        # Define file path
        file_path = "Excel/formdata.xlsx"
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Open or create the Excel file
        if os.path.exists(file_path):
            wb = load_workbook(file_path)
        else:
            wb = Workbook()
            sheet = wb.active
            # Add headers for a new workbook
            sheet.append(["Name", "Email", "Voertuigen", "Personen", "Adres", "GSM", "Merk van voertuig", "Nummerplaat"])

        # Get the active sheet
        sheet = wb.active

        # Append data as a new row
        sheet.append([name, email, voertuigen, personen, adres, gsm, merk_voertuig, nr_plaat])
        wb.save(file_path)

        return jsonify({"status": "success", "message": "Data opgeslagen!"})

    except Exception as e:
        return jsonify({"status": "error", "message": f"Er ging iets mis: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)