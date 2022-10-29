from flask import Flask, render_template, redirect, url_for, request
from SearchElement import get_website_data
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///web_element.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##CONFIGURE TABLE
class ElementTable(db.Model):
    name = db.Column(db.Float)
    x_cod = db.Column(db.String(250))
    y_cod = db.Column(db.String(250))
    height = db.Column(db.String(250))
    width = db.Column(db.Text)
    author = db.Column(db.String(250))
    img_url = db.Column(db.String(250))
# db.create_all()



@app.route('/')
def home_page(table_data):
    table_data = []
    return render_template("home.html", table_data=table_data)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/Team")
def contact():
    return render_template("team.html")


@app.route("/", methods=["POST"])
def get_website_url():
    website_url = request.form.get("website_url")
    element_data = get_website_data(website_url)
    print("website url", website_url)
    print("web elements data = ", element_data)



    return redirect(url_for("home_page"))


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000)
