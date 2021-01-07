import requests, socket, threading, subprocess
from win10toast import ToastNotifier
from time import sleep

LHOST = ''
LPORT = 8080
BUFFER_SIZE = 1024 # Max message bytes

WEBHOOK =  "https://tinyurl.com/y62xk9vx/Trigger"

def _get_current_network_():
  current_wifi = subprocess.check_output("cmd.exe /c netsh wlan show interfaces | find \"SSID                   : \"")
  current_wifi = current_wifi.decode('utf-8', errors="ignore").replace('SSID                   : ', '').strip()
  return current_wifi

def server_thread():
  # Creating server
  server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

  # Binding port
  server.bind((LHOST, LPORT))

  # Reciving Data
  while (True):
    try:
      data = server.recvfrom(BUFFER_SIZE)
      title, message = data[0].decode('utf-8', errors="ignore").split(';')

      # Show toast
      toaser = ToastNotifier()
      toaser.show_toast(title, message, threaded=True)
    except ValueError:
      pass

def main():
  current_wifi = _get_current_network_()
  address = socket.gethostbyname(socket.gethostname()) 

  requests.get(WEBHOOK, params={
    'wifi': current_wifi,
    'ip': address,
    'port': LPORT
  })

  t = threading.Thread(target=server_thread, daemon=True)
  t.start()

if __name__ == "__main__":
  try:
    main()
    while (True):
      pass
  except KeyboardInterrupt:
    print("Good Bye...")
  except Exception as e:
    print("Some fucking error occurred...")
    print(e)