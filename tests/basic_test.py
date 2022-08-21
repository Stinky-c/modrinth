from modrinth import ModrinthRequestFactory
from modrinth.utils import IndexEnum
from modrinth.models import ProjectModel, FileModel, SearchResultModel, VersionModel

# INIT
base = ModrinthRequestFactory()

# GET
def test_GET():
    data = base.get("ae2")
    assert isinstance(data, ProjectModel)


# # SEARCH
def test_SEARCH():
    data = base.search(limit=3)
    assert isinstance(data, list)
    assert isinstance(data[0], SearchResultModel)


# GET VERSIONS
def test_VERSION():
    data = base.get_versions("ae2")
    assert isinstance(data, list)
    assert isinstance(data[0], VersionModel)
    assert isinstance(data[0].files[0], FileModel)

