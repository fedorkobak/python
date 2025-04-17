'''
Tools for running jupyter kernels from the other jupyter runtime.
'''
from typing import Any
from queue import Empty
import multiprocessing
from ipykernel.kernelapp import IPKernelApp
from ipykernel.ipkernel import IPythonKernel
from ipykernel.kernelbase import Kernel
from jupyter_client.blocking import BlockingKernelClient


def _run_kernel_target(
    connection_file: str,
    kernel_class: Kernel = IPythonKernel
) -> None:
    """
    Target for multiprocessing that runs jupyter kernel.

    Parameters:
    connection_file: str
        Directory of the connection file that have to be used for the
        connection.
    kernel_class: Kernel
        Kernel class that implements kernel to be used in the application.
    """
    IPKernelApp.launch_instance(
        ["-f", connection_file],
        kernel_class=kernel_class
    )


class IPKernelAppProcess:
    '''
    Class implements the Jupyter kernel in the separate 'spawn' process.

    Parameters:
    connection_file: str
        Directory of the connection file that have to be used for the
        connection.
    kernel_class: Kernel
        Kernel class that implements kernel to be used in the application.
    '''

    def __init__(
        self,
        connection_file: str,
        kernel_class: Kernel = IPythonKernel
    ):
        context = multiprocessing.get_context("spawn")
        self.process = context.Process(
            target=_run_kernel_target,
            kwargs={
                "connection_file": connection_file,
                "kernel_class": kernel_class
            }
        )
        self.process.start()

    def __del__(self):
        self.process.terminate()
        self.process.join()


def get_messages(
    connection_file: str,
    code: str,
) -> list[dict]:
    '''
    Returns messages that corresponding of the given code on the kernel
    determined by the given connection file.

    Parameters:
    connection_file: str
        Path to the connection file.
    code: str
        Code to be executed.
    '''
    client = BlockingKernelClient()
    client.load_connection_file(connection_file)
    client.start_channels()
    client.execute(code)

    ans_list = []

    while True:
        try:
            ans_list.append(client.get_iopub_msg(timeout=5))
        except Empty:
            break

    return ans_list
