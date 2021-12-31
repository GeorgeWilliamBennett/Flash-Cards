from flask import Flask, render_template, request, redirect
import sqlite3

# load application to a variable
app = Flask(__name__)

# for id generation
next_id = 1

# connect to database
def connect_db():
    con = sqlite3.connect('flashcards.db')
    cr = con.cursor()
    return cr, con

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
    set_name = set_name.replace(' ', '_')
    set_name = set_name.replace('-', '')
    query = f"""
        CREATE TABLE {set_name} (
            id INT NOT NULL,
            question VARCHAR(255) NOT NULL,
            answer VARCHAR(255) NOT NULL
        )
        """
    try: 
        cr, con= connect_db()
        cr.execute(query)
        con.commit()
        cr.close()
    except:
        return response_page('There is Already a Set of Cards with that Name')
    return redirect(f'/practice/{set_name}')

# choosing a set
@app.route('/choose-set-prompt')
def choose_set_prompt():
    cr, _ = connect_db()
    query = """
        SELECT name FROM sqlite_schema WHERE type='table' ORDER BY name
        """
    cr.execute(query)
    sets = [x[0] for x in cr.fetchall()]
    cr.close()
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
    question = request.form['question-prompt']
    answer = request.form['answer-prompt']
    cr, con = connect_db()
    query = f"""
        INSERT INTO {set_name} (id, question, answer) VALUES ({globals()['next_id']}, '{question}', '{answer}')
        """
    cr.execute(query)
    con.commit()
    cr.close()
    globals()['next_id'] += 1
    return redirect(f'/practice/{set_name}')

# practice
@app.route('/practice/<set_name>')
def practice(set_name):
    query = f"""
        SELECT * FROM {set_name} ORDER
        BY RANDOM() LIMIT 1
        """
    cr, _ = connect_db()
    cr.execute(query)
    rand_card = False
    try: 
        rand_card = cr.fetchall()[0]
    except:
        pass
    cr.close()
    if rand_card:
        return render_template('practice.html', card=rand_card, set_name=set_name)
    else:
        return redirect(f'/create-card-prompt/{set_name}')

# delete card
@app.route('/delete-card/<set_name><card_id>')
def delete_card(set_name, card_id):
    query = f"""
        DELETE FROM {set_name} WHERE id = {card_id}
        """
    cr, con = connect_db()
    cr.execute(query)
    con.commit()
    query2 = f"""
        SELECT * FROM {set_name}
        """
    cr.execute(query2)
    rows = cr.fetchall()
    if rows:
        return redirect(f'/practice/{set_name}')
    else:
        return response_page('All Cards in this Set Have Been Deleted')


@app.route('/delete-set-prompt')
def delete_set_prompt():
    cr, _ = connect_db()
    query = """
        SELECT name FROM sqlite_schema WHERE type='table' ORDER BY name
        """
    cr.execute(query)
    sets = [x[0] for x in cr.fetchall()]
    cr.close()
    return render_template('delete-set-prompt.html', sets=sets)

# delete set of cards
@app.route('/delete-set/<set_name>')
def delete_set(set_name):
    query = f"""
        DROP TABLE {set_name}
        """
    cr, con = connect_db()
    cr.execute(query)
    con.commit()
    cr.close()
    return response_page('Set Deleted')

# run program
if __name__ == "__main__":
    app.run()