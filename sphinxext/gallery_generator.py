"""
Sphinx plugin to run generate a gallery for notebooks
"""
import base64
import dataclasses
import json
import os
import pathlib
import shutil

import matplotlib.image
import matplotlib.pyplot as plt
import pandas as pd
import yaml

DOC_SRC = pathlib.Path(os.path.dirname(os.path.abspath(__file__))).parent
default_img_loc = DOC_SRC / '_static/placeholder.png'
thumbnail_dir = DOC_SRC / '_build/thumbnails'
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
    default_img_loc: pathlib.Path = default_img_loc
    thumbnail_dir: pathlib.Path = thumbnail_dir

    def __post_init__(self):
        self.thumbnail_dir.mkdir(parents=True, exist_ok=True)
        self.png_path = self.thumbnail_dir / f'{self.filepath.stem}.png'
        with open(self.filepath) as fid:
            self.json_source = json.load(fid)
            self.gen_preview()

        nb_id = f'{self.filepath.relative_to(DOC_SRC).parent}/{self.filepath.stem}'
        self.info = {
            'thumbnail': self.png_path.relative_to(DOC_SRC).as_posix(),
            'notebook': self.filepath.relative_to(DOC_SRC).as_posix(),
            'title': self.extract_title(),
            'url': f'{nb_id}.html',
            'id': nb_id,
            'tags': list(self.filepath.relative_to(DOC_SRC / 'notebooks').parent.parts[:]),
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


def build_gallery():
    notebooks_path = DOC_SRC / 'notebooks'
    notebooks = sorted(
        [
            notebook
            for notebook in notebooks_path.glob('**/*.ipynb')
            if 'checkpoint' not in notebook.name
        ]
    )
    entries = [NotebookInfo(note).info for note in notebooks]
    df = pd.DataFrame(entries).sort_values(by=['title'])
    df.to_csv(DOC_SRC / 'gallery.csv', index=False)
    entries = df.to_dict(orient='records')
    with open(DOC_SRC / 'gallery.yaml', 'w') as fid:
        yaml.dump(entries, fid)

    s = []
    for entry in entries:
        badges = [f'{{badge}}`{badge},badge-primary`' for badge in entry['tags']]
        badges = '\n'.join(badges)
        x = f"""
---
:img-top: {entry['thumbnail']}
```{{link-button}} {entry['id']}
:type: ref
:text: {entry['title']}
:classes: btn-outline-primary btn-block stretched-link
```
+++++++

{badges}
"""

        s.append(x)

    s = ' '.join(s)

    gallery_content = f'''# Gallery
````{{panels}}
:img-top-cls: pl-5 pr-5
{s}
````
'''
    with open(DOC_SRC / 'notebook-gallery.md', 'w') as fid:
        fid.write(gallery_content)


def main(app):
    build_gallery()


def setup(app):
    app.connect('builder-inited', main)
