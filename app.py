from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import numpy as np

# load application to a variable
app = Flask(__name__)

# setup SQL Alchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 0
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Set(db.Model):
    __tablename__ = 'set'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __init__(self, name):
        self.name = name

class FlashCard(db.Model):
    __tablename__ = 'flashcard'
    id = db.Column(db.Integer, primary_key=True)
    setId = db.Column(db.Integer)
    question = db.Column(db.String(300))
    answer = db.Column(db.String(300))

    def __init__(self, setId, question, answer):
        self.setId = setId
        self.question = question
        self.answer = answer

# render a page with a simple message
def response_page(msg):
    return render_template('response-page.html', msg=msg)

# homepage
@app.route('/')
def index():
    return render_template('index.html')

# creating a new set of cards
@app.route('/create-set-prompt')
def create_set_prompt():
    return render_template('create-set-prompt.html')


@app.route('/create-new-set', methods=['POST'])
def create_new_set():
    set_name = request.form['set-name']
    set_names = db.session.query(Set).filter(Set.name == set_name).all()
    if len(set_names) < 1:
        data = Set(set_name)
        db.session.add(data)
        db.session.commit()
        return redirect(f'/practice/{set_name}')
    else:
        return response_page('There is Already a Set of Cards with that Name')
    

# choosing a set
@app.route('/choose-set-prompt')
def choose_set_prompt():
    sets = [x.name for x in db.session.query(Set).all()]
    if sets:
        return render_template('choose-set-prompt.html', sets=sets)
    else:
        return response_page('You Have not Created Any Sets of Cards')


# creating cards
@app.route('/create-card-prompt/<set_name>')
def create_card_prompt(set_name):
    return render_template('create-card-prompt.html', set_name=set_name)

@app.route('/create-card/<set_name>', methods=['POST'])
def create_card(set_name):
    setId = db.session.query(Set).filter(Set.name == set_name).first().id
    question = request.form['question-prompt']
    answer = request.form['answer-prompt']
    db.session.add(FlashCard(setId, question, answer))
    db.session.commit()
    return redirect(f'/practice/{set_name}')

# practice
@app.route('/practice/<set_name>')
def practice(set_name):
    setId = db.session.query(Set).filter(Set.name == set_name).first().id
    cards = db.session.query(FlashCard).filter(FlashCard.setId == setId).all()
    try: 
        rand_card = np.random.choice(cards)
    except:
        rand_card = False
    if rand_card:
        return render_template('practice.html', card=rand_card, set_name=set_name)
    else:
        return redirect(f'/create-card-prompt/{set_name}')

# delete card
@app.route('/delete-card/<set_name>/<card_id>')
def delete_card(set_name, card_id):
    delete_this = db.session.query(FlashCard).filter(FlashCard.id == card_id).first()
    db.session.delete(delete_this)
    db.session.commit()
    return redirect(f'/practice/{set_name}')


@app.route('/delete-set-prompt')
def delete_set_prompt():
    sets = [x.name for x in db.session.query(Set).all()]
    return render_template('delete-set-prompt.html', sets=sets)

# delete set of cards
@app.route('/delete-set/<set_name>')
def delete_set(set_name):
    delete_this = db.session.query(Set).filter(Set.name == set_name).first()
    db.session.delete(delete_this)
    db.session.commit()
    return response_page('Set Deleted')

# run program
if __name__ == "__main__":
    app.run()