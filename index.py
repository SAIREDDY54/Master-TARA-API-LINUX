from flask import Flask, request
from flask_cors import CORS, cross_origin
# import win32pipe
# import win32file
import time
import os, errno


app = Flask(__name__)
CORS(app)

# app.config['CORS_HEADERS'] = 'Content-Type', 'access-control-allow-origin'

interfaces = []
filePath = []
absPath = []
abs = []


def runAnotherFile():
    os.system('python3 db_access.py')

@app.route('/hello', methods=['GET'])
def home():
    return "Hello World"

# @app.route('/interfaces', methods=['POST'])
# # @cross_origin(origin='*',headers=['access-control-allow-origin','Content-Type'])
# def getInterfaces():
#     global interfaces
#     interfaces = request.json["interfaces"]
#     print("pipe interfaces")
#     runAnotherFile()
#     pipe = win32pipe.CreateNamedPipe(
#         r'\\.\pipe\Foo',
#         win32pipe.PIPE_ACCESS_DUPLEX,
#         win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE | win32pipe.PIPE_WAIT,
#         1, 65536, 65536,
#         0,
#         None)
#     try:
#         print("waiting for client")
#         win32pipe.ConnectNamedPipe(pipe, None)
#         print("got client")

#         win32file.WriteFile(pipe, str.encode(f"{interfaces}"))
#         time.sleep(2)
#         win32file.WriteFile(pipe, str.encode(f"{sendFilePath()}"))
#         abs.clear()
#         # print(sendFilePath())
#         print("finished now")
#     finally:
#         win32file.CloseHandle(pipe)
#     return interfaces

@app.route('/interfaces', methods=['POST'])
@cross_origin()
def getInterfaces():
    global interfaces
    interfaces = request.json["interfaces"]
    # print("pipe interfaces")
    # runAnotherFile()
    # pipe = win32pipe.CreateNamedPipe(
    #     r'\\.\pipe\Foo',
    #     win32pipe.PIPE_ACCESS_DUPLEX,
    #     win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE | win32pipe.PIPE_WAIT,
    #     1, 65536, 65536,
    #     0,
    #     None)
    # try:
    #     print("waiting for client")
    #     win32pipe.ConnectNamedPipe(pipe, None)
    #     print("got client")

    #     win32file.WriteFile(pipe, str.encode(f"{interfaces}"))
    #     time.sleep(2)
    #     win32file.WriteFile(pipe, str.encode(f"{sendFilePath()}"))
    #     abs.clear()
    #     # print(sendFilePath())
    #     print("finished now")
    # finally:
    #     win32file.CloseHandle(pipe)
    FIFO = "./mypipe"


    try:
        os.mkfifo(FIFO)
    except OSError as oe:
        if oe.errno != errno.EEXIST:
            raise

    with open(FIFO, 'w') as f:
        f.write(str(interfaces)+str(sendFilePath()))
    
    runAnotherFile()

    # while True:
    abs.clear()
    
    return interfaces
        


@app.route('/filePath', methods=['POST'])
@cross_origin()
def getFilePath():
    global filePath
    global abs
    filePath = request.json["filePath"]
    abs.append(os.path.abspath(filePath))
    return os.path.abspath(filePath)


def sendFilePath():

    return abs


@app.route('/checkStatus', methods=['GET'])
@cross_origin()
def checkStatus():
    # main()
    if (len(interfaces) > 0):
        return "SUCCESS"
    else:
        return "FAILED"
