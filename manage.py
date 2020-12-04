try:
    from werkzeug.contrib.fixers import ProxyFix
except ImportError:
    from werkzeug.middleware.proxy_fix import ProxyFix
from flask_script import Manager, Server

from app import create_app


app = create_app()

app.wsgi_app = ProxyFix(app.wsgi_app)
manager = Manager(app)
manager.add_command("run", Server())
print(app.url_map)

if __name__ == '__main__':
    manager.run()
