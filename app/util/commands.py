import threading

import subprocess
from flask import current_app


class CommandRunner():
    def init_app(self, app):
        self.COMMANDS = {
            'shutdown': app.config['CMD_SHUTDOWN'].split(),
            'restart': app.config['CMD_RESTART'].split(),
            'restart_server': app.config['CMD_RESTART_SERVER'].split()
        }
        app.logger.info(f"Currently configured commands are: {self.COMMANDS}")

    def get_command(self, cmd):
        """Looks up user-configured command from dict"""
        try:
            current_app.logger.info(f"Looking for command {cmd}")
            return self.COMMANDS[cmd]
        except KeyError:
            current_app.logger.error(f"Command '{cmd}' not found'")
            return None

    def run_command_thread(self, command):
        """Runs a command (In a thread) using subprocess
        Non blocking, returns the thread so you can use thread.join() to wait

        Args:
            command (str): Command to run: ['shutdown', 'restart, 'restart_serve']

        Returns:
            threading.Thread: Thread that the command is running in
        """
        cmd_thread = threading.Thread(target=self.run_command, args=(command,), kwargs={'capture_output': False})
        cmd_thread.daemon = True
        cmd_thread.start()
        return cmd_thread

    def run_command(self, command, capture_output=True):
        """Blocking command, for if you want to wait for some stdout.
        Args:
            command (str): Command to run: ['shutdown', 'restart, 'restart_serve']
            capture_output (bool, optional): Return stdout or not. Defaults to True.

        Returns:
            str: stdout from command if capture_output is True
        """
        current_app.logger.info(f"Request for command {command}")
        actual_command = self.get_command(command)
        if actual_command:
            current_app.logger.info(f"Running command for '{command}':'{actual_command}'")

            output = subprocess.run(
                actual_command,
                capture_output=True,
                check=True
            )

            current_app.logger.info(f"If still running, here's the output: {output.stdout.decode('utf-8')}")
            if capture_output:
                return output.stdout.decode('utf-8')
            else:
                return None
        else:
            current_app.logger.warning(f"Could not find command for '{command}'")

    def shutdown(self, thread=False):
        """Run shutdown command"""
        current_app.logger.info("Recieved signal to shutdown")
        if thread:
            self.run_command_thread('shutdown')
        else:
            self.run_command('shutdown', capture_output=False)

    def restart(self, thread=False):
        """Run restart command"""
        current_app.logger.info("Recieved signal to restart")
        if thread:
            self.run_command_thread('restart')
        else:
            self.run_command('restart', capture_output=False)

    def restart_server(self, thread=False):
        """Run restart server command"""
        current_app.logger.info("Recieved signal to restart server")
        if thread:
            self.run_command_thread('restart')
        else:
            self.run_command('restart_server', capture_output=False)
