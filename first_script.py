from flask import Flask, request, make_response, redirect, render_template, session, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import Form
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, SubmitField
from wtforms.validators import Required

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.dirname(__file__))
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SECRET_KEY'] = "super secret string"

bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)

class NameForm(Form):
	name = StringField("Hoe is jouw naam?", validators=[Required()])
	sumbit = SubmitField("Submit")

@app.route("/", methods=["GET","POST"])
def index():
	form = NameForm()
	if form.validate_on_submit():
		old_name = session.get('name')
		if old_name is not None and old_name != form.name.data:
			flash("Looks like you have changed your name!")
		session['name'] = form.name.data
		form.name.data = ""
		return redirect(url_for('index'))
	user_agent = request.headers.get("User-Agent")
	comments = ["kip","chicken","poulet","pollo","more chicken"]
	return render_template('index.html', user_agent = user_agent, comments = comments, current_time = datetime.utcnow(), form=form, name=session.get('name'))

@app.route("/user/<name>")
def user(name):
	return render_template('user.html', name=name)

@app.route("/cookie")
def cookie():
	response = make_response("<b> This document carries a cookie! </b>")
	response.set_cookie("answer","42")
	return response
	
@app.route("/redirection")
def redirection():
	return redirect("http://localhost:5000/user/Dombo")
	
@app.errorhandler(404)
def page_not_found(e):
	return render_template("404.html"), 404

if __name__ == "__main__":
	app.run(debug=True)
