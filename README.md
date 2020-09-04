# Cyber Data Exchange Model (CyberDEM) Python Package

## Overview

## Status

CyberDEM Python is based on the CyberDEM standard that is currently in DRAFT format, and therefore subject to change. 

## Getting Started

These instructions will get a copy of the package installed on your local machine.

### Installing

1. Download CyberDEM Python and unzip the download folder
2. From within the top-level cyberdem folder (where [setup.py](setup.py) is located) run
```
$ pip3 install .
```

3. To test that cyberdem is installed properly run

```
$ python3
>>> from cyberdem import base
>>> print(base.System())
System(
    id: 3bb3512e-dc75-4b86-b234-25040a79b9b9
)
```

You may also try running the example.py file downloaded with the zip file.

```
$ python3 example.py

[expected output]
```

## License

Copyright 2020 Carnegie Mellon University. See the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgements

- [SISO Cyber DEM Product Development Group](https://www.sisostds.org/StandardsActivities/DevelopmentGroups/CyberDEMPDG.aspx)