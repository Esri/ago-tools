#### Update web map version to 1.7x
#### Allows for opening new web maps in ArcGIS Explorer
#### Intended use is if you need to use AGX to create queries for iOS devices

import sys
sys.path.append('c:/scripts')  # Directory where utilities.py is located.  Change as needed

from agoTools.utilities import Utilities

agoUtilities = Utilities('<username>') # Replace <username> with your username.

webmapId = '<WEB MAP ID>'    # Replace with web map ID

agoUtilities.updatewebmapversionAGX(webmapId)
