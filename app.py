# using python 3
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required, Optional
from data import JOURNALISTS

app = Flask(__name__)
# Flask-WTF requires an enryption key - the string can be anything
app.config['SECRET_KEY'] = 'some?bamboozle#string-foobar'
# Flask-Bootstrap requires this line
Bootstrap(app)
# this turns file-serving to static, using Bootstrap files installed in env
# instead of using a CDN
app.config['BOOTSTRAP_SERVE_LOCAL'] = True

class NameForm(FlaskForm):
    name = StringField('Search by name', validators=[Optional()])
    nameSubmit = SubmitField('Search')
    
class InterestForm(FlaskForm):
    interest = StringField('Search by interest', validators=[Optional()])
    interestSubmit = SubmitField('Search')
    
class PublicationForm(FlaskForm):
    publication = StringField('Search by publication', validators=[Optional()])
    publicationSubmit = SubmitField('Search')
    
class LocationForm(FlaskForm):
    location = StringField('Search by location', validators=[Optional()])
    locationSubmit = SubmitField('Search')
    
def get_names(source):
    names = []
    for row in source:
        name = row["name"]
        names.append(name)
    return (names)

def get_journalist(source, id):
    for row in source:
        if id == str( row["id"] ):
            name = row["name"]
            title = row["title"]
            publication = row["publication"]
            interest = row["interest"]
            location = row["location"]
            # change number to string
            id = str(id)
            # return these if id is valid
            return id, name, title, publication, interest, location
    # return these if id is not valid - not a great solution, but simple
    return "Unknown", "Unknown", ""

# find the row that matches the name in the form and retrieve matching id
def get_id(source, name):
    for row in source:
        if name == row["name"]:
            id = row["id"]
            # change number to string
            id = str(id)
            # return id if name is valid
            return id
    # return these if id is not valid - not a great solution, but simple
    return "Unknown"

def get_interests(source):
    interests = []
    for row in source:
        id = row["id"]
        name = row["name"]
        interest = row["interest"]
        interests.append([id, name, interest])
    return (interests)

@app.route('/', methods=['GET', 'POST'])
@app.route('/index.html', methods=['GET', 'POST'])
def names():
    # you must tell the variable 'form' what you named the class, above
    # 'form' is the variable name used in this template: index.html
    form = NameForm(csrf_enabled=False)
    name_form = NameForm()
    interest_form = InterestForm()
    publication_form = PublicationForm()
    location_form = LocationForm()
    if name_form.validate_on_submit():
        name = name_form.name.data
        names = get_names(JOURNALISTS)
        if name in names:
            name_form.name.data = ""
            id = get_id(JOURNALISTS, name)
            # redirect the browser to another route and template
        return redirect( url_for('name', id=id) )
    elif interest_form.validate_on_submit():
        interest = interest_form.interest.data
        if interest in interests:
            interest_form.interest.data = ""
            interest = get_interests(JOURNALISTS, pairs=interests)
            # redirect the browser to another route and template
        return redirect( url_for('interest', interest=interest) )
    elif publication_form.validate_on_submit():
        publication = publication_form.publication.data
        if publication in publications:
            publication_form.publication.data = ""
            publication = get_names(JOURNALISTS, publication)
            # redirect the browser to another route and template
        return redirect( url_for('publication', publication=publication) )
    elif location_form.validate_on_submit():
        location = location_form.location.data
        if location in locations:
            location_form.name.data = ""
            location = get_names(JOURNALISTS, location)
            # redirect the browser to another route and template
        return redirect( url_for('location', location=location) )
    else:
        message = "That journalist did not attend ONA17"
    # notice that we don't need to pass name or names to the template
    return render_template('index.html', name_form=name_form, interest_form=interest_form, publication_form=publication_form, location_form=location_form)

@app.route('/name/<id>')
def journalist(id):
    # run function to get actor data based on the id in the path
    id, name, title, publication, interest, location = get_journalist(JOURNALISTS, id)
    if name == "Unknown":
        return render_template('404.html'), 404
    else:
        # pass all the data for the selected actor to the template
        return render_template('name.html', id=id, name=name, title=title, publication=publication, interest=interest, location=location)
    
@app.route('/interest/<interest>')    
def interests():
    interests = get_interests(JOURNALISTS)
    return render_template('interest.html', pairs=interests)


# keep this as is
if __name__ == '__main__':
    app.run(debug=True)