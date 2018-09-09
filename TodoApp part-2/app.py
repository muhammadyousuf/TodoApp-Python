from flask import Flask, jsonify , json, render_template, session, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///mytodo.db'

mydb = SQLAlchemy(app)

class Mytodo(mydb.Model):
    todoId=mydb.Column(mydb.Integer , primary_key=True)
    todoTitle = mydb.Column(mydb.String(50))
    todoDes = mydb.Column(mydb.String(500))
    todoDone = mydb.Column(mydb.Boolean)



mydb.create_all()

@app.route('/todoapp/api/v1.0/yousuf' , methods=['GET'])
def get_todo_data():
    mytodo = Mytodo.query.all()

    mytodoList=[]
    for mytodos in mytodo:
        myTodoData={}
        myTodoData['id']=mytodos.todoId
        myTodoData['title']=mytodos.todoTitle
        myTodoData['description']=mytodos.todoDes
        myTodoData['done'] = mytodos.todoDone
        mytodoList.append(myTodoData)

    return jsonify({'allTodo':mytodoList})

@app.route('/todoapp/api/v1.0/yousuf/<id>', methods=['GET'])
def get_one_mytodo(id):
    mytodos = Mytodo.query.filter_by(todoId=id).first()
    if not mytodos:
        return jsonify({'result':'Id are not found'})

    myTodoData={} 
    myTodoData['id'] = mytodos.todoId
    myTodoData['title'] = mytodos.todoTitle
    myTodoData['description'] = mytodos.todoDes
    myTodoData['done'] = mytodos.todoDone
    return jsonify(myTodoData)

@app.route('/todoapp/api/v1.0/yousuf' , methods=['POST'])
def create_todo():
    data = request.get_json()

    mytodo = Mytodo(todoTitle=data['title'], todoDes=data['description'], todoDone=False)
    mydb.session.add(mytodo)
    mydb.session.commit()
    return jsonify ({'result':'Add Data sucessufully Store'})

@app.route('/todoapp/api/v1.0/yousuf/<id>', methods=['PUT'])
def update_todo(id):
    mytodo = Mytodo.query.filter_by(todoId=id).first()
    if not mytodo:
        return jsonify({'result': 'Id are not found'})
    data = request.get_json()
    mytodo.todoDone=True
    mytodo.todoTitle=data['title']
    mytodo.todoDes=data['description']
    
    myTodoData={} 
    myTodoData['id'] = mytodo.todoId
    myTodoData['title'] = mytodo.todoTitle
    myTodoData['description'] = mytodo.todoDes
    myTodoData['done'] = mytodo.todoDone
    mydb.session.commit()
    return jsonify(myTodoData)

@app.route('/todoapp/api/v1.0/yousuf/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    mytodos = Mytodo.query.filter_by(todoId=todo_id).first()
    if not mytodos:
        return jsonify({'result': 'Id are not found'})
    else:
        mydb.session.delete(mytodos)
        mydb.session.commit()
    return jsonify({'result':'Congrats Delete Data Sucessfully'})



app.run(debug=True, use_reloader=False, port=3000)