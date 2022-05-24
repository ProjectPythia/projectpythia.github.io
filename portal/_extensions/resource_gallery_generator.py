import yaml

from gallery_generator import build_from_items, generate_menu


def main(app):

    with open('resource_gallery.yaml') as fid:
        all_items = yaml.safe_load(fid)

    title = 'Pythia Resource Gallery'
    submit_btn_link = 'https://github.com/ProjectPythia/projectpythia.github.io/issues/new?assignees=&labels=resource-gallery-submission&template=update-resource-gallery.md&title='
    submit_btn_txt = 'Submit a new resource'
    menu_html = generate_menu(all_items, submit_btn_txt=submit_btn_txt, submit_btn_link=submit_btn_link)
    build_from_items(all_items, 'resource-gallery', title=title, menu_html=menu_html)


def setup(app):
    app.connect('builder-inited', main)
