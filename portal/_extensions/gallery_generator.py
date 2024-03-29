import itertools
import pathlib

from truncatehtml import truncate


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
        f'<li><label class="dropdown-item checkbox {tag_key}"><input type="checkbox" rel={tag.replace(" ", "-")} onchange="change();">&nbsp;{tag.capitalize()}</label></li>'
        for tag in tag_list
    )

    return f"""
<div class="dropdown">

<button class="btn btn-sm btn-outline-primary mx-1 dropdown-toggle" type="button" id="{tag_key}Dropdown" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
{tag_key.title()}
</button>
<ul class="dropdown-menu" aria-labelledby="{tag_key}Dropdown">
{options}
</ul>
</div>
"""


def generate_menu(all_items, submit_btn_txt=None, submit_btn_link=None):
    key_list = _generate_sorted_tag_keys(all_items)

    menu_html = '<div class="d-sm-flex mt-3 mb-4">\n'
    menu_html += '<div class="d-flex gallery-menu">\n'
    if submit_btn_txt:
        menu_html += f'<div><a role="button" class="btn btn-primary btn-sm mx-1" href={submit_btn_link}>{submit_btn_txt}</a></div>\n'
    menu_html += '</div>\n'
    menu_html += '<div class="ml-auto d-flex">\n'
    menu_html += '<div><button class="btn btn-link btn-sm mx-1" onclick="clearCbs()">Clear all filters</button></div>\n'
    for tag_key in key_list:
        menu_html += _generate_tag_menu(all_items, tag_key) + '\n'
    menu_html += '</div>\n'
    menu_html += '</div>\n'
    menu_html += '<script>$(document).on("click",function(){$(".collapse").collapse("hide");}); </script>\n'
    return menu_html


def build_from_items(items, filename, title='Gallery', subtitle=None, subtext=None, menu_html='', max_descr_len=300):
    # Build the gallery file
    panels_body = []
    for item in items:
        if not item.get('thumbnail'):
            item['thumbnail'] = '_static/images/ebp-logo.png'
        thumbnail = item['thumbnail'][1:] if item['thumbnail'].startswith('/') else item['thumbnail']
        tag_list = sorted((itertools.chain(*item['tags'].values())))
        tag_list_f = [tag.replace(' ', '-') for tag in tag_list]

        tags = [f'<span class="badge bg-primary">{tag}</span>' for tag in tag_list_f]
        tags = '\n'.join(tags)

        # tag_class_str = ' '.join(tag_list_f)

        author_strs = set()
        affiliation_strs = set()
        for a in item['authors']:
            author_name = a.get('name', 'Anonymous')
            author_email = a.get('email', None)
            if author_email:
                _str = f'<a href="mailto:{author_email}">{author_name}</a>'
            else:
                _str = author_name
            author_strs.add(_str)

            affiliation_name = a.get('affiliation', None)
            if affiliation_name:
                affiliation_url = a.get('affiliation_url', None)
                if affiliation_url:
                    _str = f'<a href="{affiliation_url}">{affiliation_name}</a>'
                else:
                    _str = affiliation_name
                affiliation_strs.add(_str)

        authors_str = f"<strong>Author:</strong> {', '.join(author_strs)}"
        if affiliation_strs:
            affiliations_str = f"<strong>Affiliation:</strong> {' '.join(affiliation_strs)}"
        else:
            affiliations_str = ''

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
            {affiliations_str}
            <p class="my-2">{item['description']}</p>
            <p class="my-2">{tags}</p>
            <p class="mt-3 mb-0"><a href="{item["url"]}" class="btn btn-outline-primary btn-block">Visit Website</a></p>
            </div>
            </div>
            """
            modal_str = '\n'.join([m.lstrip() for m in modal_str.split('\n')])
        else:
            modal_str = ''
        new_panel = f"""\
            :::{{grid-item-card}}
            :shadow: md
            :class-footer: card-footer
            <div class="d-flex gallery-card">
            <img src="{thumbnail}" class="gallery-thumbnail" />
            <div class="container">
            <a href="{item["url"]}" class="text-decoration-none"><h4 class="display-4 p-0">{item["title"]}</h4></a>
            <p class="card-subtitle">{authors_str}<br/>{affiliations_str}</p>
            <p class="my-2">{short_description} </p>
            </div>
            </div>
            {modal_str}

            +++

            {tags}

            :::

            """

        print(thumbnail)
        panels_body.append('\n'.join([m.lstrip() for m in new_panel.split('\n')]))

    panels_body = '\n'.join(panels_body)

    stitle = f'#### {subtitle}' if subtitle else ''
    stext = subtext if subtext else ''

    panels = f"""\
        {title}
        {'=' * len(title)}

        {stitle}
        {stext}

        {menu_html}

        ::::{{grid}} 1
        :gutter: 4

        {panels_body}
        ````

        <div class="modal-backdrop"></div>
        <script src="/_static/custom.js"></script>
    """

    panels = '\n'.join([m.lstrip() for m in panels.split('\n')])

    pathlib.Path(f'{filename}.md').write_text(panels)
