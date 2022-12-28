from flask import Flask, render_template, redirect, url_for, request
from SearchElement import get_website_data, custom_detection
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from types import SimpleNamespace
import json


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///web_scanning.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##CONFIGURE TABLE
class ElementTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    main_name = db.Column(db.String(250))
    x_cod = db.Column(db.Integer)
    y_cod = db.Column(db.Integer)
    height = db.Column(db.Integer)
    width = db.Column(db.Integer)
    img_url = db.Column(db.String(250))
    website = db.Column(db.String(300))


db.create_all()

website_url = None


@app.route('/')
def home_page():
    print("home website = ", website_url)
    table_data = []
    if website_url:
        table_data = ElementTable.query.filter_by(website=website_url[12:17]).all()
    return render_template("home.html", table_data=table_data, website_url=website_url)


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
    global website_url
    website_url = request.form.get("website_url")
    if not website_url:
        return render_template("home.html", table_data=[], website_url=website_url)

    table_data = ElementTable.query.filter_by(website=website_url[12:17]).all()
    if not table_data:
        element_data = get_website_data(website_url)
        for data in element_data:
            insert_data = ElementTable(
                name=data['name'],
                main_name=data['main_name'],
                x_cod=data['x_cod'],
                y_cod=data['y_cod'],
                height=data['height'],
                width=data['width'],
                img_url=data['img_url'],
                website=website_url[12:12+5],
            )
            db.session.add(insert_data)
            db.session.commit()
            table_data = ElementTable.query.filter_by(website=website_url[12:17]).all()

    return render_template("home.html", table_data=table_data, website_url=website_url)


@app.route("/delete/<int:element_id>")
def delete_element(element_id):
    element_to_delete = ElementTable.query.get(element_id)
    db.session.delete(element_to_delete)
    db.session.commit()
    print("del website = ", website_url)
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
        element.main_name = str(request.form.get('main_name'))

        element = custom_detection(element, element.website)
        edit_element = ElementTable(
            name=element.name,
            main_name=element.main_name,
            x_cod=element.x_cod,
            y_cod=element.y_cod,
            height=element.height,
            width=element.width,
            img_url=element.img_url,
            website=element.website,
        )
        db.session.commit()
        return redirect(url_for("show_element", element_id=element.id))
    return render_template("edit_element.html", element=element, is_edit=True)


@app.route("/new_element", methods=["GET", "POST"])
def add_new_element():
    if request.method == 'POST':
        is_exit = ElementTable.query.filter_by(name=request.form.get('name')).all()
        if is_exit:
            return render_template("edit_element.html", element=is_exit, is_edit=False, present=True)

        element = dict()
        element['name'] = str(request.form.get('name'))
        element['width'] = int(request.form.get('width'))
        element['height'] = int(request.form.get('height'))
        element['x_cod'] = int(request.form.get('x_cod'))
        element['y_cod'] = int(request.form.get('y_cod'))
        element['img_url'] = ""
        element['website'] = website_url[12:17]
        element['main_name'] = ""


        element = SimpleNamespace(**element)
        modi_element = custom_detection(element, website_url[12:17])

        new_element = ElementTable(
            name=modi_element.name,
            main_name=modi_element.main_name,
            x_cod=modi_element.x_cod,
            y_cod=modi_element.y_cod,
            height=modi_element.height,
            width=modi_element.width,
            img_url=modi_element.img_url,
            website=modi_element.website,
            )
        db.session.add(new_element)
        db.session.commit()
        return redirect(url_for("home_page"))

    element = {
        'name': "",
        'x_cod': 0,
        'y_cod': 0,
        'height': 0,
        'width': 0,
        'img_url': "",
        "website": website_url[12:17],
        "main_name": ""
    }
    return render_template("edit_element.html", element=element, is_edit=False)


@app.route("/web-control-api/<url>", methods=["GET", "POST"])
def create_api(url):
    table_data = ElementTable.query.filter_by(website=url).all()
    json_element = []
    if len(table_data) != 0:
        for data in table_data:
            json_element.append({
                'name': data.name,
                'main_name': data.main_name,
                'x_cod': data.x_cod,
                'y_cod': data.y_cod,
                'height': data.height,
                'width': data.width,
                'img_url': data.img_url,
                "website": data.website,
            })
    else:
        json_element.append({
            'error': 'This website data does not exist',
            'statusCode': 404,
        })

    return json.dumps(json_element)


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000)
