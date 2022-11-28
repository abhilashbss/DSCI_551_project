from flask import Flask, render_template
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


# EDFS Client

@app.route('/command', methods=['POST'])
def command():
    command = request.form['command']
    commandOutput = edfs_client_processor(command).process_command()
    print(commandOutput)
    return render_template('index.html', command_output = commandOutput )
# Map Reduce


if __name__ == '__main__':
    app.run()