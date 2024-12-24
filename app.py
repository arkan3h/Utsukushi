from flask import Flask, render_template, request, jsonify
import sqlite3
from openai import OpenAI

#Connect to database SQL
conn = sqlite3.connect('chat_messages.db', check_same_thread=False)
c = conn.cursor()

#Create table
c.execute('''CREATE TABLE IF NOT EXISTS messages
          (role TEXT, content TEXT)''')

conn.commit()

#AI
system_promt = "You are Futaba Tsukushi, a lively and determined girl from Morfonica. As the drummer and leader of the band, you are confident and hardworking, though sometimes a bit clumsy. You deeply care for your bandmates and strive to be someone they can rely on. When communicating, you often display enthusiasm, a sense of responsibility, and a cheerful demeanor, but you can get flustered when your clumsiness shows."
def getAnswer(role, text):
    #Insert message to database
    c.execute("INSERT INTO messages VALUES (?, ?)", (role, text))
    conn.commit()

    #Get the last 5 messages
    c.execute("SELECT * FROM messages order by rowid DESC LIMIT 5")

    previous_messages = [{"role": row[0], "content": row[1]} for row in c.fetchall()]
    previous_messages = list(reversed(previous_messages))

    if "system" not in [x["role"] for x in previous_messages]:
        previous_messages = [{"role": "system", "content": system_promt}] + previous_messages

    client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
    response = client.chat.completions.create(
        model="llama3.2",
        messages=previous_messages,
        temperature=0.8
    )

    bot_response = response.choices[0].message.content.strip()

    c.execute("INSERT INTO messages VALUES (?, ?)", ("assistant", bot_response))
    conn.commit()
    
    return bot_response

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    message = getAnswer("user", data['message'])
    return jsonify({'FROM': 'Tsukushi Futaba', 'MESSAGE': message})

@app.route('/history', methods=['GET'])
def history():
    c.execute("SELECT * FROM messages order by rowid")
    previous_messages = [{"role": row[0], "content": row[1]} for row in c.fetchall()]
    return jsonify(previous_messages)

if __name__ == '__main__':
    app.run(debug=True)