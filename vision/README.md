# Subliminal Room: VISION

This repo contains code developed and collected for the vision sense.

## controller.py

Controls the Hue lights in the room. Connect to the Hue Bridge with
```
init(bridge_ip, gamut)
```

Requires explicit commands which can be generated like

```
make_command([255, 0, 0], 255, 0) --> color red, full brightness, 0s delay
```
which then can be stored or executed via
```
set_group(command)
```
