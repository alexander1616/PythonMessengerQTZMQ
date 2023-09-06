import sys, os, time
import zmq

def runServer(port):
    context = zmq.Context()
    socket = context.socket(zmq.PUSH)
    socket.bind("tcp://*:%d"%port)

    pid = os.getpid()
    msgcount = 1;
    print("Server %d PUSH at port %d" % (pid, port))
    while True:
        msg = "server %d msg %d" % ( pid, msgcount )
        msgcount += 1
        socket.send_string(msg)
        time.sleep(.0001)

if __name__ == "__main__":
    if len(sys.argv)<2:
        print("Missing Port")
        print(f"Usage  : {sys.argv[0]} port")
        print(f"Example: {sys.argv[0]} 5100")
        sys.exit(1)
    else:
        port=int(sys.argv[1])
    runServer(port)
    sys.exit(0)
