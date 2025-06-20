from flask import Flask, render_template, redirect, url_for, jsonify, request
import flask_ngrok, duckdb, FlagEmbedding, dateutil
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from duckdb.typing import VARCHAR, FLOAT
from flask_caching import Cache

from user import User, users
from constants import specialty_queries
from db import basic_query
from update import update

app = Flask(__name__)
# login configs
app.secret_key = "MXt9mp8qaCFg9p8j1eiGI21A$"
login_manager = LoginManager()
login_manager.init_app(app)
# server configs
flask_ngrok.run_with_ngrok(app)
# cache configs
app.config['CACHE_TYPE'] = 'SimpleCache'
app.config['CACHE_DEFAULT_TIMEOUT'] = 300
cache = Cache(app)
# database configs
conn = duckdb.connect()
model = FlagEmbedding.BGEM3FlagModel('BAAI/bge-m3', use_fp16=True)
conn.execute("""
CREATE TABLE embedded_documents
AS SELECT *
FROM read_csv('C:\\Users\\trich6\\Desktop\\rehab-frontend\\embedded_documents.csv', header=True)
""")
conn.create_function("vectorize",
                lambda sentence: model.encode(sentence)["dense_vecs"],
                [VARCHAR], 'FLOAT[1024]')
# scheduler configs & startup
# logging.basicConfig(level=logging.INFO)
# scheduler = BackgroundScheduler()
# trigger = CronTrigger(day=15, hour=2, minute=0)
# scheduler.add_job(update, trigger)
# scheduler.start()


@login_manager.user_loader
def load_user(user_id):
    if user_id in users:
        return User(user_id)

@app.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("homepage"))
    else: return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("homepage"))
    else:
        if request.method == "POST":
            username = request.form["username"]
            pw = request.form["password"]
            if username in users and users[username]["password"] == pw:
                user = User(username)
                login_user(user)
                return redirect(url_for("homepage"))
            else: return "Invalid credentials"
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))
                
@app.route("/homepage")
@login_required
def homepage():
    return render_template('home.html', specialties=specialty_queries)

# pull rows from csv based on vector similarity
@app.route("/search", methods=["POST", "GET"])
@login_required
def search():
    user_query = request.args.get('query')
    results = basic_query(conn, model, user_query)
    cache.set(f'search_results_{user_query}', results)
    cache.set('query', user_query)    
    return search_page_router(1)

# routing of pagination to enable dynamic sorting
@app.route("/search/page/<int:page>")
@login_required
def search_page_router(page):
    order_criteria = request.args.get("sort_criteria", 'similarity')
    order_asc = request.args.get("ascend", 'DESC')
    return search_page(page, order_criteria, order_asc)

# pagination of results
def search_page(page, order_criteria, order_asc):
    user_query = cache.get('query')
    results = cache.get(f"search_results_{user_query}")

    if results is None:
        results = basic_query(conn, model, user_query)
        cache.set(f"search_results_{user_query}", results)
        
    if order_criteria == "due_date":
        results.sort(key=lambda x: dateutil.parser.parse(x[3]),
                    reverse=True if order_asc == "DESC" else False)
    else:
        results.sort(key=lambda x: float(x[1]),
                    reverse=True if order_asc == "DESC" else False)
   
    per_page = 25
    start = (page - 1) * per_page
    end = start + per_page
    paginated_results = results[start:end]
    total_pages = (len(results) + per_page + 1) // per_page
    return render_template('search_results.html',
                           query=user_query,
                           length=len(results),
                           results=paginated_results,
                           total_pages=total_pages)

if __name__ == "__main__":
    app.run()
