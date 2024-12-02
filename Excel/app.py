from flask import Flask, request, jsonify
from openpyxl import Workbook, load_workbook
import os
from flask_cors import CORS  # Import CORS

app = Flask(__name__)

# Enable CORS for all routes (you can restrict this to certain origins if needed)
CORS(app)

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

        # Define the file path
        file_path = "Excel/formdata.xlsx"
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Open or create the Excel file
        if os.path.exists(file_path):
            wb = load_workbook(file_path)
        else:
            wb = Workbook()
            sheet = wb.active
            # Add headers for a new workbook
            sheet.append(["Name", "Email", "Subject"])

        # Get the active sheet
        sheet = wb.active

        # Append data as a new row
        sheet.append([name, email, subject])
        wb.save(file_path)

        return jsonify({"status": "success", "message": "Data opgeslagen!"})

    except Exception as e:
        # Log the error for debugging
        return jsonify({"status": "error", "message": f"Er ging iets mis: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)
