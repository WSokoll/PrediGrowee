import os

from flask import current_app, render_template
from flask_admin import BaseView, expose


class ErrorsBaseView(BaseView):

    @expose('/')
    def index(self):
        # TODO: add number of lines to config
        # Read last 500 lines from logs/error.log file
        path = f"{current_app.root_path}/logs/error.log"

        if not os.path.isfile(path):
            pass  # TODO

        number_of_lines = 500
        with open(path, mode='rb') as f:
            try:
                f.seek(-1, os.SEEK_END)
                new_lines = 0
                while new_lines < number_of_lines:
                    if f.read(1) == b'\n':
                        new_lines += 1
                    f.seek(-2, os.SEEK_CUR)
                f.seek(2, os.SEEK_CUR)
            # catch OSError when the file has fewer than number_of_lines
            except OSError:
                f.seek(0)
            last_lines = f.readlines()

        try:
            decoded_lines = [line.decode('utf-8') for line in last_lines]
        except UnicodeDecodeError:
            decoded_lines = [line.decode() for line in last_lines]

        lines = ''.join(decoded_lines)

        return render_template('admin/views/errors.html')
