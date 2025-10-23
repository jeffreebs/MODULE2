from flask import Flask, request,jsonify
import json


app=Flask(__name__)

valid_states= ["To do", "In progress...", "Completed!!"]
tasks_file ="tasks.json"

def load_tasks():
    try:
        with open(tasks_file,"r")as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return[]
    

def save_tasks(tasks):
    with open(tasks_file, "w") as file :
        json.dump(tasks,file,indent=4)


def is_valid_task_data(data, check_id=True):
    required = ["title", "description", "state"]
    if check_id:
        required.insert(0,"id")


    for field in required:
        if not data.get(field):
            return False, f"Missing or empty field: {field}"
        

    if data["state"] not in valid_states:
        return False, f"Invalid state.Allowed:{valid_states}"
    

    return True, None

@app.route("/")
def init():
    return "Hello Lyfter Team"



@app.route("/tasks", methods= ["GET"])
def get_task():
    tasks = load_tasks()
    filter_state= request.args.get("state")


    if filter_state:
            filtered=[t for t in tasks if t.get("state", "").lower()== filter_state.lower()]
            return jsonify({
                "message": f"Filters tasks from state:{filter_state}",
                "tasks": filtered,
                "total": len(filtered)
            })
        

    return jsonify({
            "message":"All tasks get successfully",
            "tasks": tasks,
            "total":len(tasks)

        })
    


@app.route("/tasks", methods= ["POST"])
def create_task():
    data=request.get_json()
    if not data:
        return jsonify({'error': 'Not data JSON received'}), 400
            

    is_valid, error_msg = is_valid_task_data(data)
    if not is_valid:
        return jsonify({"error": error_msg}), 400
    
    tasks= load_tasks()
    if any(t["id"] == data["id"] for t in tasks):
        return jsonify({"error": f"Task with id {data['id']} already exists"}), 409

    tasks.append(data)
    save_tasks(tasks)
    

    
    


    return jsonify({
        "message": "Task created successfully",
        "task": data
    }),201


@app.route("/tasks/<int:task_id>", methods= ["PUT"])
def update_task(task_id):
    data= request.get_json()
    if not data:
        return jsonify({"Error": "Not have any data to update. "}),400
    

    if "state" in data and data ["state"] not in valid_states:
        return jsonify({"error": f"Invalid state: {data['state']}. Allowed: {valid_states}"}), 400
    

    tasks = load_tasks()
    task = next((t for t in tasks if t["id"] == task_id), None)

    if not task:
        return jsonify({"error": f"Task with id {task_id} not found"}), 404
    

    task.update(data)
    save_tasks(tasks)


    return jsonify({
        "message": "Task update successfully",
        "task": task
    })


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    tasks= load_tasks()
    task= next ((t for t in tasks if t["id"]== task_id), None)


    if not task:
        return jsonify({"error":f"The task with {task_id} was no found"}),404
    
    tasks.remove(task)
    save_tasks(tasks)


    return jsonify({"message": f"Tasks with the id {task_id} has been deleted successfully. "})




if __name__ == "__main__":
    app.run(debug=True)
    

