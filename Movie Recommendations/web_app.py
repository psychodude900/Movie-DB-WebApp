from flask import Flask, render_template, session, request, redirect, url_for
import movie_data as md
import movie_page as mp
import os
import time

app = Flask(__name__)
page_index = 0

@app.route("/", methods=["POST", "GET"])
def home():
    global page_index
    page_index = 0
    if request.method == "POST":
        search_name = request.form["search"]
        return redirect(url_for("movie_page", movie_name=search_name))
    else:
        return render_template("index.html")

@app.route("/<movie_name>", methods=["POST", "GET"])
def movie_page(movie_name):
    global page_index
    data = md.search(movie_name)
    url = mp.create_page_html(movie_name, data, page_index)
    if len(data) == 0:
        return redirect(url_for("not_found", search_name=movie_name))
    
    if request.method == "POST":
        if request.form["page-change"] == "Next":
            page_index += 1
            if page_index <= len(data) -1:
                next_url = mp.create_page_html(movie_name, data, page_index)
                return render_template(next_url)
            else:
                page_index -=1
        else:
            page_index -= 1
            if page_index < 0:
                return redirect(url_for("home"))
            prev_url = mp.create_page_html(movie_name, data, page_index)
            return render_template(prev_url)
    return render_template(url)

@app.route("/not+found")
def not_found(search_name):
    return search_name + " not found :( \n Please go back to search page."
    
        

if __name__ == "__main__":
    app.run(debug=True)
