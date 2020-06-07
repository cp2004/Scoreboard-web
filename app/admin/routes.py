import os
from time import sleep
from flask import current_app, render_template, request, Response
from flask_login import current_user, login_required
from app.admin import bp


@bp.route('/admin/dash')
@login_required
def dash():
    current_app.logger.info(f"{request.method} Request for dashboard from user {current_user.username} IP {request.remote_addr} ")
    return render_template('admin/dash.html')

@bp.route('/admin/logs')
@login_required
def logs():
    log_path = os.path.join(current_app.config['BASE_DIRECTORY'], 'logs', 'tabletennis.log')

    def generate():
        with open(log_path) as f:
            while True:
                for line in reversed(f.readlines()):
                    yield line
                # print(read)
                sleep(1)

    return Response(generate(), mimetype='text/plain')
