import time

from .app import TarsMavApp

def main():
    app = TarsMavApp()

    while True:
        app.sim.tick()
        time.sleep(1)
        app.read()


if __name__ == "__main__":
    main()