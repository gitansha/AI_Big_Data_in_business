from flask import Flask
from flask import render_template, request

app = Flask(__name__)


@app.route('/',methods=['GET','POST'])
def index():
    return(render_template('index.html'))


@app.route('/main',methods=['GET','POST'])
def main():
    name = request.form.get("uname")
    return(render_template('main.html'))

@app.route("/SA", methods=['GET','POST'] )
def sa():
    return(render_template('SA.html'))

@app.route('/SA_result',methods=['GET','POST'])
def sa_result():
    q = request.form.get("q")
    r = 

    return(render_template('sa_rwsult.html'))



if __name__ == "__main__":
    app.run(port = 1111)