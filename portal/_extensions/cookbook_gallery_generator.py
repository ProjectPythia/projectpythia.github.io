import itertools
import pathlib
from textwrap import dedent

import yaml
from truncatehtml import truncate


def build_from_items(items, filename, title='Gallery', subtitle=None, menu_html='', max_descr_len=300):

    # Build the gallery file
    panels_body = []
    for item in items:
        if not item.get('thumbnail'):
            item['thumbnail'] = '/_static/images/ebp-logo.png'
        thumbnail = item['thumbnail']

        author_strs = set()
        institution_strs = set()
        for a in item['authors']:
            author_name = a.get('name', 'Anonymous')
            author_email = a.get('email', None)
            if author_email:
                _str = f'<a href="mailto:{author_email}">{author_name}</a>'
            else:
                _str = author_name
            author_strs.add(_str)

            institution_name = a.get('institution', None)
            if institution_name:
                institution_url = a.get('institution_url', None)
                if institution_url:
                    _str = f'<a href="{institution_url}">{institution_name}</a>'
                else:
                    _str = institution_name
                institution_strs.add(_str)

        authors_str = f"<strong>Author:</strong> {', '.join(author_strs)}"
        if institution_strs:
            institutions_str = f"<strong>Institution:</strong> {' '.join(institution_strs)}"
        else:
            institutions_str = ''

        ellipsis_str = '<a class="modal-btn"> ... more</a>'
        short_description = truncate(item['description'], max_descr_len, ellipsis=ellipsis_str)

        if ellipsis_str in short_description:
            modal_str = f"""
<div class="modal">
<div class="content">
<img src="{thumbnail}" class="modal-img" />
<h3 class="display-3">{item["title"]}</h3>
{authors_str}
<br/>
{institutions_str}
<p class="my-2">{item['description']}</p>
<p class="my-2">{tags}</p>
<p class="mt-3 mb-0"><a href="{item["url"]}" class="btn btn-outline-primary btn-block">Visit Website</a></p>
</div>
</div>
"""
        else:
            modal_str = ''

        panels_body.append(
            f"""\
---
:column:

<div class="d-flex gallery-card">
<img src="{thumbnail}" class="gallery-thumbnail" />
<div class="container">
<a href="{item["url"]}" class="text-decoration-none"><h4 class="display-4 p-0">{item["title"]}</h4></a>
<p class="card-subtitle">{authors_str}<br/>{institutions_str}</p>
<p class="my-2">{short_description}</p>
</div>
</div>
{modal_str}

"""
        )

    panels_body = '\n'.join(panels_body)

    if subtitle:
        stitle = f'<span class="display-3">Displaying "{subtitle}" tags</span>'
    else:
        stitle = ''

    panels = f"""
# {title}

{stitle}

{menu_html}

````{{panels}}
:column: col-12
:card: +mb-4 w-100
:header: d-none
:body: p-3 m-0
:footer: p-1

{dedent(panels_body)}
````

<div class="modal-backdrop"></div>
<script src="/_static/custom.js"></script>
"""

    pathlib.Path(f'{filename}.md').write_text(panels)


def main(app):

    with open('cookbook_gallery.yaml') as fid:
        all_items = yaml.safe_load(fid)

    title = 'Pythia Cookbooks Gallery'
    menu_html = _generate_menu(all_items)
    build_from_items(all_items, 'cookbook-gallery', title=title, menu_html=menu_html)


def setup(app):
    app.connect('builder-inited', main)
