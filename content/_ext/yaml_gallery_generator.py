import yaml
from textwrap import dedent
import pathlib


def _tag_in_item(item, tag_str=None):
    if tag_str is None:
        return True
    all_tags = []
    for k, e in item['tags'].items():
        all_tags.extend(e)
    return tag_str in all_tags


def _generate_sorted_tag_keys(all_items):

    key_set = set()
    for item in all_items:
        for k, e in item['tags'].items():
            key_set.add(k)
    
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

    hrefs = ''.join(f'<a class="dropdown-item" href="/pages/links/{tag.replace(" ", "-")}.html">{tag.title()}</a> \n' for tag in tag_list)

    return f"""
<div class="dropdown">
<button class="btn btn-sm btn-primary m-2 dropdown-toggle" data-toggle="collapse" data-target="#{tag_key}" aria-haspopup="true">{tag_key.title()}</button>
<div id="{tag_key}" class="collapse dropdown-menu">
{hrefs}
</div>
</div>
"""


def _generate_menu(all_items, flt=None):
    
    key_list = _generate_sorted_tag_keys(all_items)
    menu_html='<div class="d-flex flex-row">' + '\n'
    for tag_key in key_list:
        menu_html += _generate_tag_menu(all_items, tag_key) + '\n'
    if flt:
        menu_html += '<a type="button" class="btn btn-link" href="/pages/links.html">Return to Full Gallery</a>' + '\n'
    menu_html += '<a type="button" class="btn btn-link" style="position:absolute; right:0;" href="test.html">Submit a Link</a>' + '\n'
    menu_html += '</div>' + '\n'
    menu_html += "<script> $(document).on('click',function(){$('.collapse').collapse('hide');}); </script>" + '\n'
    return menu_html


def build_from_items(items, filename, display_name, menu_html):

    # Build the gallery file
    panels_body = []
    for item in items:
        if not item.get('thumbnail'):
            item['thumbnail'] = '/_static/images/ebp-logo.png'
        thumbnail = item['thumbnail']

        tag_set = set()
        for k, e in item['tags'].items():
            for t in e:
                tag_set.add(t)

        tag_list = sorted(tag_set)
        tags = [f'{{link-badge}}`"/pages/links/{tag.replace(" ", "-")}.html",{tag},cls=badge-primary badge-pill text-light`' for tag in tag_list]
        tags = '\n'.join(tags)

        authors = [a.get("name", "anonymous") for a in item['authors']]

        if len(authors) == 1:
            authors_str = f'Created by: {authors[0]}'
        elif len(authors) == 2:
            authors_str = f'Created by: {authors[0]} and {authors[1]}'

        email = [a.get("email", None) for a in item['authors']][0]
        email_str = '' if email is None else f'Email: {email}'

        affiliation = [a.get("affiliation", None) for a in item['authors']][0]
        affiliation_str = '' if affiliation is None else f'Affiliation: {affiliation}'

        affiliation_url = [a.get("affiliation_url", None) for a in item['authors']][0]
        affiliation_url_str = (
            '' 
            if affiliation_url is None 
            else f'{affiliation} Site: <{affiliation_url}>'
        )

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
<img src={thumbnail} />

**{item["title"]}**

{authors_str}

{email_str}

{affiliation_str}

{affiliation_url_str}

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
""")

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
<script src="/_static/custom.js"> </script>
"""

    pathlib.Path(f'pages/{filename}.md').write_text(panels)



def main(app):

    with open('links.yaml') as fid:
        all_items = yaml.safe_load(fid)

    menu_html = _generate_menu(all_items)
    build_from_items(all_items, 'links', 'External Links Gallery', menu_html)

    menu_html_flt = _generate_menu(all_items, flt=True)
    tag_set = _generate_tag_set(all_items)

    for tag in tag_set:
        items = [item for item in all_items if _tag_in_item(item, tag)]
        build_from_items(items, f'links/{tag.replace(" ", "-")}', f'External Links Gallery - "{tag}"', menu_html_flt)


def setup(app):
    app.connect('builder-inited', main)
