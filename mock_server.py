


import json
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Tuple, Any

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# #create a mock server to handle http post request
class MockAPIHandler(BaseHTTPRequestHandler):
    def do_POST(self) -> None:
        """Handle POST requests."""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            logger.info('Received data:')
            decoded_data = json.loads(post_data.decode('utf-8'))
            logger.info(json.dumps(decoded_data, indent=2))
            
            self._send_response(200, {"status": "success"})
        except json.JSONDecodeError:
            logger.error("Received invalid JSON data")
            self._send_response(400, {"status": "error", "message": "Invalid JSON data"})
        except Exception as e:
            logger.exception(f"An error occurred while processing the request: {e}")
            self._send_response(500, {"status": "error", "message": "Internal server error"})

    def _send_response(self, status_code: int, data: dict) -> None:
        """Send a response with the given status code and data."""
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

def run_mock_server(server_class: Any = HTTPServer, handler_class: Any = MockAPIHandler, port: int = 8000) -> None:
    """Run the mock server."""
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    
    logger.info(f"Mock API server running on port {port}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    finally:
        httpd.server_close()
        logger.info("Server closed")

if __name__ == "__main__":
    run_mock_server()