import sys

from application1 import Application


if __name__ == '__main__':
    app = Application(sys.argv)
    sys.exit(app.run())
