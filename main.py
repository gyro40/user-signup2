from flask import Flask, request, redirect
import cgi
import os
import jinja2

template_dir = os.path.join(os.path.dirname(__file__),'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))

app = Flask(__name__)
app.config['DEBUG']=True

@app.route("/")
def display_login_form():
    template = jinja_env.get_template("index.html")
    return template.render()

@app.route('/', methods=['POST'])
def validate():

    invalid_char = ' '

    username = request.form['username']
    password = request.form['password']
    verify = request.form['verify']
    email = request.form['email']

    username_error = ''
    password_error = ''
    verify_error = ''
    email_error = ''

    if len(username) == 0:
        username = ''
        username_error = "Error: Username cannot be blank"
    elif len(username) > 20 or len(username) < 3: 
        username = ''
        username_error = "Error: Username must be between 3-20 characters"   

    if len(password) == 0:
        password = ''
        password_error = "Error: Password cannot be blank"
    elif len(password) > 20 or len(password) < 3: 
        password = ''
        password_error = "Error: Username must be between 3-20 characters"      

    if len(verify) == 0:
        verify = ''
        verify_error = "Error: Field cannot be blank"
    elif verify != password:
        verify = ''
        verify_error = "Error: Passwords don't match"

    for char in username:
        if char in invalid_char:
            username = ''
            username_error = "Error: Username cannot contain spaces"

    for char in password:
        if char in invalid_char:
            password = ''
            password_error = "Error: Password cannot contain spaces"

    if len(email) > 0:

        if email.count("@") != 1 or email.count(".") != 1:
            email = ''
            email_error = "Error: Invalid email"
        elif len(email) < 3 or len(email) > 20:
            email = ''
            email_error = "Error: email must be between 3 and 20 characters"
        for char in email:
            if char in invalid_char:
                email = ''
                email_error = "Error: Invalid email"

    template = jinja_env.get_template("index.html")
    
    if not username_error and not password_error and not verify_error and not email_error:
        
        return redirect('/welcome?username={0}'.format(username)) 
    else:
        return template.render(username=username, username_error=username_error, password_error=password_error, verify_error=verify_error, email=email, email_error=email_error)

@app.route("/welcome")
def welcome():
    username = request.args.get('username')
    template = jinja_env.get_template("welcome.html")
    return template.render(username=username)

app.run()