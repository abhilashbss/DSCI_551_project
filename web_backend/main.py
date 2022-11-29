from flask import Flask, render_template, redirect, url_for
from edfs_client_processor import edfs_client_processor
from flask import request

app = Flask(__name__)

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


@app.route('/directory_tree.html')
def directory_tree():
    contents = edfs_client_processor(None).get_directory_contents(cd)
    return render_template('directory_tree.html', contents = contents ,current_directory = cd)


@app.route('/directory_tree_parse',methods=['GET'])
def directory_tree_parse():
    cd = request.args["cur_dir"]
    print(cd)
    contents = edfs_client_processor(None).get_directory_contents(cd)
    return render_template('directory_tree.html', contents = contents ,current_directory = cd)


@app.route('/directory_tree_back',methods=['GET'])
def directory_tree_back():
    cd = request.args["cur_dir"]
    cd = "/".join(cd.split("/")[:-1])
    contents = edfs_client_processor(None).get_directory_contents(cd)
    return render_template('directory_tree.html', contents = contents ,current_directory = cd)



# EDFS Client

@app.route('/command', methods=['POST'])
def command():
    command = request.form['command']
    commandOutput = edfs_client_processor(command).process_edfs_command()
    print(commandOutput)
    return render_template('index.html', command_output = commandOutput )
# Map Reduce


if __name__ == '__main__':
    app.run()