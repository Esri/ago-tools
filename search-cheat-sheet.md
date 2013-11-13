# Advanced Search Cheat Sheet

## Contents
* [Defaults](search-cheat-sheet.md#defaults)
* [Modifiers](search-cheat-sheet.md#modifiers)
* [Operators](search-cheat-sheet.md#operators)
* [Search Fields](search-cheat-sheet.md#search-fields)
* [Examples](search-cheat-sheet.md#examples)

## Defaults
The default search looks across several fields for items and groups.  The best match is always returned.
#### Items
The default fields are title, tags, snippet, description, accessinformation, spatialreference, type, and typekeywords.
#### Groups
The default fields are id, title, description, snippet, tags, and owner.

## Modifiers
#### Wildcards
Single and multiple character wildcard searches within single terms (not within phrase queries) are supported. The single character wildcard and the multiple character wildcard cannot be used in the same search.

* Single character wildcard search: use the `?` symbol.
* Multiple character wildcard search: use the `*` symbol.

#### Ranges
Range searches allow you to match a single field or multiple field values between the lower and upper bound. Range queries can be inclusive or exclusive of the upper and lower bounds. Inclusive range queries are denoted by square brackets. Exclusive range queries are denoted by curly brackets.

#### Boosting a Term
Boosting allows you to control the relevance of an item by boosting its term. To boost a term, use the `^` symbol with a boost factor (a number) at the end of the term you are searching. The higher the boost factor, the more relevant the term will be.

## Operators
#### AND
The `AND` operator performs matching where both terms exist in either the given field or the default fields.
#### OR
The `OR` operator links two terms and finds a match if either term exists.
#### +
Requires that the term after the `+` symbol exist somewhere in the given field or the default fields.
#### NOT
Excludes items that contain the term after `NOT`. This is equivalent to a difference using sets.
####\-
Excludes items that contain the term after the `-` symbol.

## Search Fields
####id
ID of the item, for example, `id:4e770315ad9049e7950b552aa1e40869` returns the item for that ID.  
####itemtype
Item type can be `url`, `text`, or `file`.  
####owner
Owner of the item, for example, `owner:esri` returns all content published by esri.  
####uploaded
The date uploaded, for example `uploaded: [0000001249084800000 TO 0000001249548000000]` finds all items published between August 1, 2009, 12:00AM to August 6, 2009 08:40AM. 
####title
Item title, for example, `title:"Southern California"` returns items with Southern California in the title.
####type
Type returns the type of item and is a predefined field. See [Items and item types](http://resources.arcgis.com/en/help/arcgis-rest-api/02r3/02r3000000ms000000.htm) for a listing of the different types. For example, type:map returns items with map as the type, such as map documents and map services. 
####typekeywords
Type keywords, for example, typekeywords:tool returns items with the tool type keyword such as Network Analysis or geoprocessing services. See [Items and item types](http://resources.arcgis.com/en/help/arcgis-rest-api/02r3/02r3000000ms000000.htm) for a listing of the different types. 
####description
Item description, for example, `description:California` finds all items with the term "California" in the description. 
####tags
The tag field, for example, `tags:"San Francisco"` returns items tagged with the term "San Francisco". 
####snippet
Snippet or summary of the item, for example, `snippet:"natural resources"` returns items with "natural resources" in the snippet.
####extent
The bounding rectangle of the item. For example, `extent: [-114.3458, 21.7518] - [-73.125, 44.0658]` returns items within that extent.
####spatialreference
Spatial reference, for example, `spatialreference:102100` returns items in the Web Mercator Auxiliary Sphere projection. 
####accessinformation
Access information, for example, `accessinformation:esri` returns items with "esri" as the source credit. 
####access
The access field, for example, `access:public` returns public items. This field is predefined, and the options are `public`, `private`, `org`, or `shared`. You will only see private or shared items that you can access. 
####group
The ID of the group, for example, `group:1652a410f59c4d8f98fb87b25e0a2669` returns items within the given group. 
####numratings
Number of ratings, for example, `numratings:6` returns items with six ratings. 
####numcomments
Number of comments, for example, `numcomments:[1 TO 3]` returns items that have one to three comments. 
####avgrating
Average rating, for example, `avgrating:3.5` returns items with 3.5 as the average rating. 
####culture
Culture, for example, `culture:en-US`, returns the locale of the item. The search engine treats the two parts of the culture code as two different terms, and searches for individual languages can be done. For example, `culture:en` returns all records that have an "en" in their culture code. There may be overlaps between the codes used for language and the codes used for country, for instance `fr-FR`, but if the client needs to target a code with this problem, they can pass in the complete code. 

## Examples
* Find all items created between December 1, 2009, and December 9, 2009: `created: [0000001259692864000 TO 0000001260384065000]`
* Find all items from the owners between arcgis_explorer and esri, not including arcgis_explorer and esri: `owner:{arcgis_explorer TO esri}`
* Search for "recent fires" and make "fires" be more relevant: `recent fires^5`
* Search for an item that contains the terms "recent" and "fires": `recent AND fires`
* Search for an item that contains the terms "recent fires" or "fires": `"recent fires" OR fires`
* Search for items that must contain "fires" and may contain "recent": `recent +fires`
* Search for items that contain "California" but not "Imagery": `California NOT Imagery`

[Source](http://resources.arcgis.com/en/help/arcgis-rest-api/index.html#//02r3000000mn000000)
