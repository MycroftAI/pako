# Pako

*The universal package manager library*

Often, scripts need to install system dependencies using the native package manager of the user's
 OS. Typically, this is solved by having some bash script that runs `apt-get`, assuming the user 
 is on Ubuntu. Smarter scripts use hand crafted code to detect the user's platform and aggregate 
 a set of dependencies on a few of the more popular platforms. Our approach is different:
 
 ```bash
pako install libgdbm-devel sdl2-dev
```

On Ubuntu, this command will run:
```bash
sudo apt-get install -y libgdbm-dev libsdl2-dev
```

However, on Solus, this will run:
```bash
sudo eopkg install -y gdbm-devel sdl2-devel
```

It works as follows:
 - Parse package format (devel/debug/normal library or executable)
 - Look up package managers that exist in PATH
 - Format parsed package with common package convention of package manager

## Installation

```bash
pip3 install pako
```

## Usage
Command line:
```
pako (install|update) [package] [-t, --type format]
```

Python bindings:
```python
from pako import PakoManager, PackageFormat

manager = PakoManager()
manager.update()
manager.install(['gdbm-dev', 'sdl2-dev'])
manager.install(['ssl-dev'], overrides={'eopkg': ['openssl-devel']})
```

## Help Wanted

This tool can improve to fit a lot of use cases. Feel free to create an issue or pull request for
 new features and improvements. For instance, we need to figure out the best way to handle cases 
 where a simple package format won't find the appropriate package.

### Add Your Package Manager

Add your package manager by adding another data block to the dict object in 
`pako/package_manager_data.py`.
