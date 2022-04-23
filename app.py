from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
import models

app = Flask(__name__)
# SqlAlchemy Database Configuration With Mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/flask_project'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)


# REST - simple get post for Todos Table
class TodosResource(Resource):
    def get(self):
        dict1 = {}
        ret = models.ToDoTable.query.all()
        for i in ret:
            dict1["sno"] = i.sno
            dict1["title"] = i.title
            dict1['desc'] = i.desc

        # 200 in return represent status code(in case of failure return 400..)
        return dict1, 200

    def post(self):
        rec1 = models.ToDoTable(sno=1, title='To build new API',
                                desc="To have GET/POST endpoints for my API")
        db.session.add(rec1)
        db.session.commit()
        return "data added", 200


api.add_resource(TodosResource, '/todos')


# REST - GET, POST, PUT with URL req parameters for Students table
class StudentsResource(Resource):
    def get(self):
        studentsData = {}
        ret = models.Students.query.all()
        for i in ret:
            dict1 = {}
            dict1["S.No"] = i.sno
            dict1["First Name"] = i.firstName
            dict1['Last Name'] = i.lastName
            dict1["age"] = i.age
            studentsData[i.firstName] = dict1
        return studentsData, 200

    # e.g - http://127.0.0.1:5000/students?firstName=Rocky&lastName=Bhai&age=42
    def post(self):
        studentData = models.Students(firstName=request.args.get(
            'firstName'), lastName=request.args.get("lastName"), age=request.args.get("age"))
        db.session.add(studentData)
        db.session.commit()
        return "Data added", 200

    def put(self):
        studentData = models.Students.query.filter_by(
            firstName=request.args.get("firstName")).first()
        updated_age = request.form.get('age')
        studentData.age = updated_age
        current_db_sessions = db.session.object_session(studentData)
        current_db_sessions.add(studentData)
        current_db_sessions.commit()
        return "Data updated", 200


api.add_resource(StudentsResource, '/students')


# use request.form for fetching body params and request.args for fetching URL params
# REST - GET, POST, DELETE with form data/request body for students table
class StudentsFormBodyResource(Resource):
    def get(self):
        studentsData = {}
        ret = models.Students.query.all()
        for i in ret:
            dict1 = {}
            dict1["S.No"] = i.sno
            dict1["First Name"] = i.firstName
            dict1['Last Name'] = i.lastName
            dict1["age"] = i.age
            studentsData[i.firstName] = dict1
        return studentsData, 200

    # e.g - http://127.0.0.1:5000/students?firstName=Rocky&lastName=Bhai&age=42
    def post(self):
        studentData = models.Students(firstName=request.form.get(
            'firstName'), lastName=request.form.get("lastName"), age=request.form.get("age"))
        db.session.add(studentData)
        db.session.commit()
        return "Data added", 200

    def delete(self):
        studentData = models.Students.query.filter_by(
            firstName=request.args.get('firstName')).first()
        if studentData == None:
            return "Student data does not exists", 400
        else:
            current_db_sessions = db.session.object_session(studentData)
            current_db_sessions.delete(studentData)
            current_db_sessions.commit()
            return "Student data deleted", 200


api.add_resource(StudentsFormBodyResource, '/studentsform')


# simple html page render way
@app.route("/")
def hello_world():
    return render_template('index.html')


# returning plain text
@app.route("/getAllTodos")
def getAllTodos():
    return "Hello My Todos"


if __name__ == "__main__":
    app.run(debug=True)
