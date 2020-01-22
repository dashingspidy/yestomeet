from project import app, socketio
from project.helpers import age
from project.models import initialize

app.jinja_env.globals.update(age=age)

# @app.errorhandler(403)
# def forbidden_page(error):
#     return render_template("errors/403.html"), 403


# @app.errorhandler(404)
# def page_not_found(error):
#     return render_template("errors/404.html"), 404


# @app.errorhandler(500)
# def server_error_page(error):
#     return render_template("errors/500.html"), 500

initialize()
socketio.run(app, host='0.0.0.0')
