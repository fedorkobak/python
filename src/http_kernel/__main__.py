from .http_kernel import HttpKernel
from ipykernel.kernelapp import IPKernelApp
IPKernelApp.launch_instance(kernel_class=HttpKernel)
