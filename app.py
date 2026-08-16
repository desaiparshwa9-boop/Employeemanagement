from flask import Flask, render_template, request, redirect
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection
client = MongoClient("mongodb://mongodb:27017/")
db = client["employee_db"]
employees = db["employees"]


@app.route("/")
def home():
    employee_list = list(employees.find())
    return render_template("index.html", employees=employee_list)


@app.route("/add", methods=["POST"])
def add_employee():
    employee = {
        "name": request.form["name"],
        "employee_id": request.form["employee_id"],
        "department": request.form["department"],
        "email": request.form["email"],
        "salary": request.form["salary"]
    }

    employees.insert_one(employee)

    return redirect("/")


@app.route("/delete/<employee_id>")
def delete_employee(employee_id):
    employees.delete_one({"employee_id": employee_id})
    return redirect("/")
@app.route("/edit/<employee_id>", methods=["GET", "POST"])
def edit_employee(employee_id):

    employee = employees.find_one({"employee_id": employee_id})

    if request.method == "POST":

        updated_employee = {
            "name": request.form["name"],
            "employee_id": request.form["employee_id"],
            "department": request.form["department"],
            "email": request.form["email"],
            "salary": request.form["salary"]
        }

        employees.update_one(
            {"employee_id": employee_id},
            {"$set": updated_employee}
        )

        return redirect("/")

    return render_template("edit.html", employee=employee)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)