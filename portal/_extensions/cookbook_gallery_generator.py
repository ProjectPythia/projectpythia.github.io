from gallery_generator import build_from_items, generate_menu


def main(app):

    with open('cookbook_gallery.yaml') as fid:
        all_items = yaml.safe_load(fid)

    title = 'Pythia Cookbooks Gallery'
    subtitle = 'Pythia Cookbooks provide example workflows on more advanced and domain-specific problems developed by the Pythia community. Cookbooks build on top of skills you learn in Pythia Foundations.'
    menu_html = generate_menu(all_items)
    build_from_items(all_items, 'cookbook-gallery', title=title, subtitle=subtitle)


def setup(app):
    app.connect('builder-inited', main)
