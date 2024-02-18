from flask import Flask, render_template, request,  redirect, url_for


app = Flask(__name__, static_url_path='/static')

# Sample data - Replace with your actual nominees
categories = {
    'Best Picture': ['Nominee 1', 'Nominee 2', 'Nominee 3'],
    'Best Actor': ['Actor 1', 'Actor 2', 'Actor 3'],
    
    
}


actual_winners = {category: None for category in categories}

votes = []

@app.route('/')
def index():
    return render_template('index.html', categories=categories)

@app.route('/vote', methods=['POST'])
def vote():
    global votes
    user_vote = {category: request.form[category] for category in categories}
    votes.append(user_vote)
    return redirect(url_for('results'))

@app.route('/results')
def results():
    return render_template('results.html', votes=votes, actual_winners=actual_winners)

@app.route('/update_results', methods=['POST'])
def update_results():
    global actual_winners
    actual_winners = {category: request.form[category] for category in categories}
    return redirect(url_for('results'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
    
    