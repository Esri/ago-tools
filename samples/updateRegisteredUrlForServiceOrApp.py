#### Update the URL for registered map services or web applications

from agoTools.utilities import Utilities

agoUtilities = Utilities(<username>) # Replace <username> with your username.

itemId = '<ITEM ID>'    # Replace with item ID
oldUrl = '<http://oldserver.com/app>'    # Replace with old URL
newUrl = '<http://newserver.com/app>'    # Replace with new URL

agoUtilities.updateItemUrl(itemId, oldUrl, newUrl)	