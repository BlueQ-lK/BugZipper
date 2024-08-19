from flask import Flask
from flask_cors import CORS
import nmap

app = Flask(__name__)
CORS(app, resources={r"/*": {'origins': "*"}})


class nmap_t:
    def __init__(self, ip, aggresive ,port = ''):
        self.ip = ip
        self.port = port
        self.aggresive = aggresive

    def port_scan(self):
        scanner = nmap.PortScanner()
        try:
            if self.port != '':
                scanner.scan(self.ip, self.port, arguments=f"-v {'-A' if self.aggresive else ''}")
                xml_output = scanner.get_nmap_last_output()
                with open('data\\output.xml', 'w') as file:
                    file.write(xml_output.decode('utf-8'))
            else:
                scanner.scan(self.ip, arguments=f"-v {'-A' if self.aggresive else ''}")
                xml_output = scanner.get_nmap_last_output()
                with open('data\\output.xml', 'w') as file:
                    file.write(xml_output.decode('utf-8'))
            
        except Exception as e:
            print(e)
    
    