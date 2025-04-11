from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Flashcard data
flashcards = [
    {"question": "How many players are on a basketball team on the court?", "answer": "5"},
    {"question": "What is it called when a player puts the ball through the hoop?", "answer": "Score"},
    {"question": "Who is known as 'MJ23'?", "answer": "Michael Jordan"},
    {"question": "What does NBA stand for?", "answer": "National Basketball Association"},
    {"question": "How many points is a free throw worth?", "answer": "1"},
]

@app.route('/')
def index():
    session['current'] = 0
    session['score'] = 0
    return render_template('index.html')

@app.route('/flashcard', methods=['GET', 'POST'])
def flashcard():
    current = session.get('current', 0)

    if current >= len(flashcards):
        return redirect(url_for('result'))

    if request.method == 'POST':
        user_answer = request.form.get('user_answer', '').strip()

        if user_answer == '':
            flash("Please enter an answer before submitting.")
            return redirect(url_for('flashcard'))

        correct_answer = flashcards[current]['answer']
        if user_answer.lower() == correct_answer.lower():
            session['score'] += 1

        session['current'] += 1
        return redirect(url_for('flashcard'))

    flashcard = flashcards[current]
    return render_template('flashcard.html', flashcard=flashcard, index=current + 1, total=len(flashcards))

@app.route('/result')
def result():
    score = session.get('score', 0)
    total = len(flashcards)
    return render_template('result.html', score=score, total=total)

@app.route('/restart')
def restart():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
