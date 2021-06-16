import itertools
import pathlib
from textwrap import dedent

import yaml


def _tag_in_item(item, tag_str=None):
    if tag_str is None:
        return True
    all_tags = sorted(itertools.chain(*item['tags'].values()))
    return tag_str in all_tags


def _generate_sorted_tag_keys(all_items):

    key_set = set(itertools.chain(*[item['tags'].keys() for item in all_items]))
    return sorted(key_set)


def _generate_tag_set(all_items, tag_key=None):

    tag_set = set()
    for item in all_items:
        for k, e in item['tags'].items():
            if tag_key and k != tag_key:
                continue
            for t in e:
                tag_set.add(t)

    return tag_set


def _generate_tag_menu(all_items, tag_key):

    tag_set = _generate_tag_set(all_items, tag_key)
    tag_list = sorted(tag_set)

    options = ''.join(
        f'<li><a class="dropdown-item" href="/links/{tag.replace(" ", "-")}">{tag.title()}</a></li>\n'
        for tag in tag_list
    )

    return f"""
<div class="dropdown">
  <button class="btn btn-sm btn-secondary mx-1 mb-3 dropdown-toggle" type="button" id="{tag_key}Dropdown" data-bs-toggle="dropdown" aria-expanded="false">
    {tag_key.title()}
  </button>
  <ul class="dropdown-menu" aria-labelledby="{tag_key}Dropdown">
    {options}
  </ul>
</div>
"""


def _generate_menu(all_items, flt=None):

    key_list = _generate_sorted_tag_keys(all_items)
    menu_html = '<div class="d-flex flex-row"> \n'
    for tag_key in key_list:
        menu_html += _generate_tag_menu(all_items, tag_key) + '\n'
    if flt:
        menu_html += '<a type="button" class="btn btn-link" href="/links.html">Return to Full Gallery</a>\n'
    menu_html += '<a type="button" class="btn btn-link" style="position:absolute; right:0;" href="https://github.com/ProjectPythia/projectpythia.github.io/issues/new?assignees=&labels=external-links-gallery-submission&template=update-external-links-gallery.md&title=">Submit a Link</a>\n'
    menu_html += '</div>\n'
    menu_html += '<script>$(document).on("click",function(){$(".collapse").collapse("hide");}); </script>\n'
    return menu_html


def build_from_items(items, filename, display_name, menu_html):

    # Build the gallery file
    panels_body = []
    for item in items:
        if not item.get('thumbnail'):
            item['thumbnail'] = '/_static/images/ebp-logo.png'
        thumbnail = item['thumbnail']
        tag_list = sorted((itertools.chain(*item['tags'].values())))
        tags = [
            f'{{link-badge}}`"/links/{tag.replace(" ", "-")}.html",{tag},cls=badge-primary badge-pill text-light`'
            for tag in tag_list
        ]
        tags = '\n'.join(tags)

        author_strs = set()
        affiliation_strs = set()
        for a in item['authors']:
            author_name = a.get('name', 'Anonymous')
            author_email = a.get('email', None)
            if author_email:
                _str = f'[{author_name}](mailto:{author_email})'
            else:
                _str = author_name
            author_strs.add(_str)

            affiliation_name = a.get('affiliation', None)
            if affiliation_name:
                affiliation_url = a.get('affiliation_url', None)
                if affiliation_url:
                    _str = f'[{affiliation_name}]({affiliation_url})'
                else:
                    _str = affiliation_name
                affiliation_strs.add(_str)
        authors_str = f"Author: {', '.join(author_strs)}"
        if affiliation_strs:
            affiliations_str = f"Affiliation: {' '.join(affiliation_strs)}"
        else:
            affiliations_str = ''

        panels_body.append(
            f"""\
---
:img-top: {thumbnail}
+++
**{item["title"]}**

<button class="modal-btn">See Details</button>
<div class="modal">
  <div class="content">
<p>
<img src="{thumbnail}" class="m-2" style="float: right; max-width: 400px; max-height: 200px;" />

**{item["title"]}**

{authors_str}

{affiliations_str}

{item['description']}

```{{link-button}} {item["url"]}
:type: url
:text: Visit Website
:classes: btn-outline-primary btn-block
```

{tags}
</p>
  </div>
</div>

{tags}
"""
        )

    panels_body = '\n'.join(panels_body)

    panels = f"""
# {display_name}

{menu_html}

````{{panels}}
:column: text-left col-6 col-lg-4
:card: +my-2
:img-top-cls: w-75 m-auto p-2
:body: d-none

{dedent(panels_body)}
````

<div class="backdrop"></div>
<script src="/_static/custom.js"></script>
"""

    pathlib.Path(f'{filename}.md').write_text(panels)


def main(app):

    with open('links.yaml') as fid:
        all_items = yaml.safe_load(fid)

    menu_html = _generate_menu(all_items)
    build_from_items(all_items, 'links', 'Project Pythia Gallery', menu_html)

    menu_html_flt = _generate_menu(all_items, flt=True)
    tag_set = _generate_tag_set(all_items)

    for tag in tag_set:
        items = [item for item in all_items if _tag_in_item(item, tag)]
        build_from_items(items, f'links/{tag.replace(" ", "-")}', f'Project Pythia Gallery - "{tag}"', menu_html_flt)


def setup(app):
    app.connect('builder-inited', main)
