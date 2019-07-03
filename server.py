import socketserver


state = "LIGHTGROUP1#OFF;LIGHTGROUP2#OFF;LIGHTGROUP3#OFF;GATE#CLOSED;SENSOR1#24.000;SENSOR2#30.000"

class Handler(socketserver.BaseRequestHandler):

    def handle(self):
        global state
        self.data = self.request.recv(1024).strip().decode("utf-8")
        print("Received " + self.data)
        if self.data == "STATE":
            self.request.sendall(bytes(state, "utf-8"))
        else:
            received = self.data.split("#")
            received_device = received[0]
            received_state = received[1]
            new_stauts = ""
            devices_statees = state.split(";")
            for device_state in devices_statees:
                device_data = device_state.split("#")
                if device_data[0] == received_device:
                    new_stauts += received_device + "#" + received_state + ";"
                else:
                    new_stauts += device_data[0] + "#" + device_data[1] + ";"
            new_stauts = new_stauts[:-1]
            state = new_stauts
            self.request.sendall(bytes("DONE", "utf-8"))

if __name__ == "__main__":
    with socketserver.TCPServer(("localhost", 7000), Handler) as server:
        print("Server started")
        server.serve_forever()
