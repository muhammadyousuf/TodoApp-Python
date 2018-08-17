from flask import Flask, render_template, request, redirect, url_for, jsonify, json
from flask_pymongo import PyMongo
from flask_bootstrap import Bootstrap
from bson.objectid import ObjectId
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
bootstrap = Bootstrap(app)


app.config['MONGO_DBNAME'] = 'axiom'
app.config['MONGO_URI'] = 'mongodb://todoapp:todo123@ds119422.mlab.com:19422/axiom'
mongo = PyMongo(app)


class NameForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = StringField('Description')
    submit = SubmitField('Submit')


@app.route("/todoapp/api/v1.0/yousuf", methods=['GET'])
def index():
    form = NameForm()

    return render_template('index.html', form=form)


@app.route("/favicon.ico")
def fav():
    return "no fav"


@app.route("/todoapp/api/v1.0/yousuf/todoList", methods=['GET'])
def todoList():
    todos = mongo.db.todoapp.find()
    return render_template('todoList.html', todos=todos)

@app.route("/todoapp/api/v1.0/yousuf/update/<id>", methods=['GET'])
def update(id):
    todos = mongo.db.todoapp.find_one({"_id": ObjectId(id)})
   
    

    return render_template('update.html', todos=todos,id=id)


@app.route("/todoapp/api/v1.0/yousuf", methods=['POST', 'GET'])
def add():
    form = NameForm()
    if form.validate_on_submit():
        users = mongo.db.todoapp
        done = bool(form.description.data and form.title.data)
        save = [{'title': form.title.data,
                 'description': form.description.data, 'done': done}]
        users.insert(save)
        return redirect(url_for('index'))
    return render_template('index.html', form=form)


@app.route("/todoapp/api/v1.0/yousuf/<id>")
def delete(id):
    users = mongo.db.todoapp
    uid = users.find_one({"_id": ObjectId(id)})
    users.remove(uid, True)
    return redirect(url_for('todoList'))


@app.route("/todoapp/api/v1.0/yousuf/up/<id>", methods=['POST'])
def edit(id):
    users = mongo.db.todoapp
    uid = users.find_one({"_id": ObjectId(id)})
    newtodotitle = request.form['updatetitle']
    newtoDescription = request.form['updateDescription']
    #done=bool(request.form['title'] and request.form['description'])

    uid['title'] = newtodotitle
    uid['description'] = newtoDescription
    uid['done'] = True
    users.save(uid)
    return redirect(url_for('todoList'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route("/todoapp/api/v1.0/yousuf/taskDone")
def api():
    dbAllData = mongo.db.todoapp.find()
    allUsers = []
    for title in dbAllData:
        allUsers.append(
            {'title': title['title'], 'description': title['description'], 'done': title['done']})

    return jsonify({"todo": allUsers})


app.run(debug=True, use_reloader=False, port=2000)
