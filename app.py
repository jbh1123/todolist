from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

@app.route("/")
def todo():
    return render_template("index.html")

'''
@app.route("/logtask", methods=['POST'])
def logtask():
    data = request.get_json()
    with open('tasks_log.txt', 'a') as log:
'''

app.run(debug=True)