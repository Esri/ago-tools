#### Update map service urls in webmaps

from agoTools.utilities import Utilities
agoUtilities = Utilities(<username>) # Replace <username> with your username.

webmapId = '<WEBMAP ID>'    # Replace with web map ID
oldUrl = '<http://myserver.com/arcgis/rest/services/old/MapServer>'    # Replace with old map service URL
newUrl = '<http://myserver.com/arcgis/rest/services/new/MapServer>'    # Replace with new map service URL

agoUtilities.updateWebmapService(webmapId, oldUrl, newUrl)