from flask import Flask, render_template, redirect, url_for, request
from SearchElement import get_website_data, custom_detection
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
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    x_cod = db.Column(db.Integer)
    y_cod = db.Column(db.Integer)
    height = db.Column(db.Integer)
    width = db.Column(db.Integer)
    author = db.Column(db.Integer)
    img_url = db.Column(db.String(250))


class WebsiteTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    web_url = db.Column(db.String(250))


db.create_all()

@app.route('/')
def home_page():
    table_data = ElementTable.query.all()
    return render_template("home.html", table_data=table_data)

@app.route("/post/<int:element_id>")
def show_element(element_id):
    requested_element = ElementTable.query.get(element_id)
    return render_template("element.html", element=requested_element)

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

    for data in element_data:
        insert_data = ElementTable(
            name=data['name'],
            x_cod=data['x_cod'],
            y_cod=data['y_cod'],
            height=data['height'],
            width=data['width'],
            img_url=data['img_url'],
        )
        db.session.add(insert_data)
        db.session.commit()

    return redirect(url_for("home_page"))


@app.route("/delete/<int:element_id>")
def delete_element(element_id):
    element_to_delete = ElementTable.query.get(element_id)
    db.session.delete(element_to_delete)
    db.session.commit()
    return redirect(url_for('home_page'))


@app.route("/edit_element/<int:element_id>", methods=["GET", "POST"])
def edit_element(element_id):
    element = ElementTable.query.get(element_id)

    if request.method == 'POST':
        element.name = str(request.form.get('name'))
        element.width = int(request.form.get('width'))
        element.height = int(request.form.get('height'))
        element.x_cod = int(request.form.get('x_cod'))
        element.y_cod = int(request.form.get('y_cod'))

        element = custom_detection(element)
        edit_element = ElementTable(
            name=element.name,
            x_cod=element.x_cod,
            y_cod=element.y_cod,
            height=element.height,
            width=element.width,
            img_url=element.img_url,
        )
        db.session.commit()
        return redirect(url_for("show_element", element_id=element.id))
    return render_template("edit_element.html", element=element)


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000)
