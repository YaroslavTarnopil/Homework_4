from flask import Flask, render_template, request, redirect, url_for
import socket
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/message')
def message():
    return render_template('message.html')

@app.route('/submit_message', methods=['POST'])
def submit_message():
    message = request.form['message']
    data = {'message': message}
    
    # Надсилаємо повідомлення Socket серверу
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('localhost', 5000)
    sock.sendto(json.dumps(data).encode(), server_address)
    sock.close()
    
    return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404

if __name__ == '__main__':
    app.run(port=3000)
