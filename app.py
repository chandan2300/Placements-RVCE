from flask import Flask, url_for, request, session, g
from flask.templating import render_template
from werkzeug.utils import redirect
from database import get_database
from werkzeug.security import generate_password_hash, check_password_hash
import json
from datetime import datetime
import yfinance as yf
import smtplib, ssl
import os
import pandas as pd
import sqlite3
from flask_pymongo import PyMongo
from pymongo import MongoClient
from transformers import pipeline

# Jobs, Resume Analysis
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import docx2txt
import os
from wtforms.validators import InputRequired
from os.path import join, dirname, realpath
import pandas as pd
from collections import defaultdict
from matplotlib import pyplot as plt
from pandas import json_normalize 
from collections import Counter
import docx2txt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from io import BytesIO
import random
import string
import urllib
import base64

import nltk
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('maxent_ne_chunker')
# nltk.download('words')
import seaborn as sns

from pdfminer.high_level import extract_text
import nltk
import re
# nltk.download('stopwords')

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['UPLOAD_FOLDER'] = join(dirname(realpath(__file__)), 'static/uploads/..')
#client = MongoClient("mongodb+srv://placement_stats:rvce1234@cluster0.vu9p3fh.mongodb.net/placement?retryWrites=true&w=majority",tls=True,tlsAllowInvalidCertificates=True)
client = MongoClient("mongodb://localhost:27017/placement")
mongo_db = client.get_database()
test = mongo_db.test
nlp = pipeline("sentiment-analysis")

@app.teardown_appcontext
def close_database(error):
    if hasattr(g, 'crudapplication_db'):
        g.crudapplication_db.close()

def get_current_user(): 
    user = None
    if 'user' in session:
        user = session['user']
        db = get_database()
        user_cur = db.execute('select * from coordinator where email = ?', [user])
        user = user_cur.fetchone() 
    return user

# Wavy Login
@app.route('/wavy')
def wavy():
    return render_template('wavy-login.html')



@app.route('/')
def index():
    user = get_current_user()
    return render_template('index.html', user = user)

@app.route('/a')
def indexa():
    user = get_current_user()
    return render_template('a.html', user = user)

@app.route('/b')
def indexb():
    user = get_current_user()
    return render_template('index.html', user = user)

# @app.route('/login', methods = ["POST", "GET"])
# def login():
#     user = get_current_user()
#     error = None
#     db = get_database()
#     if request.method == 'POST':
#         name = request.form['name']
#         password = request.form['password']
#         user_cursor = db.execute('select * from users where name = ?', [name])
#         user = user_cursor.fetchone()
#         if user:
#             if check_password_hash(user['password'], password):
#                 session['user'] = user['name']
#                 return redirect(url_for('dashboard'))
#             else:
#                 error = "Username or Password did not match, Try again."
#         else:
#             error = 'Username or password did not match, Try again.'
#     return render_template('login.html', loginerror = error, user = user)

@app.route('/login', methods = ["POST", "GET"])
def login():
    user = get_current_user()
    error = None
    db = get_database()
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if not email or not password:
                return render_template('login2index.html', loginerror = "Enter all details", user = user)
        user_cursor = db.execute('select * from coordinator where email = ?', [email])
        user1 = user_cursor.fetchone()
        if user1:
            if check_password_hash(user1['password'], password):
                session['user'] = user1['email']
                return redirect(url_for('dashboard'))
            else:
                error = "Incorrect Password, Try again."
        else:
            error = 'Incorrect Email ID, Try again.'
            
    return render_template('login2index.html', loginerror = error, user = user)

# @app.route('/register', methods=["POST", "GET"])
# def register():
#     user = get_current_user()
#     db = get_database()
#     if request.method == 'POST':
#         name = request.form['name']
#         email = request.form['email']
#         password = request.form['password']
#         hashed_password = generate_password_hash(password)
#         dbuser_cur = db.execute('SELECT * FROM coordinator WHERE email = ?', [email])
#         existing_username = dbuser_cur.fetchone()
#         if existing_username:
#             return render_template('register.html', registererror = 'Email already taken , try registering with different email.')
#         db.execute('INSERT INTO coordinator ( name, email, password) values (?, ?, ?)',[name, email, hashed_password])
#         db.commit()
#         return redirect(url_for('index'))
#     return render_template('register.html', user = user)

@app.route('/register', methods=["POST", "GET"])
def register():
    user = get_current_user()
    db = get_database()
    if user and user['email'] == 'placementhead@rvce.edu.in':
        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            password = request.form['password']
            if not name or not email or not password:
                return render_template('register2index.html',user = user, registererror = 'Enter all details')
        
            hashed_password = generate_password_hash(password)
            dbuser_cur = db.execute('SELECT * FROM coordinator WHERE email = ?', [email])
            existing_username = dbuser_cur.fetchone() 
            if existing_username:
                return render_template('register2index.html',user = user, registererror = 'Email already taken , try registering with different email.')
            
            MY_ADDRESS = 'rvceplacement.review.2023@gmail.com'
            TO_ADDRESS = email
            PASSWORD = 'mbpbcrttmuosdudy'
            port = 465  # For SSL
            smtp_server = "smtp.gmail.com"
            sender_email = MY_ADDRESS  # Enter your address
            receiver_email = TO_ADDRESS  # Enter receiver address
            msg = "Subject: Student Placement Coordinator Registration\n\n"
            msg1 = "Hi " + name + ",\n\tYou have been registered as the student placement coordinator by the placement dean and here are your login credentials.\n\nName : " + name + "\nEmail : " + email + "\nPassword : " + password +"\n\nThanks,\nPlacement Dean"
            msg = msg + msg1
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                server.login(sender_email, PASSWORD)
                server.sendmail(sender_email, receiver_email, msg)
            
            db.execute('INSERT INTO coordinator ( name, email, password) values (?, ?, ?)',[name, email, hashed_password])
            db.commit()
            return redirect(url_for('register'))
        return render_template('register2index.html', user = user)
    else:
        return redirect(url_for('login'))
        # return render_template('login2.html', loginerror = 'Admin privilege needed', user = user)

# @app.route('/dashboard')
# def dashboard():
#     user = get_current_user()
#     db = get_database()
#     emp_cur = db.execute('select * from emp')
#     allemp = emp_cur.fetchall()
#     return render_template('dashboard.html', user = user, allemp = allemp)
@app.route('/topRecruiters', methods = ["POST"])
def topRecruiters():
    db = get_database()
    user = get_current_user() 
    if request.method == "POST":
        branch = request.form.get("branchToggle")
        offerType =  int(request.form.get("offerType"))
        print(offerType)
        salmin, salmax = 0, 1000
        if offerType ==  2:
            salmin, salmax = 8, 1000
        elif offerType == 3:
            salmin, salmax = 5, 8
        elif offerType == 4: 
            salmin, salmax = 0, 5 
        print('AAAAA')
        companies = db.execute("select compName, Count(USN) from offers where dept=? and ctc >= ? and ctc < ?  group by compName order by Count(USN) desc limit 15;",[branch,salmin,salmax])
        top_companies = [[row['compName'],row['Count(USN)']] for row in companies.fetchall()]
        print(top_companies)
        return json.dumps(top_companies)


@app.route('/statistics', methods = ["GET", "POST"])
def statistics():
    db = get_database()
    user = get_current_user()

    if request.method == "POST":
        toggle_val = int(request.form.get("toggle"))
        print(int(request.form.get("toggle")))
        print(type(toggle_val))
        salmin, salmax = 0, 1000
        if toggle_val ==  2:
            salmin, salmax = 8, 1000
        elif toggle_val == 3:
            salmin, salmax = 5, 8
        elif toggle_val == 4: 
            salmin, salmax = 0, 5 
        # else:
        #     return redirect(url_for('statistics'))
        sample1 = db.execute('select dept,count(usn) FILTER(WHERE ctc >= ? and ctc < ?) as cnt from offers group by dept order by dept;', [salmin, salmax])
        dept_offers1 = [[row['dept'],row['cnt']] for row in sample1.fetchall()]
        print(dept_offers1)
        return json.dumps(dept_offers1)
        #return render_template('chrt2.html',toggle_val = toggle_val, dept_offers = dept_offers1,alloffers =  [], ran = [], depts = [])

        #return render_template('chrt2.html', dept_offers = dept_offers1,alloffers =  [], ran = [], depts = [])

    if request.method == "GET":
        offer_cur = db.execute('select * from offers') 
        alloffers = offer_cur.fetchall()    
        all_offers_list = [] 
        for row in alloffers:
            all_offers_list.append([x for x in row])

        # extra
        alloffers = json.dumps( [dict(ix) for ix in alloffers]) 
        aList = json.loads(alloffers)
        aList = pd.DataFrame(aList)
        data = aList.to_numpy().tolist()
         # extra

        depts = db.execute('select DISTINCT(dept) from offers order by dept')
        all_depts = depts.fetchall() 
        all_depts_list = [] 
        for row in all_depts:
            all_depts_list.append(row['dept'])
        print(all_depts_list)

        sample = db.execute('select dept,count(usn) from offers group by dept order by dept;')
        dept_offers = [[row['dept'],row['COUNT(usn)']] for row in sample.fetchall()]
        print('XXXXXXXXXX')
        print(dept_offers)

        # Queries for Table
        table = db.execute('SELECT dept,COUNT(usn) as offers,MIN(ctc) AS min,MAX(ctc) AS max,ROUND(AVG(ctc),2) AS avg FROM offers GROUP BY dept ORDER BY dept;')
        table_data = [[row['dept'],row['offers'],row['min'],row['max'],row['avg']] for row in table.fetchall()]
        table_head = ['Department', 'Offers', 'Min ctc', 'Max ctc', 'Avg ctc', 'Median ctc']
        departments = db.execute('select DISTINCT dept AS department from offers order by dept;')
        dep = []
        for row in departments.fetchall():
            dep.append(row['department']) 
        for i in range(0,len(dep)):
            med = db.execute("SELECT AVG(ctc) AS median FROM (SELECT ctc FROM offers where dept = ? ORDER BY ctc LIMIT 2 - (SELECT COUNT(*) FROM offers where dept = ?) % 2 OFFSET (SELECT (COUNT(*) - 1) / 2 FROM offers where dept = ?))",[dep[i],dep[i],dep[i]])
            table_data[i].append(med.fetchone()['median'])
        
        # Top Companies Hiring From RVCE
        companies = db.execute('''
        select compName, Count(USN) from offers 
        where dept='CSE' 
        group by compName 
        order by Count(USN) 
        desc limit 15;
        ''')
        top_companies = [[row['compName'],row['Count(USN)']] for row in companies.fetchall()]
        print(top_companies)

        # Line chart query
        lineChartData = []
        for dept in dep:
            deptQuery = db.execute(''' 
            WITH months AS (
                SELECT '01' AS month_num UNION ALL
                SELECT '02' AS month_num UNION ALL
                SELECT '03' AS month_num UNION ALL
                SELECT '04' AS month_num UNION ALL
                SELECT '05' AS month_num UNION ALL
                SELECT '06' AS month_num UNION ALL
                SELECT '07' AS month_num UNION ALL
                SELECT '08' AS month_num UNION ALL
                SELECT '09' AS month_num UNION ALL
                SELECT '10' AS month_num UNION ALL
                SELECT '11' AS month_num UNION ALL
                SELECT '12' AS month_num
            ),
            offers_count AS (
                SELECT strftime('%m', offerDate) AS month, COUNT(usn) AS numOfOffers
                FROM offers
                WHERE dept = ?
                GROUP BY month
            )
            SELECT COALESCE(offers_count.numOfOffers, 0) AS num_offers
            FROM months
            LEFT JOIN offers_count ON months.month_num = offers_count.month
            ORDER BY months.month_num;
            ''', [dept]);
            deptData = [row['num_offers'] for row in deptQuery.fetchall()]
            lineChartData.append(deptData)
            

        # Query for number of students placed
        students = db.execute('select dept,COUNT(DISTINCT USN) from offers group by dept order by dept;')
        num_of_students = [[row['dept'],row['COUNT(DISTINCT USN)']] for row in students.fetchall()]
        print('YYYYYYYYYYY')
        print(num_of_students)

        return render_template('chrt2index.html',user = user, table_data = table_data, tableYear = 2022, dept_offers = dept_offers, num_of_students = num_of_students, top_companies =top_companies,lineChartData=lineChartData)

@app.route('/dashboard')
def dashboard():
    user = get_current_user()
    db = get_database()
    if user:
        offer_cur = db.execute('select * from offers')
        alloffers = offer_cur.fetchall()
        return render_template('dashboard2index.html', user = user, alloffers = alloffers)
    else:
        return redirect(url_for('login'))

@app.route('/addnewoffer', methods = ["POST", "GET"])
def addnewoffer():
    user = get_current_user()
    if request.method == "POST":
        usn = request.form['usn']
        name = request.form['name']
        dept = request.form['dept']
        gender = request.form['gender']
        compName = request.form['compName']
        offerType = request.form['offerType']
        ctc = request.form['ctc']
        jobProfile = request.form['jobProfile']
        category = request.form['category']
        remarks = request.form['remarks']
        offerDate = request.form['offerDate']

        db = get_database()
        db.execute('insert into offers (usn, name, dept, gender ,compName ,offerType ,ctc ,jobProfile ,category ,remarks ,offerDate) values (?,?,?,?,?,?,?,?,?,?,?)', [usn, name, dept, gender ,compName ,offerType ,ctc ,jobProfile ,category ,remarks ,offerDate])
        db.commit()
        return redirect(url_for('dashboard'))
    return render_template('addnewoffer2index.html', user = user)
@app.route('/singleemployee/<int:empid>')
def singleemployee(empid):
    user = get_current_user()
    db = get_database()
    emp_cur = db.execute('select * from emp where empid = ?', [empid])
    single_emp = emp_cur.fetchone()
    return render_template('singleemployee.html', user = user, single_emp = single_emp)

@app.route('/fetchone/<string:usn>')
def fetchone(usn):
    user = get_current_user()
    db = get_database()
    offer_cur = db.execute('select * from offers where usn = ?', [usn])
    single_offer = offer_cur.fetchone()
    return render_template('updateofferindex.html', user = user, single_offer = single_offer)

@app.route('/updateoffers' , methods = ["POST"])
def updateoffer():
    user = get_current_user()
    usn = request.form['usn']
    name = request.form['name']
    dept = request.form['dept']
    gender = request.form['gender']
    compName = request.form['compName']
    offerType = request.form['offerType']
    ctc = request.form['ctc']
    jobProfile = request.form['jobProfile']
    category = request.form['category']
    remarks = request.form['remarks']
    offerDate = request.form['offerDate']
    db = get_database()
    db.execute('update offers set name = ?, dept = ? , gender = ? , compName = ? , offerType = ?, ctc = ?, jobProfile = ?, category = ?, remarks = ?, offerDate = ? where usn = ?', [name, dept, gender, compName, offerType, ctc, jobProfile, category, remarks, offerDate, usn])
    db.commit()
    return redirect(url_for('dashboard'))

@app.route('/deleteoffer/<string:usn>', methods = ["GET", "POST"])
def deleteoffer(usn):
    user = get_current_user()
    if request.method == 'GET':
        db = get_database()
        db.execute('delete from offers where usn = ?', [usn])
        db.commit()
        return redirect(url_for('dashboard'))
    return render_template('dashboard2index.html', user = user)

@app.route('/review', methods = ["POST"])
def reviews():
    user = get_current_user()
    review = request.form['review']
    MY_ADDRESS = 'rvceplacement.review.2023@gmail.com'
    TO_ADDRESS = 'harshahl.cs20@rvce.edu.in'
    PASSWORD = 'mbpbcrttmuosdudy'
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = MY_ADDRESS  # Enter your address
    receiver_email = TO_ADDRESS  
    password = PASSWORD
    msg = "Subject: RVCE Placement Website Review\n\n"
    msg = msg + review
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg)

    print(review)

#   MONGO UPADATE

    data = request.form.get("review")
    result = nlp(data)
    print(test.insert_one({'text':data.strip(),'sentiment':result[0]['label']}))

    return render_template('index.html', user = user)

@app.route('/timeline', methods = ["GET", "POST"])
def timeline():
    db = get_database()
    user = get_current_user()
    if request.method == 'GET':
        events = db.execute('SELECT * FROM drive ORDER BY date(date); ')
        allevents = events.fetchall()
        return render_template('timeline.html', user = user, events = allevents)    
    else:
        companyName = request.form['companyName']
        companySymbol = request.form['companySymbol']
        offerType = request.form['offerType'] 
        semester = request.form['semester']
        branches = request.form['branches']
        stipendCtc = request.form['stipendCtc']
        date = request.form['date']
        company = yf.Ticker(companySymbol)
        info = company.info
        try:
            website = info['website']
        except:
            website = 'www.google.com'
        try:
            summary = ".".join(info['longBusinessSummary'].split(".")[:2]) + "."
        except:
            summary = ''
        try:
            location = info['state'] + ', ' + info['country']
        except:
            location = ''
        try:
            employees = info['fullTimeEmployees']
        except:
            employees = ''
        try:
            sector = info['sector']
        except:
            sector = ''
        try:
            industry = info['industry']
        except:
            industry = ''
        try:
            logo_url = info['logo_url']
        except:
            logo_url = ''

        
        print(companyName)
        print(companySymbol)
        print(offerType)
        print(semester)
        print(branches)
        print(stipendCtc)
        print(website)
        print(summary)
        print(location)
        print(employees)
        print(sector)
        print(industry)
        print(logo_url)
        print(date)
        db.execute('insert into drive (companyName, companySymbol, offertype, semester , branches , stipendCtc , website , summary , location , employees , sector , industry , logo_url , date) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?)', [companyName, companySymbol, offerType, semester , branches , stipendCtc , website , summary , location , employees , sector , industry , logo_url , date])
        db.commit()
        return redirect(url_for('timeline'))

# -------------------------------------------Resume and Jobs------------------------------------------------------#

class UploadFileForm(FlaskForm):
    file = FileField("File", validators = [InputRequired()])
    submit = SubmitField("Submit")


PHONE_REG_GH = re.compile(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]')

PHONE_REG_USA = re.compile(r'/^\(?(\d{3})\)?[-]?(\d{3})[-]?(\d{4})$/') 

EMAIL_REG = re.compile(r'[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+')


def extract_text_from_pdf(pdf_path):
    text = extract_text((pdf_path))
    return text

def extract_emails(resume_text):
    return re.findall(EMAIL_REG, resume_text)


def extract_names(txt):

    person_names = []

    for sent in nltk.sent_tokenize(txt):
        for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
            if hasattr(chunk, 'label') and chunk.label() == 'PERSON':
                person_names.append(
                    ' '.join(chunk_leave[0] for chunk_leave in chunk.leaves())
                )

    return person_names 


# generate random file names
letters = [random.choice(string.ascii_lowercase) for i in range(4)]
random_filename = ''.join(letters)
    

def extract_phone_number(resume_text):
    phone = re.findall(PHONE_REG_GH, resume_text)

    if phone:
        number = ''.join(phone[0])

        if resume_text.find(number) >= 0 and len(number) < 16:
            return number
    return None 

file_skills_domain = pd.read_excel(join(dirname(realpath(__file__)), 'static/ResumeSkill.xlsx'))
file_skills_domain.columns = file_skills_domain.columns.str.strip().str.upper()

list_domains = []
for col in file_skills_domain.columns:
  
    file_skills_domain[col] = file_skills_domain[col].str.strip().str.upper()

    if col != 'EDUCATION' :
        list_domains.append('%s' % col)
        globals()['%s' % col]= [x for x in file_skills_domain[col].to_list() if type(x) != float]

list_skills = []
for i in list_domains:
  list_skills=list_skills + eval(i)


skills_dict = {}
domain_list = []


def extract_skills(input_text):
    stop_words = set(nltk.corpus.stopwords.words('english'))
    word_tokens = nltk.tokenize.word_tokenize(input_text)

    # remove the stop words
    filtered_tokens = [w for w in word_tokens if w not in stop_words]

    # remove the punctuation
    filtered_tokens = [w for w in word_tokens if w.isalpha()]

    # generate bigrams and trigrams (such as artificial intelligence)
    bigrams_trigrams = list(map(' '.join, nltk.everygrams(filtered_tokens, 1, 3)))

    # we create a set to keep the results in.
    found_skills = set()

    # we search for each token in our skills database
    for token in filtered_tokens:
        if token.upper() in list_skills:
            found_skills.add(token)

    # we search for each bigram and trigram in our skills database
    for ngram in bigrams_trigrams:
        if ngram.upper() in list_skills:
            found_skills.add(ngram)

    for skill in found_skills :
        if skill.upper() not in skills_dict.keys():
            skill = skill.upper()
            cnt = 0
            for i in bigrams_trigrams:
                i = i.upper()
                if skill in i:
                    cnt += 1
                    for j in list_domains:
                        if skill in eval(j):
                            domain_list.append(j)

            print(skill.upper(), ' is repeated ' , cnt, ' times.')
            skills_dict[skill.upper()]= cnt


@app.route('/jobs', methods = ['GET',"POST"])
def upload():
    form = UploadFileForm()
    print(form)
    if request.method == 'POST':
        root_dir = app.config['UPLOAD_FOLDER']
        
        if form.validate_on_submit():
            file = form.file.data 
            file_path = ""
            file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),
            app.config['UPLOAD_FOLDER'], secure_filename(file.filename))) 
            
            file_path += ((os.path.join(root_dir,file.filename)))

            txt = extract_text_from_pdf(file_path)
            names = extract_names(txt)
            name_candidate = names[0] + ' ' + names[1].split(' ')[0]

            phone_number_gh = extract_phone_number(txt)
            phone_number_usa = None

            phone_contact = []
            phone_contact.append(phone_number_gh)

            print(phone_contact)
            
            emails = extract_emails(txt)

            if emails:
                print(emails)

            general_dict = { 'Name' : name_candidate.upper(),
                'Email' : emails ,
                'Contact' : phone_contact
        
            }  

            print(phone_contact) 



            # Exxctract Skills Part
            input_text = txt
            stop_words = set(nltk.corpus.stopwords.words('english'))
            word_tokens = nltk.tokenize.word_tokenize(input_text)

            # remove the stop words
            filtered_tokens = [w for w in word_tokens if w not in stop_words]

            # remove the punctuation
            filtered_tokens = [w for w in word_tokens if w.isalpha()]

            # generate bigrams and trigrams (such as artificial intelligence)
            bigrams_trigrams = list(map(' '.join, nltk.everygrams(filtered_tokens, 1, 3)))

            # we create a set to keep the results in.
            found_skills = set()

            # we search for each token in our skills database
            for token in filtered_tokens:
                if token.upper() in list_skills:
                    found_skills.add(token)

            # we search for each bigram and trigram in our skills database
            for ngram in bigrams_trigrams:
                if ngram.upper() in list_skills:
                    found_skills.add(ngram)

            for skill in found_skills :
                if skill.upper() not in skills_dict.keys():
                    skill = skill.upper()
                    cnt = 0
                    for i in bigrams_trigrams:
                        i = i.upper()
                        if skill in i:
                            cnt += 1
                            for j in list_domains:
                                if skill in eval(j):
                                    domain_list.append(j)

                    print(skill.upper(), ' is repeated ' , cnt, ' times.')
                    skills_dict[skill.upper()]= cnt
            score_list = []
    
            df = pd.read_csv("naukri-jobs.csv")
            for index, row in df.iterrows():
                job_skill = row["Skills"].split(',')
                job_skill = [skill.lower() for skill in job_skill]
                matches = 0
                found_skills.clear()
                for word in bigrams_trigrams:
                    if word.lower() not in skills_dict.keys() and word.lower() in job_skill:
                        found_skills.add(word.lower())
                        matches+=1
                score_list.append(matches/len(job_skill))
            df["Score"] = score_list
            df.sort_values(by=['Score'],ascending=False,inplace=True)
            print(df)
            
            # End Of extract skills

            new_vals = Counter(domain_list).most_common()
            new_vals = new_vals[::-1] #this sorts the list in ascending order
            print("this is: ", new_vals)

            domain_dict = {}
            for a, b in new_vals:
                domain_dict[a] = b


            general_dict["skills"] = skills_dict
            if len(new_vals) > 1:
                general_dict["domain"] = [new_vals[-1][0],new_vals[-2][0]]
            else: 
                new_vals = []

            skill_df = json_normalize(general_dict['skills'])
            num = skill_df.sum(axis = 1)[0]

            list_details = []
            for skill_x in skill_df.columns:
                list_details.append({
                        'doc':file_path ,'Name' : name_candidate.upper(),
                        'email' : emails[0] if emails else None,
                        'contact' : phone_contact[0] if phone_contact else None ,
                        'domain':[new_vals[-1][0][5:],new_vals[-2][0][5:]] if len(new_vals) > 1  else ["No domains"],
                        'skills':skill_x ,
                        'normalised_count':round((skill_df[skill_x][0]*100)/num,2),
                        'total_skills':list(skill_df.columns)
                    })

            job_description = docx2txt.process(join(dirname(realpath(__file__)), 'static/job_desc.docx'))
            resume = docx2txt.process(join(dirname(realpath(__file__)), 'static/resume1.docx'))

            text = [resume, job_description]

            # Calculate similarity score 
            cv = CountVectorizer()
            count_matrix = cv.fit_transform(text)
            print("\Similarity Score: ")
            print(cosine_similarity(count_matrix))

            # Count match percentage
            match_percentage = cosine_similarity(count_matrix)[0][1] * 100
            match_percentage = round(match_percentage, 2)
            print()
            print("The match percentage of the resume is ", match_percentage,"%")

            jobs_data = df.to_json(orient='records')

            return render_template(
                    'jobs.html', plot_url = "./static/plot.png", plot_url_two = "./static/plot.png", 
                    user_data = general_dict,
                    match_percentage = match_percentage , form = form,jobs_data = jobs_data
                )
    else:
        df = pd.read_csv('naukri-jobs.csv')
        jobs_data = df.to_json(orient='records')
        return render_template('jobs.html',form=form,jobs_data = jobs_data)

    return render_template('jobs.html',form=form,jobs_data = "")




@app.route('/logout') 
def logout():
    session.pop('user', None)
    return render_template('index.html')
 
if __name__ == '__main__':
    app.run(debug = True)