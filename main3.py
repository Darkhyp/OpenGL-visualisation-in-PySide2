import sys

from V3.application import Application


if __name__ == '__main__':
    app = Application(sys.argv)
    sys.exit(app.run())
