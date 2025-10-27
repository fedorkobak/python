'''
Set of tools to automate the MLflow functionality overview.
'''
import os
import sys
import logging
import multiprocessing as mp

import mlflow
import mlflow.models.flavor_backend_registry

logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)


def run_inference_server(
    model_uri: str,
    port: int = 5000
):
    """Run mlflow inference server for a model with given URI."""
    backend = mlflow.models.flavor_backend_registry.get_flavor_backend(
        model_uri=model_uri,
        env_manager="local"
    )
    backend.serve(
        model_uri=model_uri,
        port=port,
        host="localhost",
        timeout=60,
        enable_mlserver=False
    )


class ModelInferenceProcess():
    """
    Runs the MLflow model inference server as a subprocess.
    """
    def __init__(
        self,
        model_uri: str,
        port: int = 5000,
        stdout: str | bytes | os.PathLike | None = os.devnull,
        stderr: str | bytes | os.PathLike | None = os.devnull
    ):
        self.model_uri = model_uri
        self.port = port
        self.stdout = stdout
        self.stderr = stderr
        self._process = None

    def _run(self):
        logger.debug(
            "Running the server. Got stdout=%s, stderr=%s",
            self.stdout, self.stderr
        )
        if self.stdout:
            sys.stdout = open(self.stdout, 'a')
        if self.stderr:
            sys.stderr = open(self.stderr, 'a')
        run_inference_server(
            model_uri=self.model_uri,
            port=self.port
        )

    def start(self):
        if self._process is not None:
            raise RuntimeError("Process is already running.")

        self._process = mp.Process(target=self._run, daemon=True)
        self._process.start()

    def stop(self):
        if self._process is None:
            raise RuntimeError("Process is not running.")
        self._process.terminate()
        self._process.join()
        self._process = None
