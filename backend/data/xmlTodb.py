import xml.etree.ElementTree as ET
import sqlite3

scan_info_id = None
port_Number = []

def parse_xml_and_store_to_db(xml_file, db_file, saveName):
    global scan_info_id, port_Number
    # Parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Connect to SQLite database
    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    # Create tables
    c.execute('''
    CREATE TABLE IF NOT EXISTS scan_info (
        id INTEGER PRIMARY KEY,
        scanner TEXT,
        startstr TEXT,
        version TEXT
    )
    ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS host (
        id INTEGER PRIMARY KEY,
        scan_info_id INTEGER,
        state TEXT,
        addr TEXT,
        addrtype TEXT,
        os_name TEXT,
        os_accuracy INTEGER,
        os_vendor TEXT,
        os_family TEXT,
        os_gen TEXT,
        lastboot TEXT,
        FOREIGN KEY(scan_info_id) REFERENCES scan_info(id)
    )
    ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS port (
        id INTEGER PRIMARY KEY,
        host_id INTEGER,
        protocol TEXT,
        portid INTEGER,
        state TEXT,
        reason TEXT,
        reason_ttl INTEGER,
        service_name TEXT,
        service_product TEXT,
        service_version TEXT,
        service_extrainfo TEXT,
        FOREIGN KEY(host_id) REFERENCES host(id)
    )
    ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS script (
        host_id INTEGER ,
        port_id INTEGER,
        script_id TEXT,
        output TEXT,
        FOREIGN KEY (port_id) REFERENCES port (id)
    )
    ''')

    # Insert data into scan_info table
    scan_info = root.attrib
    scan_info_values = (saveName, scan_info.get('startstr'), "1.0")
    c.execute('INSERT INTO scan_info (scanner, startstr, version) VALUES (?, ?, ?)', scan_info_values)
    scan_info_id = c.lastrowid
    

    # Insert data into host table
    for host in root.findall('host'):
        status = host.find('status').attrib
        address = host.find('address').attrib

        os = host.find('os/osmatch')
        if os is not None:
            os_name = os.get('name')
            os_accuracy = int(os.get('accuracy'))
            os_class = os.find('osclass')
            os_vendor = os_class.get('vendor')
            os_family = os_class.get('osfamily')
            os_gen = os_class.get('osgen')
        else:
            os_name = os_accuracy = os_vendor = os_family = os_gen = None

        uptime = host.find('uptime')
        if uptime is not None:
            lastboot = uptime.get('lastboot')
        else:
            lastboot = None

        host_values = (scan_info_id, status.get('state'), address.get('addr'), address.get('addrtype'), os_name, os_accuracy, os_vendor, os_family, os_gen, lastboot)
        c.execute('''
        INSERT INTO host (scan_info_id, state, addr, addrtype, os_name, os_accuracy, os_vendor, os_family, os_gen, lastboot)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', host_values)
        host_id = c.lastrowid

        # Insert data into port table
        for port in host.find('ports').findall('port'):
            state = port.find('state').attrib
            service = port.find('service').attrib if port.find('service') is not None else {'name': None, 'product': None, 'version': None, 'extrainfo': None, 'method': None, 'conf': None}
            port_values = (host_id, port.attrib.get('protocol'), port.attrib.get('portid'), state.get('state'), state.get('reason'), state.get('reason_ttl'), service.get('name'), service.get('product'), service.get('version'), service.get('extrainfo'))
            
            if all(value is not None for value in service.values()):        
                c.execute('''
                INSERT INTO port (host_id, protocol, portid, state, reason, reason_ttl, service_name, service_product, service_version, service_extrainfo)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', port_values)
                port_id = c.lastrowid

                #script data
                for script in port.findall('script'):
                    script_id = script.get('id')
                    output = script.get('output')

                    c.execute('''
                    INSERT INTO script (host_id, port_id, script_id, output)
                    VALUES (?, ?, ?, ?)
                    ''', (host_id, port_id, script_id, output))
            elif all(value is None for value in service.values()):
                port_Number.append(port.attrib.get('portid'))
                 
            

    # Commit and close the connection
    conn.commit()
    conn.close()

def main(saveName):
    # Example usage
    parse_xml_and_store_to_db(r'data\output.xml', r'data\map_scan.db', saveName)
    return scan_info_id, port_Number
