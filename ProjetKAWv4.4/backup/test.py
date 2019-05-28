from flask import Flask,request,render_template
from flask_socketio import SocketIO

testKAW = Flask(__name__)
socketio = SocketIO(testKAW)

if __name__ == "__main__":
    socketio.run(testKAW)

@testKAW.route('/')
@testKAW.route('/test_log', methods=['POST'])
def testintro():
	return render_template("formtest.html")