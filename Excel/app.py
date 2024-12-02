from flask import Flask, request
from openpyxl import load_workbook

app = Flask(__name__)

# Route voor het ontvangen van formuliergegevens
@app.route('/submit', methods=['POST'])
def submit_form():
    # Ontvang gegevens van het formulier
    name = request.form.get('name')
    email = request.form.get('email')
    subject = request.form.get('subject')

    # Open het Excel-bestand
    file_path = "formdata.xlsx"  # Geef het pad naar je Excel-bestand
    wb = load_workbook(file_path)
    sheet = wb.active

    # Voeg de gegevens toe als een nieuwe rij
    sheet.append([name, email, subject])
    wb.save(file_path)

    return {"status": "success", "message": "Data opgeslagen!"}

if __name__ == '__main__':
    app.run(debug=True)
