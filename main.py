from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import pdfplumber

app = FastAPI()

# Serve static files (Frontend)
app.mount("/static", StaticFiles(directory="."), name="static")

PDF_PATH = "sd-pages.pdf"

# Extract Name & Father's Name from PDF
def extract_student_data():
    students = []
    with pdfplumber.open(PDF_PATH) as pdf:
        for page in pdf.pages:
            table = page.extract_table()
            if table:
                headers = ["S.No", "Name", "Student Mobile", "Father Name"]
                for row in table[1:]:  # Skip headers
                    students.append({"Name": row[1], "Father Name": row[3]})
    return students

STUDENT_DATA = extract_student_data()

@app.get("/")
async def serve_frontend():
    """ Serve index.html when visiting the root URL """
    return FileResponse("index.html")

@app.get("/user/{name}")
async def get_user(name: str):
    """ Search for a student by Name """
    for student in STUDENT_DATA:
        if student["Name"].lower() == name.lower():
            return {
                "name": student["Name"],
                "father_name": student["Father Name"]
            }
    raise HTTPException(status_code=404, detail="User not found")
