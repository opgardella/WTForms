from flask import Flask, request, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import Required, Email

import requests
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.debug = True

@app.route('/')
def home():
    return "Hello, world!"

#create class to represent WTForm that inherits flask form
class ArtistForm(FlaskForm):
    artist = StringField('What is the artist name?', validators=[Required()])
    num_results = IntegerField('How many results do you want to see?', validators=[Required()])
    email = StringField('What is your email?', validators=[Required(),Email()])
    submit = SubmitField('Submit')

@app.route('/itunes-form')
def itunes_form():
    #what goes here
    simpleForm = ArtistForm()
    return render_template('itunes-form.html', form=simpleForm) # HINT : create itunes-form.html to represent the form defined in your class

@app.route('/itunes-results', methods = ['GET', 'POST'])
def itunes_result():
    #what code goes here?
    # HINT : create itunes-results.html to represent the results and return it
    form = ArtistForm(request.form)
    params_diction = {}
    if request.method == 'POST' and form.validate_on_submit():
        params_diction['term'] = form.artist.data
        params_diction['limit'] = form.num_results.data #basically request.args.get('num_results')
        email = form.email.data
        response = requests.get('https://itunes.apple.com/search', params = params_diction)
        response_text = json.loads(response.text)
        result_py = response_text['results']
        return render_template('itunes-results.html', result__html = result_py)
    flash('All fields are required!')
    return redirect(url_for('itunes_form')) #this redirects you to itunes_form if there are errors

if __name__ == '__main__':
    app.run()
