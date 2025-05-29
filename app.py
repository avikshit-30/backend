from flask import Flask, request, render_template
import pandas as pd
import os

app = Flask(__name__)

# Load data
stations_df = pd.read_csv('stations.csv')  # Sheet 1
details_df = pd.read_csv('details.csv')    # Sheet 2

# Convert stipend to integer if possible
def format_stipend(x):
    try:
        return int(float(x))
    except:
        return x

stations_df['Stipend'] = stations_df['Stipend'].apply(format_stipend)

# Convert Date to datetime format
stations_df['ParsedDate'] = pd.to_datetime(stations_df['Date'], format="%B %dth, %Y")

@app.route('/')
def home():
    query = request.args.get('search', '').lower()
    sort_order = request.args.get('sort', '')
    filtered = stations_df.copy()

    if query:
        filtered = filtered[filtered['Station'].str.lower().str.contains(query)]

    if sort_order == 'asc':
        filtered = filtered.sort_values(by='Stipend', ascending=True)
    elif sort_order == 'desc':
        filtered = filtered.sort_values(by='Stipend', ascending=False)
    elif sort_order == 'date_asc':
        filtered = filtered.sort_values(by='ParsedDate', ascending=True)
    elif sort_order == 'date_desc':
        filtered = filtered.sort_values(by='ParsedDate', ascending=False)

    return render_template('home.html', stations=filtered.to_dict(orient='records'), query=query)

@app.route('/details/<int:station_id>')
def details(station_id):
    projects = details_df[details_df['ID'] == station_id]

    if projects.empty:
        return f"No details found for Station ID {station_id}", 404

    return render_template('details.html', projects=projects.to_dict(orient='records'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # default to 5000 if not set
    app.run(host='0.0.0.0', port=port, debug=True)
