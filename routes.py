from flask import Blueprint, request, render_template, redirect, url_for, make_response
from flask_login import login_user, login_required, logout_user, current_user
import dateutil, csv, io

from db import basic_query, get_db
from constants import specialty_queries
from extensions import cache, login_manager
from user import User, users

bp = Blueprint('main', __name__)

#################################
#       LOGIN MANAGEMENT        #
#################################

# checks login credentials of attempting user
@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.homepage"))
    else:
        if request.method == "POST":
            username = request.form["username"]
            pw = request.form["password"]
            if username in users and users[username]["password"] == pw:
                user = User(username)
                login_user(user)
                return redirect(url_for("main.homepage"))
            else: return "Invalid credentials", 401
    return render_template("login.html")

# logs out user
@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.login"))

# homepage route upon starting app
@bp.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("main.homepage"))
    else: return redirect(url_for("main.login"))

# landing page after successful login                 
@bp.route("/homepage")
@login_required
def homepage():
    return render_template('home.html', specialties=specialty_queries)

#################################
#  BEGIN SEARCH PAGE FUNCTIONS  #
#################################

# pull rows from db based on vector similarity
@bp.route("/search", methods=["POST", "GET"])
@login_required
def search():
    conn = get_db()
    user_query = request.args.get('query')
    results = basic_query(conn, user_query)
    display = request.args.get('display')
    
    cache.set(f'search_results_{user_query}', results)
    cache.set('query', user_query)
    cache.set('display', display)
    return search_page_router(1)

# routing of pagination to enable dynamic sorting
@bp.route("/search/page/<int:page>")
@login_required
def search_page_router(page):
    order_criteria = request.args.get("sort_criteria", 'similarity')
    order_asc = request.args.get("ascend", 'DESC')
    show_trials = request.args.get("show_trials", "true")
    show_trials = show_trials.lower() in ("1", "true")
    return search_page(page, order_criteria, order_asc, show_trials)

# pagination & dynamic sorting of results
def search_page(page, order_criteria, order_asc, show_trials):
    conn = get_db()
    per_page = 25
    user_query = cache.get('query')
    results = cache.get(f"search_results_{user_query}")
    display = cache.get('display')

    # regenerate results if cache has expired
    if results is None:
        results = basic_query(conn, user_query)
        cache.set(f"search_results_{user_query}", results)

    # filter & re-order based on updated sort criteria from user
    if not show_trials:
        results = [row for row in results if row[6]]
        total_pages = (len(results) + per_page + 1) // per_page
    
    if order_criteria == "due_date":
        results.sort(key=lambda x: dateutil.parser.parse(x[3]),
                    reverse=(order_asc == "DESC"))
        total_pages = (len(results) + per_page + 1) // per_page
    else:
        results.sort(key=lambda x: float(x[4]),
                    reverse=(order_asc == "DESC"))
        total_pages = (len(results) + per_page + 1) // per_page


    # paginate newly-sorted search results
    start = (page - 1) * per_page
    end = start + per_page
    paginated_results = results[start:end]
    return render_template('search_results.html',
                           query=user_query,
                           display=display,
                           show_trials=show_trials,
                           length=len(results),
                           results=paginated_results,
                           total_pages=total_pages)

# export current search results to CSV
@bp.route('/search/export')
@login_required
def export_csv():
    user_query = request.args.get('query')
    display = request.args.get('display')
    order_criteria = request.args.get("sort_criteria", 'similarity')
    order_asc = request.args.get("ascend", 'DESC')
    show_trials = request.args.get("show_trials", "true")
    show_trials = show_trials.lower() in ("1", "true")
    
    results = basic_query(get_db(), user_query)
    
    if not show_trials:
        results = [row for row in results if row[6]]

    if order_criteria == "due_date":
        results.sort(key=lambda x: dateutil.parser.parse(x[3]),
                     reverse=(order_asc == "DESC"))
    else:
        results.sort(key=lambda x: float(x[4]),
                     reverse=(order_asc == "DESC"))

    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(['Award Name', 'Organization', 'Due Date',
                     'Brief Description', 'Link', 'isGrant'])
    for row in results:
        writer.writerow([
            row[0], row[1], row[3], row[2], row[5], row[6]
            ])

    filename = display if (display is not None) else query
    response = make_response(buffer.getvalue())
    response.headers["Content-Disposition"] = f"attachment; filename=search_{filename}.csv"
    response.headers["Content-Type"] = "text/csv"
    return response
