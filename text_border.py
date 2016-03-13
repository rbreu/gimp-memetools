#!/usr/bin/env python

import gimpfu
from gimpfu import gimp, pdb


def python_text_border(image, drawable, thickness=5, colour=(0, 0, 0)):
    """The plugin's main function."""

    text_layer = image.active_layer
    layer_name = text_layer.name
    pdb.gimp_image_select_item(image, 2, text_layer)
    pdb.gimp_selection_grow(image, thickness)
    border_layer = gimp.Layer(
        image, 'border', image.width, image.height, gimpfu.RGBA_IMAGE, 100,
        gimpfu.NORMAL_MODE)
    position = pdb.gimp_image_get_layer_position(image, text_layer)
    image.add_layer(border_layer, position + 1)

    old_fg = gimp.get_foreground()
    gimp.set_foreground(colour)
    pdb.gimp_edit_fill(border_layer, gimpfu.FOREGROUND_FILL)
    gimp.set_foreground(old_fg)

    layer = pdb.gimp_image_merge_down(image, text_layer, 0)
    pdb.gimp_layer_set_name(layer, layer_name)




gimpfu.register(
    'python_text_border',
    'Creates a border around text.',
    'Creates a border around text.',
    'Rebecca Breu',
    '2016 Rebecca Breu, GPLv3',
    '12 March 2016',
    '<Image>/Layer/Text/Add text border...',
    'RGBA',
    [
        (gimpfu.PF_INT,
         'thickness',
         'Border thickness (pixel)',
         5),
        (gimpfu.PF_COLOUR,
         'colour',
         'Border colour',
         (0, 0, 0)),
    ],
    [],
    python_text_border,
)

gimpfu.main()
