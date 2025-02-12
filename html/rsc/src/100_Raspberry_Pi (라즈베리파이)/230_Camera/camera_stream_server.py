# camera_stream_server.py
# Mostly copied from https://picamera.readthedocs.io/en/release-1.13/recipes2.html

print( "Getting a camera ..." )
import io, logging, socketserver, subprocess
from http import server
from threading import Condition

from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.encoders import H264Encoder
from picamera2.outputs import FileOutput

size = (width, height) = (640, 480)
#size = (width, height) = (1296, 972)

PAGE = f"""\
<html>
    <head>
        <title>라즈베리파이 감시 카메라</title>
        <meta charset="UTF-8">
    </head>
    <body>
        <center>
            <h3>라즈베리파이 감시 카메라</h3>
            <img src="stream.mjpg" width="{width}" height="{height}" /> 
        </center>
    </body>
</html>
"""

class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = Condition()

    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()
        pass
    pass
pass

class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()
        pass
    pass
pass

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True
pass

picam2 = Picamera2()
picam2.configure(picam2.create_video_configuration(main={"size": (640, 480)}))
output = StreamingOutput()
picam2.start_recording(JpegEncoder(), FileOutput(output))

print( "start camera recording ..." )

try:
    port = 8080
    address = ('', port)
    server = StreamingServer(address, StreamingHandler)
    ip_addr = subprocess.getoutput("hostname -I").strip()
    print( f"Serving the camera stream ..." )
    print( f"http://{ip_addr}:{port}" )
    server.serve_forever()
finally:
    picam2.stop_recording()
pass