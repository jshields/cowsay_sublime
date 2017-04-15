"""
Instructions:

Initial setup:

    1. Install dependency: `sudo apt-get install cowsay`
    2. Put this file at ~.config/sublime-text-3/Packages/User/cowsay_sublime.py

Run the command:

    1. Hit Ctrl+` to open the Sublime console
    2. Type/paste `view.run_command("cowsay")` (without the backticks)
    3. Hit the Enter key

You may choose to create a shortcut or macro for running the command.
"""
import sublime, sublime_plugin
import subprocess
from os.path import splitext


class CowsayCommandError(Exception):
    pass


class CowsayCommand(sublime_plugin.TextCommand):
    def description(self):
        return 'Runs cowsay in the current file'

    def run(self, edit):
        file_name = self.view.file_name()
        if file_name is None:
            raise CowsayCommandError('No file name')

        # TODO use comment delimiters based on current selected syntax
        tokens = ('/*\n', '\n*/\n')
        if splitext(file_name)[1] == '.py':
            tokens = ('"""\n', '\n"""\n')

        self.view.window().set_status_bar_visible(True)
        self.view.window().status_message('Cowsay: %s' % file_name)

        # TODO have the cow say the TODOs in the file
        # FIXME sanitize file name to prevent security issues
        command = 'cowsay "{file_name}"'.format(file_name=file_name)
        results = subprocess.check_output(command, shell=True)

        out = (
            '{comment}'
            '{cow}'
            '{uncomment}'
        ).format(
            comment=tokens[0],
            cow=results.decode('UTF8'),
            uncomment=tokens[1]
        )

        self.view.insert(edit, 0, out)
