"""
Sphinx plugin to run generate a gallery for notebooks
"""
import base64
import dataclasses
import json
import os
import pathlib
import random
import shutil
from textwrap import dedent

import matplotlib.image
import matplotlib.pyplot as plt
import pandas as pd
import yaml

with open('lorem_ipsum.txt') as fid:
    descriptions = fid.read().split('\n\n')


DOC_SRC = pathlib.Path(os.path.dirname(os.path.abspath(__file__))).parent
default_img_loc = DOC_SRC / '_static/images/sphinx-logo.png'
thumbnail_dir = DOC_SRC / '_static/thumbnails'
thumbnail_dir.mkdir(parents=True, exist_ok=True)


def create_thumbnail(infile, width=275, height=275, cx=0.5, cy=0.5, border=4):
    """Overwrites `infile` with a new file of the given size"""
    im = matplotlib.image.imread(infile)
    rows, cols = im.shape[:2]
    size = min(rows, cols)
    if size == cols:
        xslice = slice(0, size)
        ymin = min(max(0, int(cx * rows - size // 2)), rows - size)
        yslice = slice(ymin, ymin + size)
    else:
        yslice = slice(0, size)
        xmin = min(max(0, int(cx * cols - size // 2)), cols - size)
        xslice = slice(xmin, xmin + size)
    thumb = im[yslice, xslice]
    thumb[:border, :, :3] = thumb[-border:, :, :3] = 0
    thumb[:, :border, :3] = thumb[:, -border:, :3] = 0

    dpi = 100
    fig = plt.figure(figsize=(width / dpi, height / dpi), dpi=dpi)

    ax = fig.add_axes([0, 0, 1, 1], aspect='auto', frameon=False, xticks=[], yticks=[])
    ax.imshow(thumb, aspect='auto', resample=True, interpolation='bilinear')
    fig.savefig(infile, dpi=dpi)
    plt.close(fig)
    return fig


@dataclasses.dataclass
class NotebookInfo:
    filepath: pathlib.Path
    default_img_loc: pathlib.Path
    thumbnail_dir: pathlib.Path
    src_dir: pathlib.Path

    def __post_init__(self):
        self.thumbnail_dir.mkdir(parents=True, exist_ok=True)
        self.png_path = self.thumbnail_dir / f'{self.filepath.stem}.png'
        with open(self.filepath) as fid:
            self.json_source = json.load(fid)
            self.gen_preview()

        nb_id = f'{self.filepath.relative_to(self.src_dir).parent}/{self.filepath.stem}'
        self.info = {
            'thumbnail': f'../{self.png_path.relative_to(self.src_dir).as_posix()}',
            'notebook': f'../{self.filepath.relative_to(self.src_dir).as_posix()}',
            'title': self.extract_title(),
            'url': f'../{nb_id}.html',
            'id': nb_id,
            'description': random.choice(descriptions)[:200].strip(),
        }

    def gen_preview(self):
        preview = self.extract_preview_pic()
        if preview is not None:
            with open(self.png_path, 'wb') as buff:
                buff.write(preview)
        else:
            shutil.copy(self.default_img_loc, self.png_path)

        create_thumbnail(self.png_path)

    def extract_preview_pic(self):
        """Use the last image in the notebook as preview pic"""
        pic = None
        for cell in self.json_source['cells']:
            for output in cell.get('outputs', []):
                if 'image/png' in output.get('data', []):
                    pic = output['data']['image/png']
        if pic is not None:
            return base64.b64decode(pic)
        return None

    def extract_title(self):
        for cell in self.json_source['cells']:
            if cell['cell_type'] == 'markdown':
                rows = [row.strip() for row in cell['source'] if row.strip()]
                for row in rows:
                    if row.startswith('# '):
                        return row[2:].replace(':', '-')
        return self.filepath.stem.replace('_', ' ').replace(':', '-')


def build_gallery(srcdir, gallery, contains_notebooks):
    src_dir = pathlib.Path(srcdir)
    os.chdir(srcdir)
    target_dir = src_dir / f'{gallery}_gallery'
    image_dir = target_dir / '_thumbnails'
    image_dir.mkdir(parents=True, exist_ok=True)

    if contains_notebooks:
        notebooks_path = src_dir / 'notebooks'
        notebooks = sorted(
            [notebook for notebook in notebooks_path.glob('**/*.ipynb') if 'checkpoint' not in notebook.name]
        )
        entries = [
            NotebookInfo(note, default_img_loc=default_img_loc, thumbnail_dir=image_dir, src_dir=src_dir).info
            for note in notebooks
        ]
        df = pd.DataFrame(entries).sort_values(by=['title'])
        entries = df.to_dict(orient='records')
        with open(target_dir / f'{gallery}_gallery.yaml', 'w') as fid:
            yaml.dump(entries, fid)

        panels_body = []
        for entry in entries:
            x = f"""\
            ---
            :img-top: {entry["thumbnail"]}
            +++
            **{entry['title']}**

            {entry['description'][:50]} ...

            {{link-badge}}`{entry["url"]},"rendered-notebook",cls=badge-secondary text-white float-left p-2 mr-1`
            """

            panels_body.append(x)

        panels_body = '\n'.join(panels_body)

        gallery_content = f'''# {gallery.capitalize()} Gallery
````{{panels}}
:container: full-width
:column: text-left col-6 col-lg-4
:card: +my-2
:img-top-cls: w-75 m-auto p-2
:body: d-none

{dedent(panels_body)}
````
'''
        with open(target_dir / 'index.md', 'w') as fid:
            fid.write(dedent(gallery_content))


def main(app):
    for gallery in [('notebooks', True)]:
        build_gallery(app.builder.srcdir, gallery[0], gallery[1])


def setup(app):
    app.connect('builder-inited', main)
