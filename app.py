from flask import Flask
from flask import render_template, request
import textblob
import google.generativeai as genai
import os

api = os.getenv("makersuite")

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
    r = textblob.TextBlob(q).sentiment

    return(render_template('SA_result.html',r=r))

@app.route("/Gen_AI", methods=['GET','POST'] )
def gen_AI():
    return(render_template('Gen_AI.html'))

@app.route('/Gen_AI_result',methods=['GET','POST'])
def gen_AI_result():
    ques = request.form.get("response")
    genai.configure(api_key= api)
    model = genai.GenerativeModel("gemini-1.5-flash")
    answer= model.generate_content(ques)
    answer = answer.text
    # from IPython.display import Markdown
    # answer = display(Markdown(response.text))
    return(render_template('Gen_AI_result.html',answer = answer))



if __name__ == "__main__":
    app.run(port = 1111)