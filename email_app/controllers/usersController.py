from flask import Flask, render_template, request, redirect, session
from email_app import app
from email_app.models import userModel

@app.errorhandler(404)
def page_not_found(error):
    app.logger.error(error)
    return render_template('404.html'), 404

@app.route('/', methods=['GET'])
def index():

    if 'email' in session:
        session.pop('email')

    return render_template("index.html")

@app.route('/create_user', methods=['POST'])
def create_user():
    
    if not userModel.User.validateUser(request.form):
        return redirect('/')

    data = {
        'email': request.form.get('email')
    }

    result = userModel.User.save(data)

    print(result)

    if result:
        session['email'] = request.form.get('email')
        return redirect('/success')
    else:
        return redirect('/')

@app.route('/success', methods=['GET'])
def success():
    
    email = None

    if 'email' in session:
        email = session['email']
        # userModel.User.validateUser({'email': email})

    users = userModel.User.get_all()

    return render_template('success.html', users = users)