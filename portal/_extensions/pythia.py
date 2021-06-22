from bs4 import BeautifulSoup as bs
from sphinx.application import Sphinx


def add_functions_to_context(app, pagename, templatename, context, doctree):
    def denest_sections(html):
        soup = bs(html, 'html.parser')

        sections = []
        for h1 in soup.find_all(['h1']):
            sections.append(h1.parent)
            for child in h1.parent.children:
                if (child.name == 'section') or (child.name == 'div' and 'section' in child['class']):
                    sections.append(child.extract())

        return '\n'.join(str(s) for s in sections)

    def bootstrapify(html):
        soup = bs(html, 'html.parser')

        for s in soup.select('section,div.section'):
            h = s.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
            if not h:
                continue

            i = h.name[-1]

            h['class'] = [f'display-{i}'] + h.get('class', [])

            if h.name in ['h1', 'h2']:
                s.wrap(soup.new_tag('div', **{'class': f'container-fluid sectionwrapper-{i}'}))
                s.wrap(soup.new_tag('div', **{'class': f'container section-{i}'}))

            if h.name == 'h2':
                h.wrap(soup.new_tag('div', **{'class': 'section-title-wrapper'}))
                h.wrap(soup.new_tag('div', **{'class': 'section-title'}))

        return str(soup)

    context['bootstrapify'] = bootstrapify
    context['denest_sections'] = denest_sections


def setup(app: Sphinx):
    app.require_sphinx('3.5')
    app.connect('html-page-context', add_functions_to_context)

    return {
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
