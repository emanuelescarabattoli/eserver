import socketserver


status = "LIGHTGROUP1#OFF;LIGHTGROUP2#OFF;LIGHTGROUP3#OFF;GATE#CLOSED;SENSOR1#24.000;SENSOR2#30.000"

class Handler(socketserver.BaseRequestHandler):


    def handle(self):
        global status
        self.data = self.request.recv(1024).strip().decode("utf-8")
        if self.data == "STATUS":
            self.request.sendall(bytes(status, "utf-8"))
        else:
            received = self.data.split("#")
            received_device = received[0]
            received_status = received[1]
            new_stauts = ""
            devices_statuses = status.split(";")
            for device_status in devices_statuses:
                device_data = device_status.split("#")
                if device_data[0] == received_device:
                    new_stauts += received_device + "#" + received_status + ";"
                else:
                    new_stauts += device_data[0] + "#" + device_data[1] + ";"
            new_stauts = new_stauts[:-1]
            status = new_stauts
            self.request.sendall(bytes("DONE", "utf-8"))

if __name__ == "__main__":
    with socketserver.TCPServer(("localhost", 7000), Handler) as server:
        server.serve_forever()
