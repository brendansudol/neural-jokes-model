"""
A script to port weights to deeplearnjs.

This script takes a checkpoint file and writes all of the
variables in the checkpoint to a directory.
"""

import json
import os
import re
import string

import tensorflow as tf


FILENAME_CHARS = string.ascii_letters + string.digits + '_'


def var_to_filename(var_name):
    chars = []

    for c in var_name:
        if c in FILENAME_CHARS:
            chars.append(c)
        elif c == '/':
            chars.append('_')

    return ''.join(chars)


def dump_checkpoints(vocab, model_name, final_model):
    print('Converting weights for js:', model_name, final_model)

    chk_fpath = os.path.expanduser('./checkpoints/{}/{}'.format(model_name, final_model))
    reader = tf.train.NewCheckpointReader(chk_fpath)
    var_to_shape_map = reader.get_variable_to_shape_map()

    remove_variables_regex = re.compile('.*Adam.*|.*beta.*')
    output_dir = './output/{}'.format(model_name)
    tf.gfile.MakeDirs(output_dir)

    manifest = {}
    var_filenames_strs = []

    for name in var_to_shape_map:
        if re.match(remove_variables_regex, name) or name in ['global_step', 'Variable']:
            print('Ignoring ' + name)
            continue

        var_filename = var_to_filename(name)
        manifest[name] = {
            'filename': var_filename,
            'shape': var_to_shape_map[name]
        }

        print('Writing variable ' + name + '...')
        tensor = reader.get_tensor(name)
        with open(os.path.join(output_dir, var_filename), 'wb') as f:
            f.write(tensor.tobytes())

        var_filenames_strs.append("\"" + var_filename + "\"")

    # save the vocab
    vocab_fpath = os.path.join(output_dir, 'vocab.json')
    print('Writing vocab to ' + vocab_fpath)
    with open(vocab_fpath, 'w') as f:
        f.write(json.dumps(vocab, indent=2, sort_keys=True))

    # save the manifest
    manifest_fpath = os.path.join(output_dir, 'manifest.json')
    print('Writing manifest to ' + manifest_fpath)
    with open(manifest_fpath, 'w') as f:
        f.write(json.dumps(manifest, indent=2, sort_keys=True))

    print('Done!')
