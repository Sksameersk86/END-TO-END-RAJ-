import requests
import json
import time
import os
import threading
from platform import system
import http.server
import socketserver
import random

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"MR PRINCE SERVER ACTIVE")

def execute_server():
    PORT = int(os.environ.get('PORT', 4000))
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print("Server running at http://localhost:{}".format(PORT))
        httpd.serve_forever()

def generate_e2ee_headers(token):
    """Generate headers for E2EE Messenger requests"""
    return {
        'Authorization': f'Bearer {token}',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; Pixel 3 Build/QQ3A.200805.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/85.0.4183.81 Mobile Safari/537.36 [FBAN/MessengerLite;FBAV/258.0.0.16.124;FBBV/258013416;FBDM/{density=2.75,width=1080,height=2028};FBLC/en_US;FBRV/0;FBCR/AT&T;FBMF/Google;FBBD/Google;FBPN/com.facebook.mlite;FBDV/Pixel 3;FBSV/10;FBOP/1;FBCA/arm64-v8a:;]',
        'Content-Type': 'application/json',
        'X-FB-Friendly-Name': 'sendMessage',
        'X-FB-Connection-Type': 'mobile.LTE',
        'X-FB-MSGR-Region': 'ATN',
        'X-FB-Request-Analytics-Tags': 'graphservice',
        'X-FB-Sim-HNI': '310260',
        'X-FB-Device-ID': f"n{random.randint(10**15, 10**16)}",
        'X-FB-Connection-Quality': 'EXCELLENT',
    }

def send_e2ee_message(token, thread_id, message):
    """Send an end-to-end encrypted message through Messenger"""
    url = f"https://graph.facebook.com/v17.0/me/messages"
    
    payload = {
        "recipient": {"id": thread_id},
        "message": {"text": message},
        "messaging_type": "MESSAGE_TAG",
        "tag": "NON_PROMOTIONAL_SUBSCRIPTION"
    }
    
    try:
        response = requests.post(
            url,
            headers=generate_e2ee_headers(token),
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, response.json()
    except Exception as e:
        return False, str(e)

def send_initial_message():
    with open('token.txt', 'r') as file:
        tokens = file.readlines()

    target_id = "100064267823693"  # Replace with your target thread ID
    msg_template = "Hello Prince sir! I am using your E2EE server. My token ending with: {}"

    for token in tokens:
        access_token = token.strip()
        short_token = access_token[-6:]  # Show only last 6 chars for security
        msg = msg_template.format(short_token)
        
        success, response = send_e2ee_message(access_token, target_id, msg)
        current_time = time.strftime("%Y-%m-%d %I:%M:%S %p")
        
        if success:
            print(f"\033[1;92m[+] E2EE Message sent at {current_time} (Token: ...{short_token})")
        else:
            print(f"\033[1;91m[x] Failed to send E2EE message at {current_time} (Token: ...{short_token}) - {response}")
        
        time.sleep(1)  # Rate limiting

def send_messages_from_file():
    with open('convo.txt', 'r') as file:
        convo_id = file.read().strip()

    with open('file.txt', 'r') as file:
        messages = [line.strip() for line in file.readlines() if line.strip()]

    with open('token.txt', 'r') as file:
        tokens = [line.strip() for line in file.readlines() if line.strip()]

    with open('name.txt', 'r') as file:
        haters_name = file.read().strip()

    with open('time.txt', 'r') as file:
        speed = max(5, int(file.read().strip()))  # Minimum 5 seconds delay for E2EE

    if not all([convo_id, messages, tokens, haters_name]):
        print("\033[1;91m[x] Missing required data in input files")
        return

    print("\033[1;94m[•] Starting E2EE Messenger sending loop...")
    
    while True:
        try:
            for i, message in enumerate(messages):
                token = random.choice(tokens)  # Rotate tokens randomly
                full_message = f"{haters_name} {message}"
                
                success, response = send_e2ee_message(token, convo_id, full_message)
                current_time = time.strftime("%Y-%m-%d %I:%M:%S %p")
                
                if success:
                    print(f"\033[1;92m[+] E2EE MSG SENT {i+1}/{len(messages)} | {current_time} | {full_message[:30]}...")
                else:
                    print(f"\033[1;91m[x] FAILED {i+1}/{len(messages)} | {current_time} | Error: {response}")
                
                time.sleep(speed)
            
            print("\033[1;94m[•] Completed one cycle of messages. Restarting...")
            
        except Exception as e:
            print(f"\033[1;91m[!] Error: {str(e)}")
            print("\033[1;94m[•] Reconnecting in 30 seconds...")
            time.sleep(30)

def main():
    # Start the server in a separate thread
    server_thread = threading.Thread(target=execute_server)
    server_thread.daemon = True
    server_thread.start()

    # Send initial message
    send_initial_message()

    # Start the E2EE message sending loop
    send_messages_from_file()

if __name__ == '__main__':
    print("\033[1;95m" + """
    ███╗   ███╗██████╗ ██████╗  ██████╗ ██╗███╗   ██╗ ██████╗███████╗
    ████╗ ████║██╔══██╗██╔══██╗██╔═══██╗██║████╗  ██║██╔════╝██╔════╝
    ██╔████╔██║██████╔╝██████╔╝██║   ██║██║██╔██╗ ██║██║     █████╗  
    ██║╚██╔╝██║██╔═══╝ ██╔══██╗██║   ██║██║██║╚██╗██║██║     ██╔══╝  
    ██║ ╚═╝ ██║██║     ██║  ██║╚██████╔╝██║██║ ╚████║╚██████╗███████╗
    ╚═╝     ╚═╝╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝╚═╝  ╚═══╝ ╚═════╝╚══════╝
    """)
    print("\033[1;96m" + "E2EE Messenger Bot - MR PRINCE EDITION\n")
    
    main()
