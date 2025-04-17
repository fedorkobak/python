'''
Tools for running jupyter kernels from the other jupyter runtime.
'''
import multiprocessing
from ipykernel.kernelapp import IPKernelApp
from ipykernel.ipkernel import IPythonKernel
from ipykernel.kernelbase import Kernel


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
