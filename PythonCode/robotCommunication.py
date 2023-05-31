import socket

def EstablishConnection():
    clientAddress = None
    clientSocket = None
    if clientAddress is None or clientSocket is None:
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)            # Set up server socket
        serverSocket.bind(("130.89.212.46", 3500))                                 # Binds socket to device IP address and port 8080
        serverSocket.listen(1)                                                      # Waits for one device to connect

        print("Waiting for a connection...")
        clientSocket, clientAddress = serverSocket.accept()                         # Accepts connection from ESP32 
        print("Accepted connection from:", clientAddress) 
        
def SendSignals(PWM1,PWM2,PWM3,PWM4,PWM5,PWM6):
    
    PWMtoSend = bytearray([int(PWM1), int(PWM2), int(PWM3), int(PWM4), int(PWM5), int(PWM6)])         # Creates bytearray consisting of the generated values
    try:
        clientSocket.sendall(PWMtoSend)                                             # Sends data from server to client via TCP
    except ConnectionError:                                             
        print("Connection error. Device disconnected.")                             #In case of Disconnect resets clientAddress and clientSocket
        clientSocket.close()
        clientAddress = None
        clientSocket = None