import os
import textwrap
import tempfile

from unittest.mock import MagicMock
from unittest import IsolatedAsyncioTestCase

from traitlets.config import Config


from src.http_kernel.http_kernel import HttpKernel


class TestHttpKernel(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self._original_ipython_dir = os.environ.get("IPYTHONDIR")
        self._tmpdir = tempfile.TemporaryDirectory()
        os.environ["IPYTHONDIR"] = self._tmpdir.name

        config = Config()
        config.HistoryManager.enabled = False
        self.kernel = HttpKernel(config=config)
        self.kernel.send_response = MagicMock()

    async def asyncTearDown(self):
        self.kernel.do_shutdown(False)
        if self._original_ipython_dir is None:
            os.environ.pop("IPYTHONDIR", None)
        else:
            os.environ["IPYTHONDIR"] = self._original_ipython_dir
        self._tmpdir.cleanup()

    async def test_http_request_emits_stream_output(self):
        request_text = (
            "GET /ping HTTP/1.1\r\n"
            "Host: localhost\r\n"
            "Connection: close\r\n"
            "\r\n"
        )
        code = textwrap.dedent(f"""
            import socket
            import time

            req = {request_text!r}
            for _ in range(50):
                try:
                    s = socket.create_connection(("127.0.0.1", 3232), timeout=0.2)
                    break
                except OSError:
                    time.sleep(0.05)
            else:
                raise RuntimeError("server not ready")

            s.sendall(req.encode("latin1"))
            s.shutdown(socket.SHUT_WR)
            while True:
                chunk = s.recv(1024)
                if not chunk:
                    break
            s.close()
            """
        )

        result = await self.kernel.do_execute(
            code=code,
            silent=True,
            store_history=False,
        )

        self.assertEqual(result["status"], "ok")
        self.kernel.send_response.assert_called_once()
        args, _ = self.kernel.send_response.call_args
        self.assertEqual(args[1], "stream")
        self.assertEqual(args[2]["text"], request_text)
