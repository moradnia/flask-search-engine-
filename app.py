from flask import Flask, render_template, request,redirect,url_for
from elasticsearch import Elasticsearch

app = Flask(__name__)
es = Elasticsearch('http://localhost', port=9200)
# es=Elasticsearch()


@app.route('/')
def index():
    return render_template('index.html')
@app.route('/voice')
def voice():
    return render_template('voice.html')


@app.route('/search')
def home():
    return render_template('search.html')

@app.route('/search/results', methods=['GET', 'POST'])
def search_request():
    search_term = request.form["input"]
    res = es.search(
        index="imdb", 
        size=20, 
        body={
            "query": {
                "multi_match" : {
                    "query": search_term, 
                    "fields": [
                        "name", 
                        "years",
                        "href",
                        "plot",
                        "budge",
                        "src_image",
                        'director',
                        'stars',
                    ] 
                }
            }
        }
    )
    return render_template('results.html', res=res )

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(host='0.0.0.0', port=5000)