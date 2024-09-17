from http.server import HTTPServer,BaseHTTPRequestHandler
import json

#create a mock server to handle http post request
class MockAPIHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        print('Recieved data')
        print(json.loads(post_data.decode('utf-8')))
        self.send_response(200)
        self.send_header('Content-type','application-type')
        self.end_headers()
        self.wfile.write(json.dumps({"status":"success"}).encode('utf-8'))
    
#run the mock server on a local port
def run_mock_server(port=8000):
        server_address = ('',port)
        httpd = HTTPServer(server_address,MockAPIHandler)
        
        print(f"Mock API server running on port {port}")
        httpd.serve_forever()

if __name__ == "__main__":
    run_mock_server()