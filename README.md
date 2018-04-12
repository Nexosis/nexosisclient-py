## Nexosis API Client Library

[![Build Status](https://travis-ci.org/Nexosis/nexosisclient-py.svg?branch=master)](https://travis-ci.org/Nexosis/nexosisclient-py)

This software is provided as a way to include Nexosis API functionality in your own Python software.

You can read about the Nexosis API at [https://developers.nexosis.com](https://developers.nexosis.com/docs/services/98847a3fbbe64f73aa959d3cededb3af)

Install with pip:

```bash
pip install nexosisclient
```

### Version 3.0.0 Release Notes (Breaking Changes)

Each of the entity list operations for Datasets, Sessions, Models, and Imports have been changed to require a list query object instead of a set of parameters.
We added the ability to sort by various entity properties specific to each type along with a sort order for that sorted request. The query objects allow us to provide better
feedback on appropriate properties and simplify the interface to the operations.

Also note that while the date based modifiers such as *createdBefore*, or *requestedAfter*, etc. are now expected to include the word 'date' as a suffix:
- created_after_date
- created_before_date

...and so on when used in the **options** bag passed to the list query initializer. You may optionally use the properties on the queries as well. When the query
object creates a query string it will use the longer form such as *createdBeforeDate*.  The API itself will continue to accept either form if queried directly.

Finally, the date parameters may be strings but should comply with the ISO-8601 format. We are using dateutil.parser.parse when strings are provided. A failure to parse will result in a None value. Of course the safest way to get the value you want is to continue to use datetime objects.

*Pull requests are welcome*
