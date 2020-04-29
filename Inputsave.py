"""Simple example showing how to get gamepad events."""

from __future__ import print_function


from inputs import get_gamepad


def main():
    """Just print out some event infomation when the gamepad is used."""
    while 1:
        events = get_gamepad()
        for event in events:
            if event.state != 0:
                print("Button" + event.code)
                print(event.state)


if __name__ == "__main__":
    main()