from dataclasses import dataclass
from datetime import date
from .helper import _get, _download


@dataclass(kw_only=True, frozen=True, slots=True)
class BaseModel:  # keep miminal
    api_url: str
    headers: dict


@dataclass(kw_only=True, frozen=True, slots=True)
class FileModel(BaseModel):
    hashes: dict
    url: str
    filename: str
    primary: bool
    size: int

    def download(self) -> bytes:  # TODO
        return _download(self.url, self.headers)


@dataclass(kw_only=True, frozen=True, slots=True)
class VersionModel(BaseModel):
    name: str
    version_number: str
    changelog: str
    dependencies: list[dict]
    game_versions: list[str]
    version_type: str
    loaders: list[str]
    featured: bool
    id: str
    project_id: str
    author_id: str
    date_published: date
    downloads: int
    changelog_url: str | None
    files: list[FileModel]


@dataclass(kw_only=True, frozen=True, slots=True)
class ProjectModel(BaseModel):
    slug: str
    title: str
    description: str
    categories: list[str]
    client_side: str
    server_side: str
    body: str
    issues_url: str
    source_url: str
    wiki_url: str
    discord_url: str
    donation_urls: list[dict]
    project_type: str
    downloads: int
    icon_url: str
    id: str
    team: str
    body_url: str
    moderator_message: None
    published: str
    updated: str
    followers: int
    status: str
    license: dict
    versions: list[str]
    gallery: list[dict]
    approved: str
    additional_categories: list[str]


@dataclass(kw_only=True, frozen=True, slots=True)
class SearchResultModel(BaseModel):
    slug: str
    title: str
    description: str
    categories: list[str]
    client_side: str
    server_side: str
    project_type: str
    downloads: int
    icon_url: str
    project_id: str
    display_categories: list[str]
    author: str
    versions: list[str]
    follows: int
    date_created: date
    date_modified: date
    latest_version: str
    license: str
    gallery: list[str]

    def get(self) -> ProjectModel:
        """Shortcut to returning a more complex Project"""
        url = "https://api.modrinth.com/v2/project/" + self.slug
        return ProjectModel(
            **_get(url, headers=self.headers), headers=self.headers, api_url=url
        )
