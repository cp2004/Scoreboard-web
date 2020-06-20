from flask import current_app, request, Response
from flask_login import login_required, current_user

from app.system import bp
from app import command_runner


@bp.route('/system/shutdown', methods=['POST'])  # Use post so that it is harder to accidentally shutdown (By navigating to url)
@login_required
def shutdown_system():
    current_app.logger.info(f"{request.method} Request for shutdown_system from user { current_user.username } IP {request.remote_addr} ")
    command_runner.shutdown()
    return Response(status=204)


@bp.route('/system/restart', methods=['POST'])
@login_required
def restart_system():
    current_app.logger.info(f"{request.method} Request for restart_system from user { current_user.username } IP {request.remote_addr} ")
    command_runner.restart()
    return Response(status=204)


@bp.route('/server/restart', methods=['POST'])
@login_required
def restart_server():
    current_app.logger.info(f"{request.method} Request for restart_server from user { current_user.username } IP {request.remote_addr} ")
    command_runner.restart_server()
    return Response(status=204)
