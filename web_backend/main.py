from flask import Flask, render_template, redirect, url_for, jsonify
from edfs_client_processor import edfs_client_processor
from flask import request

app = Flask(__name__)
global edfs_cl_processor
# Basic

@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/search.html')
def search():
    return render_template('search.html')

@app.route('/analytics.html')
def analytics():
    return render_template('analytics.html')

global cd
cd = ""
global db_selected
db_selected="firebase"

@app.route('/directory_tree.html')
def directory_tree():
    global edfs_cl_processor
    contents = edfs_cl_processor.get_directory_contents(cd)
    return render_template('directory_tree.html', contents = contents ,current_directory = cd)

@app.route('/db_selection', methods=['POST'])
def db_selection():
    global edfs_cl_processor
    edfs_cl_processor = edfs_client_processor(request.form['db_type'])
    return jsonify(message='success')


@app.route('/directory_tree_parse',methods=['GET'])
def directory_tree_parse():
    cd = request.args["cur_dir"]
    print(cd)
    global edfs_cl_processor
    contents = edfs_cl_processor.get_directory_contents(cd)
    return render_template('directory_tree.html', contents = contents ,current_directory = cd)


@app.route('/directory_tree_back',methods=['GET'])
def directory_tree_back():
    cd = request.args["cur_dir"]
    cd = "/".join(cd.split("/")[:-1])
    global edfs_cl_processor
    contents = edfs_cl_processor.get_directory_contents(cd)
    return render_template('directory_tree.html', contents = contents ,current_directory = cd)



# EDFS Client

@app.route('/command', methods=['POST'])
def command():
    command = request.form['command']
    global edfs_cl_processor
    commandOutput = edfs_cl_processor.process_edfs_command(command)
    print(commandOutput)
    return render_template('index.html', command_output = commandOutput )
# Map Reduce


if __name__ == '__main__':
    app.run()