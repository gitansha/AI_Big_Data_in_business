from flask import Flask
from flask import render_template, request, jsonify
import textblob
import google.generativeai as genai
import os
import markdown
import re



# api = os.getenv("makersuite")
api = 'AIzaSyCCXOIplLPvb7lvtigD68LNXgRdKUXXjso'

def get_gemini_response(question, chat):
    response = chat.send_message(question, stream = True)
    return response



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
    polarity = r.polarity
    subjectivity = r.subjectivity

    return(render_template('SA_result.html',polarity = polarity, subjectivity = subjectivity, q = q))

@app.route("/Gen_AI", methods=['GET','POST'] )
def gen_AI():
    return(render_template('Gen_AI.html'))

@app.route('/Gen_AI_result',methods=['GET','POST'])
def gen_AI_result():
    ques = request.form.get("response")
    genai.configure(api_key= api)
    model = genai.GenerativeModel("gemini-1.5-flash")
    answer= model.generate_content(ques)
    answer = markdown.markdown(answer.text)
    answer = re.sub(r'<.*?>', '', answer)
    return(render_template('Gen_AI_result.html',answer = answer))

@app.route('/Gen_AI_chatbot', methods=['GET', 'POST'])
def gen_AI_chatbot():
    if request.method == 'POST':
        try:
            # Get the initial question from the form
            initial_question = request.form.get("response")
            
            # Configure and get response from Gemini
            genai.configure(api_key=api)
            model = genai.GenerativeModel("gemini-pro")
            chat = model.start_chat(history=[])
            
            response = chat.send_message(initial_question, stream=True)
            
            full_response = ""
            for chunk in response:
                if chunk.text:
                    full_response += chunk.text
            
            answer = markdown.markdown(full_response)
            answer = re.sub(r'<.*?>', '', answer)
            
            # Render the chatbot template with the initial response
            return render_template('Gen_AI_chatbot.html', initial_message=initial_question, initial_response=answer)
            
        except Exception as e:
            return render_template('Gen_AI_chatbot.html', error=str(e))
    
    # For GET requests, just render the chatbot interface
    return render_template('Gen_AI_chatbot.html')

# Route for handling chat messages via AJAX
@app.route('/chat_message', methods=['POST'])
def chat_message():
    try:
        ques = request.form.get("response")
        genai.configure(api_key=api)
        model = genai.GenerativeModel("gemini-pro")
        chat = model.start_chat(history=[])
        
        response = chat.send_message(ques, stream=True)
        
        full_response = ""
        for chunk in response:
            if chunk.text:
                full_response += chunk.text
        
        answer = markdown.markdown(full_response)
        answer = re.sub(r'<.*?>', '', answer)
        
        return jsonify({'answer': answer})
        
    except Exception as e:
        return jsonify({'answer': f"Error: {str(e)}"})

@app.route("/paynow", methods=['GET','POST'] )
def paynow():
    return(render_template('paynow.html'))


if __name__ == "__main__":
    app.run(port = 1111)