import json
import os
import typing

import frontmatter
import pydantic
from markdown_it import MarkdownIt


class Author(pydantic.BaseModel):
    name: str = 'anonymous'
    affiliation: str = None
    affiliation_url: typing.Union[str, pydantic.HttpUrl] = None
    email: typing.Union[str, pydantic.EmailStr] = None


class Submission(pydantic.BaseModel):
    title: str
    description: str
    url: pydantic.HttpUrl
    thumbnail: typing.Union[str, pydantic.HttpUrl] = None
    authors: typing.List[Author] = None
    tags: typing.Dict[str, typing.List[str]] = None


@pydantic.dataclasses.dataclass
class IssueInfo:
    gh_event_path: pydantic.FilePath
    submission: Submission = pydantic.Field(default=None)

    def __post_init_post_parse__(self):
        with open(self.gh_event_path) as f:
            self.data = json.load(f)

    def create_submission(self):
        self._get_inputs()
        self._create_submission_input()
        return self

    def _get_inputs(self):
        self.author = self.data['issue']['user']['login']
        self.title = self.data['issue']['title']
        self.body = self.data['issue']['body']

    def _create_submission_input(self):
        md = MarkdownIt()
        inputs = None
        for token in md.parse(self.body):
            if token.tag == 'code':
                inputs = frontmatter.loads(token.content).metadata
                break
        name = inputs.get('name')
        title = inputs.get('title')
        description = inputs.get('description')
        url = inputs.get('url')
        thumbnail = inputs.get('thumbnail')
        _authors = inputs.get('authors')
        authors = []
        if _authors:
            for item in _authors:
                authors.append(
                    Author(
                        name=item.get('name', 'anyonymous'),
                        affiliation=item.get('affiliation'),
                        affiliation_url=item.get('affiliation_url'),
                        email=item.get('email', ''),
                    )
                )
        else:
            authors = [Author(name='anyonymous')]
        _tags = inputs.get(
            'tags', {'packages': ['unspecified'], 'formats': ['unspecified'], 'domains': ['unspecified']}
        )
        self.submission = Submission(
            name=name, title=title, description=description, url=url, thumbnail=thumbnail, authors=authors, tags=_tags
        )


if __name__ == '__main__':

    issue = IssueInfo(gh_event_path=os.environ['GITHUB_EVENT_PATH']).create_submission()
    inputs = issue.submission.dict()
    with open('gallery-submission-input.json', 'w') as f:
        json.dump(inputs, f)
