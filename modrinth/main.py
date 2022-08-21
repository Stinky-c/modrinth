from dataclasses import dataclass
from .models import ProjectModel, SearchResultModel, VersionModel, FileModel
from .exceptions import *
from .utils import URLBuilder, IndexEnum
from .helper import _get, _get_u


@dataclass(init=False, frozen=True, slots=True)
class ModrinthRequestFactory:
    """
    The main class handling
    pre-init attribs
        MODRINTH_ENDPOINT: sets the endpoint, no trailing slash
        MODRINTH_TOKEN: A token used in certain requests, raises exception if needed and not provided
        REQUEST_HANDLER: Function that handles requests, check function for extra
    """

    MODRINTH_ENDPOINT = "https://api.modrinth.com/v2"  # no trailing slash
    MODRINTH_TOKEN = None  # mostly uneeded # TODO add handler for adding token
    HEADERS = {
        "User-Agent": "APIWrapperTesting/github.com/Stinky-c"
    }  # be sure to self elsewhere

    def get(self, id: str) -> ProjectModel:
        endpoint = f"{self.MODRINTH_ENDPOINT}/project/{id}"
        return ProjectModel(
            **_get(endpoint, self.HEADERS), api_url=endpoint, headers=self.HEADERS
        )

    def get_versions(self, id: str) -> list[VersionModel]:
        # write shortcut into main class
        endpoint = f"{self.MODRINTH_ENDPOINT}/project/{id}/version"
        g = []
        data = _get(endpoint, self.HEADERS)

        for i in data:
            g.append(
                VersionModel(
                    **{
                        **i,
                        "files": [
                            FileModel(**c, headers=self.HEADERS, api_url=endpoint)
                            for c in i["files"]
                        ],
                    },
                    headers=self.HEADERS,
                    api_url=endpoint,
                )
            )
        return g

    def get_version_id(self, version_id: str):
        endpoint = f"{self.MODRINTH_ENDPOINT}/version/{version_id}"
        data = _get(endpoint, self.HEADERS)
        return VersionModel(**data, api_url=endpoint, headers=self.HEADERS)

    def _search(
        self,
        query: str = None,
        index: IndexEnum = None,
        offset: int = None,
        limit: int = 20,
    ) -> list[SearchResultModel]:
        # TODO - filters, facets

        endpoint = URLBuilder(self.MODRINTH_ENDPOINT + "/search")
        urldict = {
            "query": query,
            # "facets": facets,
            "index": index,
            "offset": offset,
            "limit": limit,
        }
        endpoint.add(urldict)
        return _get_u(endpoint, self.HEADERS)

    def search(
        self,
        query: str = None,
        index: IndexEnum = None,
        offset: int = None,
        limit: int = 20,
    ) -> list[SearchResultModel]:
        """
        spec docs: https://docs.modrinth.com/api-spec/#tag/projects/operation/searchProjects
        """
        # TODO - filters, facets

        data, endpoint = self._search(
            query=query, index=index, offset=offset, limit=limit
        )

        g = []
        for i in data["hits"]:
            g.append(SearchResultModel(**i, api_url=endpoint, headers=self.HEADERS))
        return g

    def search_gen(
        self,
        query: str = None,
        index: IndexEnum = None,
        offset: int = None,
        limit: int = 20,
    ) -> list[SearchResultModel]:
        """
        spec docs: https://docs.modrinth.com/api-spec/#tag/projects/operation/searchProjects
        A search generator function
        """
        # TODO - filters, facets

        data, endpoint = self._search(
            query=query, index=index, offset=offset, limit=limit
        )

        for i in data["hits"]:
            yield SearchResultModel(**i, api_url=endpoint, headers=self.HEADERS)
