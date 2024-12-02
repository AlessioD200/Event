from flask import Flask, request, jsonify
from openpyxl import load_workbook
import os

app = Flask(__name__)

# Route for receiving form data
@app.route('/submit', methods=['POST'])
def submit_form():
    try:
        # Get form data
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')

        # Check if form fields are not empty
        if not name or not email or not subject:
            return jsonify({"status": "error", "message": "Alle velden moeten worden ingevuld!"})

        # Open the Excel file
        file_path = "formdata.xlsx"
        if os.path.exists(file_path):
            wb = load_workbook(file_path)
        else:
            wb = load_workbook()

        sheet = wb.active

        # Append data as a new row
        sheet.append([name, email, subject])
        wb.save(file_path)

        return jsonify({"status": "success", "message": "Data opgeslagen!"})

    except Exception as e:
        return jsonify({"status": "error", "message": f"Er ging iets mis: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)
