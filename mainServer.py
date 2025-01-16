import sys
sys.path.append("Kode")
import server #importer player fra kode mappen

from PyQt6.QtWidgets import *

if __name__ == "__main__":
    '''
    while True:
        try:
            port = input("Hvilken port mellem 49152 og 65535 skal serveren bruge?\nTryk enter for 54321\n")
            if port == "":
                port = 54321
                break
            elif int(port.strip()) >= 65535 and int(port.strip()) <= 49152:
                port = int(port)
                break
        except:
            pass
    '''
        
    port = 54321        
    server = server.host(port)
    print("Fire på stribe hostes nu på "+str(server.myIP)+":"+str(port))
    while True:
        if input("Skriv \"C\" for at lukke serveren:").strip() == "C":
            server.closeMe()
            break
    
    
