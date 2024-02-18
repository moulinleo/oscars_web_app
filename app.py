from flask import Flask, render_template, request,  redirect, url_for
from bs4 import BeautifulSoup
import requests
import pandas as pd
from warnings import filterwarnings 
filterwarnings("ignore")

app = Flask(__name__, static_url_path='/static')


def scrap_nominees(url="https://en.wikipedia.org/wiki/96th_Academy_Awards"):
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    indiatable=soup.find('table',{'class':"wikitable"}, role="presentation")
    
    # Create an empty DataFrame to store the nominees
    df_nominees = pd.DataFrame(columns=['category', 'nominees'])

    # Extract rows from the table
    rows = indiatable.find_all('tr')

    # Iterate through rows and print the content
    for row in rows:
        # Extract cells from the row
        cells = row.find_all(['th', 'td'])
        
        # Extract text from each cell
        cell_data = [cell.get_text(strip=False) for cell in cells]
        
        for col in [0,1]:
            try:
                split_cell = cell_data[col].split('\n')[:-1]
            except:
                continue
            category = split_cell[0]
            nominees = split_cell[1:]
            
            df_nominees = df_nominees.append({'category': category, 'nominees': nominees}, ignore_index=True)

    nominees_dict = dict(zip(df_nominees['category'], df_nominees['nominees']))
    return nominees_dict

def calculate_points(user_vote):
    total_points = 0
    for category, vote in user_vote.items():
        if actual_winners[category] == vote:
            if category == 'Best Picture':
                total_points += 4
            elif category == 'Best Director':
                total_points += 3
            elif category == 'Best Actor' or category == 'Best Actress':
                total_points += 2
            elif category == 'Best Supporting Actor' or category == 'Best Supporting Actress':
                total_points += 2
            else:
                total_points += 1
    return total_points
app.jinja_env.globals.update(calculate_points=calculate_points)




categories = scrap_nominees(url="https://en.wikipedia.org/wiki/96th_Academy_Awards")


# Keep only the first two keys
num_keys_to_keep = 2
categories = {key: categories[key] for key in list(categories.keys())[:num_keys_to_keep]}


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

@app.route('/enter_winners', methods=['GET', 'POST'])
def enter_winners():
    global actual_winners
    if request.method == 'POST':
        actual_winners = {category: request.form[category] for category in categories}
        return redirect(url_for('results'))
    return render_template('enter_winners.html', categories=categories)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
    
    