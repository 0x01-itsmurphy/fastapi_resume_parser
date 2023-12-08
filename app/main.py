import spacy
from io import BytesIO
from fastapi import FastAPI, File, UploadFile
from pdfminer.high_level import extract_text
from pypdf import PdfReader
from spacy.matcher import Matcher
from mangum import Mangum

from . import utils as utl

app = FastAPI()

nlp = spacy.load("en_core_web_sm")
matcher = Matcher(nlp.vocab)


@app.get("/")
async def root():
    return {"status": 200, "data": "hello parser"}


@app.post("/parse_resume", description="Not working properly")
async def parse_resume(file: UploadFile = File(...)):
    # Download and read the PDF file
    contents = await file.read()
    pdf_reader = PdfReader(BytesIO(contents))
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()

    # Process the plain text using spaCy
    doc = nlp(text)
    print(doc)
    extracted_text = {}

    email = utl.get_email(text)
    phone_number = utl.get_phone(text)
    name_ext = utl.extract_name(text)
    skills = utl.extract_skills_new(text)
    edu = utl.extract_education(text)

    name = None
    # email = None
    experience = None
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            name = ent.text
        elif ent.label_ == "EXPERIENCE":
            experience = ent.text

    # Return the extracted information in a JSON response
    return {
        "name": name_ext,
        "email": email,
        'phone': phone_number,
        'skills': skills,
        'education': edu,
        'experience': experience,
    }


@app.post("/parse", description="Working")
async def parse(file: UploadFile):
    # Download and read the PDF file
    contents = await file.read()
    pdf_reader = PdfReader(BytesIO(contents))
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()

    # data = ResumeParser(text).get_extracted_data()

    data = extract_text(file.file)
    print(data)

    # Process the plain text using spaCy
    doc = nlp(text)

    name = utl.extract_name(data)
    email = utl.get_email(data)
    phone = utl.get_phone(data)
    linkedIn = utl.linkedin(data)
    github = utl.extract_github(data)
    others_urls = utl.extract_urls(data)
    skills = utl.extract_skills_new(data)
    experience = None
    course_name = utl.extract_course_name(data)
    specializations = utl.extract_specializations(data)
    college = utl.get_college(data)
    languages = utl.get_language(data)
    location = utl.get_location(data)
    # address = utl.extract_address(data) // Not Wprking
    extracted_zip = utl.extract_zip_code(data)

    return {
        "name": name,
        "email": email,
        "phone_number": phone,
        "social_links": {
            "linkedIn": linkedIn,
            "github": github,
            "others": others_urls,
        },
        "skills": skills,
        "education_details": {
            "courses": course_name,
            "specializations ": specializations,
            "college": college,
        },
        "address": {"location": location, "zip_code": extracted_zip},
        "languages": languages,
        "raw_data": data,
    }


handler = Mangum(app)
