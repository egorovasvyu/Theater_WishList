from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer


HOST = "0.0.0.0"
PORT = 3000


if __name__ == "__main__":
    server = ThreadingHTTPServer((HOST, PORT), SimpleHTTPRequestHandler)
    print(f"Theatre wishlist is running on http://{HOST}:{PORT}")
    server.serve_forever()
