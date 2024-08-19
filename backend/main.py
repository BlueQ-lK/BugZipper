from flask import Flask, jsonify, request
from flask_cors import CORS
from side_quest import run
from data import xmlTodb, dbmain, autoDel

app = Flask(__name__)
CORS(app, resources={r"/*": {'origins': "*"}})

checkForComplete = False

def scanHandler(**kwargs):
    global checkForComplete
    if kwargs.get('aggresive') is None:
        kwargs['aggresive'] = False

    print("normal scan")
    obj  = run.nmap_t(
        ip = kwargs.get('target'),
        port = kwargs.get('port'),
        aggresive = kwargs.get('aggresive')
    )
    obj.port_scan()
    checkForComplete = True

@app.route('/', methods=["POST", "GET"])
def handleRequest():
    targetSave = None
    try:
        if request.method == 'GET':
            return jsonify({'status' : 'Success'})
    
        if request.method == 'POST':
            data = request.get_json()
            targetip = data.get('ip_addr')
            targetport = data.get('port')
            targetagg = data.get('aggscan')
            targetSave = data.get('save')
            targetsaveName = data.get('saveName')
            if targetsaveName == '' or targetsaveName is None or targetsaveName == '':
                targetsaveName = 'New Scan'
            scanHandler(
                target = targetip,
                port = targetport,
                aggresive = targetagg
            )
            if checkForComplete == True:
                latestdb, port_number = xmlTodb.main(targetsaveName)
                inforesult = dbmain.provideData(latestdb, port_number)
                return jsonify(infoHost=inforesult[0], infoPort=inforesult[1], infoScript=inforesult[2])
    except Exception as e:
        print(e)
    finally:
        #if save button is not clicked
        if targetSave == False or targetSave is None: 
            try:
                autoDel.main(latestdb)
            except Exception as e:
                print(e) 
            
    return jsonify({'status': 'Operation completed'}) 

        

@app.route('/history', methods=['GET', 'DELETE'])
def history_handler():
    try:
        if request.method == 'GET':
            #history page
            dbmainresult = dbmain.main()
            return jsonify(dbmainresult=dbmainresult)
        
        if request.method == 'DELETE':
            data = request.get_json()
            status = dbmain.row_delete(data['delid'])
            dbmainresult = dbmain.main()
            return jsonify(status=status , dbmainresult=dbmainresult)
        
    except Exception as e:
        print(e)


@app.route('/details', methods=['GET'])
def aa():
    scan_info_id = request.args.get('scan_info_id')
    inforesult = dbmain.provideData(scan_info_id)
    return jsonify(infoHost=inforesult[0], infoPort=inforesult[1], infoScript=inforesult[2])


if __name__ == '__main__':
    app.run(debug=True, port=4000)