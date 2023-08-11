from flask import Flask, render_template, request
from quickstart import Update_Sequence
from time import sleep

app = Flask(__name__)


@app.route('/')
def dynamicindex():
    Update_Sequence()
    return render_template('dynamicindex.html')


if __name__ == '__main__':
    app.run(debug=True,port = 8000)
