# ReactivePanda

ReactivePanda is a library that aims to make it easier to teach programming to middle school / high school students.

Our philosophy is that using a non-domain specific langague such as python with the addition of reactive programming elements allows for an easier introduction and transition to more advanced programming.

This library is a wrapper of the [panda3d](https://panda3d.org) game engine.

## Usage

A simple hello world:

    from PandaSRC.Panda import *
    panda(hpr = hpr(time,1,0))
    start()

This produces a panda model that rotates based on the current time.

## Documentation and website

All documentation and other information used to be found at our website, [reactive-engine.org](http://www.reactive-engine.org), but that's gone now; now see the archived (2017-07-25) [Reactive Panda](https://web.archive.org/web/20170725062950/http://wiki.western.edu/mcis/index.php?title=Reactive_Panda_Web_Site) web site. There are also papers:

- Cleary, A., Vandenbergh, L. & Peterson, J. (2015). Reactive Game Engine Programming for STEM Outreach. In A. Decker, K. Eiselt, C. Alphonce & J. Tims (eds.), Proceedings of the 46th ACM Technical Symposium on Computer Science Education, February, : ACM
  - [doi: 10.1145/2676723.2677312](https://doi.org/10.1145/2676723.2677312)
- Peterson, J., Cleary, A. & Roe, K. (2015). PyFRP: Function Reactive Programming in Python
  [PDF](http://www.cs.jhu.edu/~roe/pyfrp-function-reactive.pdf)

## Installation

(Added 2023-10-05 by gdmcbain.)

```PowerShell
python -m venv .venv
Add-Content .git/info/exclude ".venv/", ".vscode/"
.venv/Scripts/Activate.ps1
python -m pip install -U pip
python -m pip install panda3d #https://www.panda3d.org/download/sdk-1-10-13/
python
```

```python
from PandaSRC.Panda import *
```

No good: needs `pythonfrp`. There's a package of that name at <https://github.com/WSCU/pythonfrp> but it can't be installed, lacking a pyproject.toml. Thus it's forked at <https://github.com/gdmcbain/pythonfrp>.

```PowerShell
python -m pip install -e ..\pythonfrp
```
