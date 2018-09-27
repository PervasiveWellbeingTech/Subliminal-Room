# Subliminal Room: PILOT

This repo contains code developed and collected for the pilot experiment.

## experiment.py

Runs the pilot experiment in either **debugging** or **experiment** mode. For the **debugging** mode the code must be ran as follows:
```
python experiment.py test
```
If the computer is configured properly, the code should be self-sufficient in navigating the experiment. After each step is complete, the code will save progress in a folder located in
```
pilot/output/
```
The files saved are
```
params.json --> initial parameters of the experiment, saved once
experimentX.json --> responses, times, and etc. saved multiple times

```

## analysis.py

When run, performs histogram analysis of the output data located in the folder above.
