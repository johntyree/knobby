Knobby
======

An experiment in reverse engineering the Griffin PowerMate USB jog
wheel/button on Linux.

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

Events
------

The events have one of three identified types and always come in groups. All
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
