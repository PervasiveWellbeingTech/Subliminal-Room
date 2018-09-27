# Subliminal Room: OLFACTORY

This repo contains code developed and collected for the olfactory sense.

## pmoodo.py

Controls the Moodo device in the room. Connect to the hub with
```
init(email, password)
```
Then, control the device with
```
change_state(fan_volume=0, box_status=1, fan_speeds=[0,0,0,0], fan_states=[False,False,False,False])
```
