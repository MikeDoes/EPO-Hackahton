from flask import Flask, render_template

app = Flask(__name__,  
static_folder='static',
)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/search_results")
def search_results():
    return render_template('search_results.html')

@app.route("/patent/<patent_no>")
def display_patent(patent_no):
    return render_template('patent.html', data=patent_no)