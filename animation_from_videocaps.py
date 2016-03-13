#!/usr/bin/env python

import gimpfu
from gimpfu import gimp, pdb


def python_animation_from_videocaps(image, drawable, fps=24, reduce_by=4,
                                    text_mode='none', text_layer=None):
    """The plugin's main function."""

    gimpfu.gimp.progress_init('Working on frames...')

    # Reduce frames
    delay = int(1000 / fps * reduce_by)
    for i, layer in enumerate(image.layers[:]):
        if i % reduce_by == 0:
            layer.name = '%s (%sms)' % (layer.name, delay)
        else:
            pdb.gimp_image_remove_layer(image, layer)

    gimpfu.gimp.progress_update(0.5)

    # Add text
    if text_mode != 'none' and text_layer.image == image:
        pdb.gimp_layer_resize_to_image_size(text_layer)
        pdb.gimp_edit_copy(text_layer)
        layers = image.layers[::2] if text_mode == 'blink' else image.layers
        for i, layer in enumerate(layers):
            selection = pdb.gimp_edit_paste(layer, True)
            pdb.gimp_floating_sel_anchor(selection)
        pdb.gimp_image_remove_layer(image, text_layer)

    gimpfu.gimp.progress_update(1)


gimpfu.register(
    'python_animation_from_videocaps',
    'Helps preparing an animation from video screencaps.',
    'Helps preparing an animation from video screencaps.',
    'Rebecca Breu',
    '2016 Rebecca Breu, GPLv3',
    '13 March 2016',
    '<Image>/Filters/Animation/Animators/From video screencaps...',
    '*',
    [
        (gimpfu.PF_INT,
         'fps',
         'Frames per second of source video',
         24),
        (gimpfu.PF_SLIDER,
         'reduce_by',
         'Keep every n-th frame',
         4,
         (1, 12, 1)),
        (gimpfu.PF_RADIO,
         'text_mode',
         'Add text?',
         'none',
         (('No text', 'none'),
          ('Regular text', 'regular'),
          ('Blinking text', 'blink')),
        ),
        (gimpfu.PF_LAYER,
         'text_layer',
         'Text layer',
         None),
    ],
    [],
    python_animation_from_videocaps,
)

gimpfu.main()
