from flask import Flask, request, jsonify, render_template
import pandas as pd
from openpyxl import load_workbook

app = Flask(__name__)

# Path to your Excel file
EXCEL_FILE = '\Alessio\Documents\GitHub\Event\Excel\data.xlsx'

@app.route('/')
def index():
    # Render the form
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_form():
    try:
        # Extract form data
        form_data = {
            'Naam/Voornaam': request.form['name'],
            'Email': request.form['email'],
            'Personen': request.form['personen'],
            'Adres': request.form['adres'],
            'GSM': request.form['gsm'],
            'Voertuigen': request.form['voertuigen'],
            'Merk voertuig': request.form['merk_voertuig'],
            'Nummerplaat': request.form['nr_plaat'],
        }

        # Load existing data from the Excel file or create a new DataFrame
        try:
            df = pd.read_excel(EXCEL_FILE)
        except FileNotFoundError:
            # Create an empty DataFrame with appropriate columns
            df = pd.DataFrame(columns=form_data.keys())

        # Append the new form data
        df = df.append(form_data, ignore_index=True)

        # Save back to Excel
        df.to_excel(EXCEL_FILE, index=False)

        # Adjust column widths using openpyxl
        adjust_column_width(EXCEL_FILE, df.columns)

        return jsonify({'status': 'success', 'message': 'Data successfully saved!'})

    except Exception as e:
        # Handle errors and return a failure response
        return jsonify({'status': 'error', 'message': str(e)}), 500

def adjust_column_width(file_path, columns):
    """Adjusts the width of the columns in the Excel file."""
    workbook = load_workbook(file_path)
    sheet = workbook.active

    for col_index, col_name in enumerate(columns, start=1):
        col_letter = chr(64 + col_index)  # Convert column index to Excel letter (1 -> A, 2 -> B, etc.)
        sheet.column_dimensions[col_letter].width = max(20, len(col_name) + 5)  # Adjust width as needed

    workbook.save(file_path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
