import openai
from flask import Flask, render_template, request, jsonify
from config import API_KEY

app = Flask(__name__)

openai.api_key = API_KEY

messages = [{"role": "system", "content": "You are an assistant that provides detailed explanations of various subjects, with 3 multiple choice questions that follows the explanation, and after you give the multiple choice questions, you will give the answers to the multiple choice questions in list form."}]

def CustomChatGPT(user_input):
    messages.append({"role": "user", "content": f"Explain, in detail, {user_input} and give me 3 multiple choice questions that follows the explanation, and after you give the multiple choice questions, you will give the answers to the multiple choice questions in list form."})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=1000  # Limit response length to save API usage
    )
    ChatGPT_reply = response["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": ChatGPT_reply})
    return ChatGPT_reply

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.form['user_input']
    response = CustomChatGPT(user_input)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
