A simple Django project where teachers can register, log in, add students, update marks, and view audit logs.  

##TeACHER portal
A simple Django web application where teachers can:
Login and manage their students
Add, update, and delete student records
View a list of students with inline editing of marks
Secure login and logout without using Django’s built-in authentication

#Security Considerations
CSRF protection enabled ({% csrf_token %} in all forms)
Session-based authentication (custom session handling)
Input validation (marks must be 0–100)
Steps:
	git clone https://github.com/skravi1996/Teacher-portal.git

#Create virtual environment
python -m venv venv
#activate
source venv/bin/activate
#Install dependencies
pip install -r requirements.txt
#Run migrations
python manage.py migrate
#Run
python manage.py runserver

 
