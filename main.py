import os
import json
import socket
import threading
from datetime import datetime
from flask import Flask, request, send_from_directory, render_template_string
import socketserver  # Додаємо необхідний імпорт

app = Flask(__name__)

# Маршрутизація для HTML сторінок
@app.route('/')
def index():
    return render_template_string(open('templates/index.html').read())

@app.route('/message', methods=['GET', 'POST'])
def message():
    if request.method == 'POST':
        username = request.form['username']
        message = request.form['message']
        send_to_socket_server({'username': username, 'message': message})
        return 'Message sent!'
    return render_template_string(open('templates/message.html').read())

# Статичні ресурси
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

# Обробка помилки 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template_string(open('templates/error.html').read()), 404

# Функція для відправки даних на Socket сервер
def send_to_socket_server(data):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(json.dumps(data).encode(), ('localhost', 5000))

# Функція для запуску Flask серверу
def run_flask():
    app.run(port=3000)

# Socket сервер для обробки повідомлень
class UDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request[0].strip()
        message = json.loads(data.decode())
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        save_message(timestamp, message)

def save_message(timestamp, message):
    if not os.path.exists('storage'):
        os.makedirs('storage')
    filepath = 'storage/data.json'
    if os.path.exists(filepath):
        with open(filepath, 'r') as file:
            data = json.load(file)
    else:
        data = {}
    data[timestamp] = message
    with open(filepath, 'w') as file:
        json.dump(data, file, indent=4)

def run_socket_server():
    server = socketserver.UDPServer(('localhost', 5000), UDPHandler)
    server.serve_forever()

if __name__ == '__main__':
    flask_thread = threading.Thread(target=run_flask)
    socket_thread = threading.Thread(target=run_socket_server)
    
    flask_thread.start()
    socket_thread.start()
    
    flask_thread.join()
    socket_thread.join()
