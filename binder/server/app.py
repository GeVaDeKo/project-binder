from functools import partial
from http.server import ThreadingHTTPServer
from pathlib import Path

from binder.server.handler import BinderRequestHandler
  
def start_server(
    binder_path: Path,
    host: str = "127.0.0.1",
    port: int = 8787
):
    BinderRequestHandler.binder_path = Path(binder_path)
    
    static_root = Path(__file__).parent
    handler = partial(BinderRequestHandler, directory=str(static_root))
    
    server = ThreadingHTTPServer((host, port), handler)
    
    print(f"Project-Binder viewer running at http://{host}:{port}")
    print("Press CTRL+C to stop.")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nProject-Binder viewer stopped.")
    finally:
        server.server_close()