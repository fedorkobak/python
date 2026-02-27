import os
from tempfile import mkstemp
from command_kernel import CommandKernel, command

import logging

logger = logging.getLogger(__name__)


class LintersKernel(CommandKernel):
    """
    Kernel that apples a linter to the given code.
    """

    def _temp_file(self, code: str) -> str:
        """
        Create a tempfile that stores the code to be linted.

        Returns
        -------
        Path to the file.
        """
        fd, path = mkstemp()
        os.write(fd, code.encode("utf-8"))
        os.close(fd)
        return path

    def no_commands(self, code: str) -> str:
        logger.info("no commands is invoked")
        return f"python3 {self._temp_file(code)}"

    @command("#mypy")
    def mypy(self, code: str) -> str:
        logger.info("mypy is invoked")
        return f"mypy {self._temp_file(code)}"

    @command("#pyright")
    def pyright(self, code: str) -> str:
        logger.info("pyright is invoked")
        return f"pyright {self._temp_file(code)}"