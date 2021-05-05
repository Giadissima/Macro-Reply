import requests, socket, threading, subprocess
from win10toast import ToastNotifier
from time import sleep
import win32gui, win32con


hide = win32gui.GetForegroundWindow()
win32gui.ShowWindow(hide, win32con.SW_HIDE)

LHOST = '0.0.0.0'
LPORT = 8080
BUFFER_SIZE = 1024 # Max message bytes

WEBHOOK =  "https://tinyurl.com/y62xk9vx/Trigger"
toaster = ToastNotifier()


def incoming_call(title, message):
    toaster.show_toast(title,
    message,
    icon_path="src/cell.ico",
    duration=5,
    threaded=True)

def success_notify(title, message):
  toaster.show_toast(title,
  message,
  icon_path="src/TOAST.ico",
  duration=5,
  threaded=True)

def notification_notify(title, message):
  toaster.show_toast(title,
  message,
  icon_path="src/notifiche.ico",
  duration=5,
  threaded=True)

def _get_current_network_():
  current_wifi = subprocess.check_output("cmd.exe /c netsh wlan show interfaces | find \"SSID                   : \"")
  current_wifi = current_wifi.decode('utf-8', errors="ignore").replace('SSID                   : ', '').strip()
  return current_wifi

def server_thread():
  # Creating server 
  server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  # Binding port
  server.bind((LHOST, LPORT))

  # Receiving Data
  while (True):
    try:
      server.listen(1)
      (client, address) = server.accept()

      data = client.recv(BUFFER_SIZE) # Blocking instruction, wait until a message recived
      client.close()
      title, message = data.decode('utf-8', errors="ignore").split(';')
    
      print("New message:")
      print("\ttitle: ", title)
      print("\tmessage: ",message)

      if(title == "Successo"):
          success_notify(title, message)
      if(title == "Chiamata in arrivo"):
          incoming_call(title, message)
      else:
          notification_notify(title, message)
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
  print("my ip is... ", address)

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