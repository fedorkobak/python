"""
Modificaiton of the IPythonKernel that listens for the 3232 port. If there is
some content it prints the contents as the cell output.
Could be useful for researching the tools that thransfer content through
network.
"""
import socket
import logging
import multiprocessing as mp

from ipykernel.ipkernel import IPythonKernel

logger = logging.getLogger(__name__)


def run_server(log_queue, host="0.0.0.0", port=8080):
    """
    Runs raw HTTP listener and sends printed data to the
    parent via queue.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen(5)

        while True:
            conn, addr = s.accept()
            with conn:

                raw = b""
                conn.settimeout(1.0)

                try:
                    while True:
                        chunk = conn.recv(4096)
                        if not chunk:
                            break
                        raw += chunk
                except socket.timeout:
                    pass

                try:
                    log_queue.put(raw.decode("latin1"))
                except Exception as e:
                    log_queue.put(f"Decode error: {e}")

                resp = (
                    "HTTP/1.1 200 OK\r\n"
                    "Content-Type: text/plain\r\n"
                    "Content-Length: 0"
                )
                conn.sendall(resp.encode("latin1"))


class HttpKernel(IPythonKernel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.log_queue = mp.Queue()
        self.proc = mp.Process(
            target=run_server,
            args=((self.log_queue, "0.0.0.0", 3232)),
            daemon=True
        )
        self.proc.start()

    async def do_execute(
        self,
        code,
        silent,
        store_history=True,
        user_expressions=None,
        allow_stdin=False
    ):
        await super().do_execute(
            code=code,
            silent=silent,
            store_history=store_history,
            user_expressions=user_expressions,
            allow_stdin=allow_stdin
        )

        if not self.log_queue.empty():
            msg = self.log_queue.get()
            self.send_response(
                self.iopub_socket,
                'stream',
                {"name": "stdout", "text": msg}
            )

        return {
            'status': 'ok',
            'execution_count': self.execution_count,
            'payload': [],
            'user_expressions': {},
        }

    def do_shutdown(self, restart):
        logging.info("Shutting kernel down.")
        self.proc.terminate()
        self.proc.join()
        return super().do_shutdown(restart)
