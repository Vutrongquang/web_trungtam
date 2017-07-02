import os
from flask import *
import mlab
from mongoengine import *
from werkzeug.utils import secure_filename

app = Flask(__name__)
mlab.connect()

app.config["IMG_PATH"] = os.path.join(app.root_path, "images")

class Course(Document):
    image = StringField()
    title = StringField()
    price = FloatField()

# course1 = Course(image = "https://www.gohacking.com/wp-content/uploads/2015/02/learn-how-to-hack-735x400.jpg",
#                  title = "Hack",
#                  price = 350000000)

# course1.save()

image = "http://hourofcode.vn/wp-content/uploads/2015/10/HOUROFCODE.VN_.jpg"
title = "Hour of code"
price = 150000000

courses  = [
    {"image" : "http://hourofcode.vn/wp-content/uploads/2015/10/HOUROFCODE.VN_.jpg",
     "title": "Hour of code",
     "price": 150000000

},
    {"image" : "https://lh3.googleusercontent.com/4bv-VZSXu2vJyhNQaeU5Uq4tGWTq7s1qwJQfKU4JhGvkmNEyFSKwSrKdekcpXHjIFiTQ=h556",
     "title": "Code",
     "price": 250000000
    },

    {"image" : "https://www.gohacking.com/wp-content/uploads/2015/02/learn-how-to-hack-735x400.jpg",
     "title": "Hack",
     "price": 350000000


    }]

@app.route('/')
def index():
    return render_template("index.html", courses = Course.objects() )

@app.route("/images/<image_name>")
def image(image_name):
    return  send_from_directory(app.config["IMG_PATH"], image_name)

@app.route("/about")
def about():
    return "Hi, welcome to Zipo's page"


@app.route("/add_course", methods=["GET","POST"])
def add_course():
    if request.method == "GET":
        return render_template("add_course.html" )
    elif request.method == "POST":
        #1 Get data

        form = request.form
        title = form["title"]
        price = form["price"]

        image = request.files["image"]

        filename = secure_filename(image.filename)

        image.save(os.path.join(app.config["IMG_PATH"], filename))

        #2 Save int
        new_course = Course(title = title,
                            image = "/images/{0}".format(filename),
                            price = price)
        new_course.save()
        return redirect(url_for("index"))

@app.route("/users/<username>")
def user(username):
    return "Hello, my name is "+ username + ", welcome to my page"

@app.route("/add/<int:a>/<int:b>")
def add(a, b):

    return "{0} + {1} = {2}".format(a,b, a+b)

if __name__ == '__main__':
    app.run()
