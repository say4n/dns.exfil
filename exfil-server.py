import dnslib
import socketserver

HOST = "localhost"
PORT = 6000


class RequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data, socket = self.request
        parsed_data = dnslib.DNSRecord.parse(data)
        query = parsed_data.get_q().get_qname().idna()
        response = parsed_data.replyZone("status.noerror 0 IN A 0.0.0.0")

        print(f"{self.client_address} asked: {query}")

        socket.sendto(response.pack(), self.client_address)


if __name__ == "__main__":
    with socketserver.UDPServer((HOST, PORT), RequestHandler) as server:
        server.serve_forever()
