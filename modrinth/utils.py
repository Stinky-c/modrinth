from furl import furl
from enum import Enum

# Replace with better url builder
class URLBuilder(furl):
    def __init__(self, url, **kwargs):
        super().__init__(url=url, **kwargs)

    def add(self, query_params: dict):
        "Custom Querry handler"
        for o in query_params:
            if query_params[o] != None:
                self.query.add({o: str(query_params[o])})
        return self


# facets - enums


class IndexEnum(Enum):
    """Search index Enum"""

    relevance = "relevance"
    downloads = "downloads"
    follows = "follows"
    newest = "newest"
    updated = "updated"


class VersionTypeEnum(Enum):
    """Version Type Enum"""

    release = "release"
    beta = "beta"
    alpha = "alpha"
