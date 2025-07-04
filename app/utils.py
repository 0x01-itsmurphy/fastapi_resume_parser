import csv
import re
import locationtagger
import pandas as pd
import spacy
import logging
from typing import List, Dict, Optional, Set, Union

from geopy.geocoders import Nominatim
from nltk.corpus import stopwords
from spacy.matcher import Matcher
from urlextract import URLExtract

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load spaCy model with error handling
try:
    nlp = spacy.load("en_core_web_sm")
    matcher = Matcher(nlp.vocab)
    logger.info("spaCy model loaded successfully in utils")
except Exception as e:
    logger.error(f"Failed to load spaCy model in utils: {e}")
    nlp = None
    matcher = None


def extract_name(resume_text: str) -> Optional[str]:
    """Extract name from resume text using spaCy NLP"""
    if not nlp:
        logger.error("spaCy model not loaded")
        return None
    
    try:
        nlp_text = nlp(resume_text)
        
        # First name and Last name are always Proper Nouns
        pattern = [{'POS': 'PROPN'}, {'POS': 'PROPN'}]
        
        matcher.add('NAME', [pattern], on_match=None)
        matches = matcher(nlp_text)
        
        for match_id, start, end in matches:
            span = nlp_text[start:end]
            return span.text
        
        # Fallback: look for PERSON entities
        for ent in nlp_text.ents:
            if ent.label_ == "PERSON":
                return ent.text
        
        return None
    except Exception as e:
        logger.error(f"Error extracting name: {e}")
        return None


def get_email(txt: str) -> Set[str]:
    """Extract email addresses from text"""
    try:
        EMAIL_REG = re.compile(r'[a-zA-Z_0-9\.\-+]+@[a-z0-9\.\-+]+\.[a-z]+')
        email = re.findall(EMAIL_REG, txt)
        return set(email)
    except Exception as e:
        logger.error(f"Error extracting email: {e}")
        return set()


def get_phone(txt: str) -> Optional[str]:
    """Extract phone number from text"""
    try:
        PHONE_REG = re.compile(r'[\+\(]?[1-9][0-9.\-\(\)]{8,}[0-9]')
        phone = re.findall(PHONE_REG, txt)
        
        if phone:
            number = ''.join(phone[0])
            if txt.find(number) >= 0 and len(number) <= 16:
                return number
        return None
    except Exception as e:
        logger.error(f"Error extracting phone: {e}")
        return None


def linkedin(text: str) -> str:
    """Extract LinkedIn profile URL from text"""
    try:
        pat = re.compile(
            r"((?:(?:[\w]+\.)?linkedin\.com\/(?:pub|in|profile)\/(?:[-a-zA-Z0-9]+)\/*))"
        )
        matches = pat.findall(text)
        
        if len(matches) == 0:
            return ""
        return matches[0]  # Return the first occurrence
    except Exception as e:
        logger.error(f"Error extracting LinkedIn: {e}")
        return ""


def extract_github(text: str) -> str:
    """Extract GitHub username from text"""
    try:
        pat = re.compile(r"(?:http[s]?://)?github\.com/([^\s^/]+)")
        matches = pat.findall(text)
        
        if len(matches) == 0:
            return ""
        return matches[0]  # Return the first occurrence
    except Exception as e:
        logger.error(f"Error extracting GitHub: {e}")
        return ""


def extract_urls(text: str) -> List[str]:
    """Extract URLs from text"""
    try:
        extractor = URLExtract()
        urls = extractor.find_urls(text)
        return urls
    except Exception as e:
        logger.error(f"Error extracting URLs: {e}")
        return []


def get_skills(txt: str) -> list[str]:
    nlp_text = nlp(txt)

    # removing stop words and implementing word tokenization
    tokens = [token.text for token in nlp_text if not token.is_stop]

    # reading the csv file
    data = pd.read_csv("./app/assets/skills.csv")

    # extract values
    skills = list(data.columns.values)

    skillset = []

    # check for one-grams (example: python)
    for token in tokens:
        if token.lower() in skills:
            skillset.append(token)

    # check for bi-grams and tri-grams (example: machine learning)
    for token in nlp_text.noun_chunks:
        token = token.text.lower().strip()
        if token in skills:
            skillset.append(token)

    return [i.capitalize() for i in set([i.lower() for i in skillset])]


def extract_skills_new(resume_text: str) -> List[str]:
    """Extract skills from resume text using an improved skill matching algorithm"""
    if not nlp:
        logger.error("spaCy model not loaded")
        return []
    
    try:
        nlp_text = nlp(resume_text.lower())
        
        # removing stop words and implementing word tokenization
        tokens = [token.text for token in nlp_text if not token.is_stop]
        
        # Comprehensive skills list
        skills = [
            # Programming Languages
            "python", "java", "javascript", "typescript", "c++", "c#", "c", "php", "ruby", "go", "rust", "swift", "kotlin",
            "scala", "r", "matlab", "sql", "html", "css", "xml", "json", "yaml", "shell", "bash", "powershell",
            
            # Frameworks and Libraries
            "react", "vue.js", "angular", "node.js", "express", "django", "flask", "spring", "laravel", "rails",
            "jquery", "bootstrap", "tailwind css", "sass", "less", "webpack", "babel", "electron", "react native",
            "flutter", "dart", "xamarin", "ionic", "cordova", "phonegap", "unity", "unreal engine",
            
            # Databases
            "mysql", "postgresql", "mongodb", "redis", "cassandra", "dynamodb", "oracle", "sql server", "sqlite",
            "elasticsearch", "neo4j", "couchdb", "firebase", "mariadb", "nosql", "database management",
            
            # Cloud and DevOps
            "aws", "azure", "google cloud", "gcp", "docker", "kubernetes", "jenkins", "terraform", "ansible",
            "puppet", "chef", "vagrant", "git", "github", "gitlab", "bitbucket", "ci/cd", "devops", "linux",
            "ubuntu", "centos", "redhat", "debian", "nginx", "apache", "tomcat", "microservices", "serverless",
            
            # Data Science and ML
            "machine learning", "deep learning", "neural networks", "convolutional neural networks", "cnn",
            "recurrent neural networks", "rnn", "natural language processing", "nlp", "computer vision",
            "image processing", "object detection", "object recognition", "tensorflow", "pytorch", "scikit-learn",
            "pandas", "numpy", "matplotlib", "seaborn", "plotly", "jupyter", "anaconda", "tableau", "power bi",
            "data analysis", "data visualization", "statistics", "statistical analysis", "regression", "clustering",
            "classification", "recommendation systems", "time series analysis", "big data", "hadoop", "spark", "kafka",
            
            # Mobile Development
            "ios", "android", "mobile development", "app development", "swift", "objective-c", "kotlin", "java",
            "react native", "flutter", "xamarin", "ionic", "cordova", "phonegap",
            
            # Web Development
            "web development", "frontend", "backend", "full stack", "responsive design", "ui/ux", "figma",
            "sketch", "adobe xd", "photoshop", "illustrator", "wireframing", "prototyping",
            
            # Project Management
            "project management", "agile", "scrum", "kanban", "waterfall", "jira", "trello", "asana",
            "confluence", "slack", "teams", "zoom", "leadership", "team management", "communication",
            "problem-solving", "critical thinking", "creativity", "analytical thinking",
            
            # Security
            "cybersecurity", "information security", "network security", "encryption", "authentication",
            "authorization", "penetration testing", "vulnerability assessment", "security auditing",
            
            # Quality Assurance
            "testing", "unit testing", "integration testing", "automated testing", "selenium", "cypress",
            "jest", "mocha", "chai", "junit", "testng", "quality assurance", "qa", "bug tracking",
            
            # Office Tools
            "excel", "word", "powerpoint", "outlook", "google docs", "google sheets", "google slides",
            "office 365", "sharepoint", "onenote", "visio", "project"
        ]
        
        # create a set of lowercase skills for comparison
        lowercase_skills = set([skill.lower() for skill in skills])
        
        skillset = []
        
        # check for one-grams (example: python)
        for token in tokens:
            if token in lowercase_skills:
                skillset.append(token)
        
        # check for bi-grams and tri-grams (example: machine learning)
        for i in range(len(tokens) - 1):
            bigram = f"{tokens[i]} {tokens[i + 1]}"
            if bigram in lowercase_skills:
                skillset.append(bigram)
        
        for i in range(len(tokens) - 2):
            trigram = f"{tokens[i]} {tokens[i + 1]} {tokens[i + 2]}"
            if trigram in lowercase_skills:
                skillset.append(trigram)
        
        # Return capitalized unique skills
        return [skill.title() for skill in set(skillset)]
    
    except Exception as e:
        logger.error(f"Error extracting skills: {e}")
        return []


# def extract_education_details(text: str):
#     # Define a list of degrees and their variations
#     degrees = ["B\.A\.", "B\.S\.", "B\.Sc\.", "M\.A\.", "M\.S\.", "M\.Sc\.",
#                "Ph\.D\.", "M\.B\.A\.", "B\.E\.", "M\.E\.", "B\.Tech\.", "M\.Tech\.", "Bachelor of Technology",]

#     # Define a regex pattern for degrees and university names
#     degree_pattern = "|".join(degrees)
#     university_pattern = r"[A-Za-z\s]+University"

#     # Find matches in the text
#     degree_matches = re.findall(degree_pattern, text)
#     university_matches = re.findall(university_pattern, text)

#     # Combine and return the results
#     return university_matches

def extract_course_name(text: str):
    # Define a list of degrees and their variations
    degrees = ["B\.A\.", "B\.S\.", "B\.Sc\.", "M\.A\.", "M\.S\.", "M\.Sc\.", "Ph\.D\.",
               "M\.B\.A\.", "B\.E\.", "M\.E\.", "B\.Tech\.", "M\.Tech\.",
               "B\.Com\.", "M\.Com\.",
               'SSC', 'HSC', 'CBSE', 'ICSE'
               r"[^a-zA-Z\d] Board",
               r"Bachelor of Technology(?: in [\w\s]+)?",
               r"Master of Technology(?: in [\w\s]+)?",
               r"Bachelor of Science(?: in [\w\s]+)?",
               r"Master of Science(?: in [\w\s]+)?",
               r"Bachelor of Arts(?: in [\w\s]+)?",
               r"Master of Arts(?: in [\w\s]+)?",
               r"Doctor of Philosophy(?: in [\w\s]+)?",
               r"Bachelor of Commerce(?: in [\w\s]+)?",
               r"Master of Commerce(?: in [\w\s]+)?",
               r"Bachelor of Engineering(?: in [\w\s]+)?",
               r"Master of Engineering(?: in [\w\s]+)?",
               r"Associate of Arts(?: in [\w\s]+)?",
               r"Associate of Science(?: in [\w\s]+)?",
               r"Associate of Applied Science(?: in [\w\s]+)?",
               r"Juris Doctor(?: in [\w\s]+)?",
               "J\.D\."
               "Diploma",
               r"Diploma(?: in [\w\s]+)?",
               r"Postgraduate Diploma(?: in [\w\s]+)?",
               r"Graduate Diploma(?: in [\w\s]+)?",
               r"Advanced Diploma(?: in [\w\s]+)?",
               ]

    degree_pattern = re.compile("|".join(degrees), re.IGNORECASE)
    matches = degree_pattern.findall(text)

    degree_list = []
    for match in matches:
        degree_list.append(match)

    return degree_list


def extract_specializations(resume_text):

    # specializations = [
    #     "Computer Science",
    #     "Computer Engineering",
    #     "Civil Engineering",
    #     "Electrical Engineering",
    #     "Mechanical Engineering",
    #     "Chemical Engineering",
    #     "Aerospace Engineering",
    #     "Industrial Engineering",
    #     "Material Engineering",
    #     "Biomedical Engineering",
    #     "Environmental Engineering",
    #     "Software Engineering"
    # ]

    specializations = []

    with open("app/assets/spe.csv", "r") as csvfile:
        csvreader = csv.reader(csvfile)
        header = next(csvreader)
        for row in csvreader:
            specializations.append(row[1])

    found_specializations = []

    for specialization in specializations:
        if re.search(specialization, resume_text, re.IGNORECASE):
            found_specializations.append(specialization)

    return found_specializations


def get_college(txt):
    RESERVED_WORDS = [
        'school',
        'college',
        'univers',
        'academy',
        'faculty',
        'institute',
        'faculdades',
        'Schola',
        'schule',
        'lise',
        'lyceum',
        'lycee',
        'polytechnic',
        'kolej',
        'ünivers',
        'okul',
    ]
    RESERVED_WORDS = [m.capitalize() for m in RESERVED_WORDS]+[m.upper()
                                                               for m in RESERVED_WORDS]+RESERVED_WORDS
    line = txt.split('\n')
    edu = []
    for i in line:
        for j in RESERVED_WORDS:
            if j in i:
                edu.append(i)

    return edu


def get_language(txt):
    lang = ['English', 'Marathi', 'Telugu', 'Hindi', 'Malayalam', 'Kannada',
            'Tamil', 'Spanish', 'French', 'Urdu', 'Bengalis', 'Punjabi', 'Gujarati']
    lang = [m.capitalize() for m in lang] + [m.lower() for m in lang] + lang
    lines = txt.split('\n')
    detected_languages = []

    for line in lines:
        for language in lang:
            if language in line:
                detected_languages.append(language)

    if len(detected_languages) > 0:
        return list(set(detected_languages))
    else:
        return None


def contains_integer(s):
    return bool(re.search(r'\d', s))


def check_list(lst):
    if len(lst) >= 2 and contains_integer(lst[-2]):
        print(lst[-2])
    else:
        print("No integer found in second last string")


def get_location(txt):
    place = locationtagger.find_locations(text=txt)
    # doc = nlp(txt)

    # locations = [ent.text for ent in doc.ents if ent.label_ == "GPE"]
    cities = place.cities

    # Define the city
    city = cities[0]
    geolocator = Nominatim(user_agent="geoapiExercises")

    # Perform a geocode lookup for the city
    location = geolocator.geocode(city, language="en")
    print(location)
    if location:
        address = location.address.split(', ')
        print("ADD")
        print(address)

        state = None
        country = None
        zip_code = None

        if len(address) > 0:
            last_element = address[-1]
            country = last_element
        else:
            last_element = None

        if len(address) >= 1 and contains_integer(address[-2]):
            last_second_element = address[-2]
            zip_code = last_second_element
        else:
            print("No integer found in second last string")
            last_second_element = None

        if len(address) > 2:
            last_third_element = address[-3]
            state = last_third_element
        else:
            last_third_element = None

        return {
            "formatted": None,
            "streetNumber": None,
            "street": None,
            "apartmentNumber": None,
            "city": city,
            "postalCode": zip_code,
            "state": state,
            "country": country,
            # "raw": location,
        }
    else:
        return None


def extract_address(resume_text):
    # Regex pattern for city, state, and zip code
    pattern = r'([A-Za-z]+(?:[ -][A-Za-z]+)*),\s*([A-Za-z]{2})\s*(\d{5}(?:-\d{4})?)?'

    # Find all matches in the resume text
    matches = re.finditer(pattern, resume_text)

    # Extract the addresses
    addresses = [match.group(0) for match in matches]

    return addresses


def extract_zip_code(resume_text):
    # Use regex to extract zip code
    zip_code_pattern = r"\b(?:\d{5}(?:-\d{4})?|\d{6})\b"
    zip_codes = re.findall(zip_code_pattern, resume_text)

    return zip_codes

# def extract_addresses(text):
#     # Regex pattern for city, state, and zip code
#     pattern = r'([A-Za-z]+(?:[ -][A-Za-z]+)*),\s*([A-Za-z]{2})\s*(\d{5}(?:-\d{4})?)?'

#     # Find all matches in the text
#     matches = re.finditer(pattern, text)

#     # Extract the addresses
#     addresses = [match.group(0) for match in matches]

#     # Use Named Entity Recognition (NER) to extract additional addresses
#     doc = nlp(text)
#     for ent in doc.ents:
#         if ent.label_ == "GPE":
#             addresses.append(ent.text)

#     return addresses


def extract_education(resume_text):
    nlp_text = nlp(resume_text)

    # Sentence Tokenizer
    nlp_text = [sent.text.strip() for sent in nlp_text.sents]

    # Grad all general stop words
    STOPWORDS = set(stopwords.words('english'))

    # Education Degrees
    EDUCATION = [
        'BE', 'B.E.', 'B.E', 'BS', 'B.S',
        'ME', 'M.E', 'M.E.', 'MS', 'M.S',
        'BTECH', 'B.TECH', 'Bachelor of Technology', 'M.TECH', 'MTECH',
        'SSC', 'HSC', 'CBSE', 'ICSE', 'X', 'XII'
    ]

    edu = {}
    # Extract education degree
    for index, text in enumerate(nlp_text):
        for tex in text.split():
            # Replace all special symbols
            tex = re.sub(r'[?|$|.|!|,]', r'', tex)
            if tex.upper() in EDUCATION and tex not in STOPWORDS:
                edu[tex] = text + nlp_text[index + 1]

    education = []
    for key in edu.keys():
        year = re.search(re.compile(r'(((20|19)(\d{2})))'), edu[key])
        if year:
            education.append((key, ''.join(year[0])))
        else:
            education.append(key)
    return education
