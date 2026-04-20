from flask import Flask, render_template, request, send_file
import pytesseract
from PIL import Image
from openpyxl import Workbook
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def extract_text(image_path):
    return pytesseract.image_to_string(Image.open(image_path), lang='eng')

def create_excel(text):
    file = "result.xlsx"
    wb = Workbook()
    ws = wb.active

    ws.append(["Raw Text"])
    for line in text.split("\n"):
        ws.append([line])

    wb.save(file)
    return file

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["file"]
        path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(path)

        text = extract_text(path)
        excel_file = create_excel(text)

        return send_file(excel_file, as_attachment=True)

    return render_template("index.html")

if __name__ == "__main__":
    app.run()