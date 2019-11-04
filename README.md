# lpe_manager
This is a utility for managing custom AOVs with LPEs in the Arnold rendering engine inside of Maya. It has been tested and known to work in Maya 2019, but should work in other versions as well as long as PyMel and Arnold are available.

With just a few clicks, the utility generates commonly-used AOVs for selected light groups.

## Usage
```python
from lpe_manager_ui import LPEManagerUI
LPEManagerUI()
```

A window will pop up that shows all existing light groups in the scene. If any changes are made to light groups, the window needs to be closed and reopened to refresh the list. Future versions will updated automatically.
