Knobby
======

An experiment in reverse engineering the Griffin PowerMate USB jog
wheel/button on Linux.

First, install the udev rule to make sure your PowerMate appears at
`/dev/powermate`. Adjust the `RUN` line to something suitable for your machine
or remove it altogether if you want no notification of success. If all is done
correctly, a symlink should appear when the device is plugged in. If it doesn't
seem to be working, try running `# udevadm control --reload-rules` and
replugging the device.

A small but fully functional example is in `knobby/handlers/volume_control.py`.
Test it out with:

```
python -m knobby.handlers.volume_control
```

The example assumes that `/dev/powermate` is readable.

Events
------

Events come in from the device node as a byte stream with each event having the
form

```C
struct {
    timeval {long sec, long usec}
    unsigned int id
    int data
}
```
where `id` is unique for each kind of event and data describes the event in
some way.

The events have one of three identified ids and always come in groups. All
events in a group occur at the same time. The final event in a group is always
`end` and signals that no more events will arrive with the current time stamp.

Turn:
 * id: `0x00070002`
 * data: Magnitude of turn. Sign indicates direction with positive clockwise.

Button:
 * id: `0x01000001`
 * data: `1` if pressed. `0` if released.

End:
 * id: `0x0`
 * data: `0x0`

API
---

```python
from knobby.api import EventHandler, main

counter = 0

def my_callback(event):
    print(event)
    counter += 1
    # Stop processing after 4 events
    return counter == 4

my_handler = EventHandler(callback=my_callback)

if __name__ == '__main__':
    main(handler=my_handler)
