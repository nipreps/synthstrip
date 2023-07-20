# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
#
# Copyright 2022 The NiPreps Developers <nipreps@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# We support and encourage derived works from this project, please read
# about our expectations at
#
#     https://www.nipreps.org/community/licensing/
#
"""SynthStrip interface."""

import os
import attr
from pathlib import Path
import pydra
import nest_asyncio
nest_asyncio.apply()

_fs_home = os.getenv("FREESURFER_HOME", None)
_default_model_path = Path(_fs_home) / "models" / "synthstrip.1.pt" if _fs_home else None

if _fs_home and not _default_model_path.exists():
    _default_model_path = Undefined

_SynthStripInputSpec = pydra.specs.SpecInfo(
    name='SynthStripInputSpec',
    fields=[
        (
            'in_file',
            attr.ib(
                type=str,
                metadata={
                    'argstr': "-i",
                    'help_string': 'Input image to skullstrip',
                    'mandatory': True,
                },
            ),
        ),
        (
            'out_file',
            str,
            {
                'argstr': "-o",
                "help_string": "Save stripped image to path",
                "output_file_template": "{in_file}_desc-brain.nii.gz",
            },
        ),
        (
            'out_mask',
            str,
            {
                'argstr': "-m",
                "help_string": "Save binary brain mask to path",
                "output_file_template": "{in_file}_desc-brain_mask.nii.gz",
            },
        ),
        (
            'use_gpu',
            bool,
            False,
            {
                'argstr': "-g",
                'help_string': 'Use the GPU',
            },
        ),
        (
            'border_mm',
            int,
            1,
            {
                'argstr': "-b",
                "help_string": "Mask border threshold in mm",
            },
        ),
        (
            'no_csf',
            bool,
            False,
            {
                'argstr': "--no-csf",
                'help_string': 'Exclude CSF from brain border',
            },
        ),
        (
            'model',
            pydra.specs.File,
            str(_default_model_path),
            {
                'argstr': "--model",
                "help_string": "File containing model's weights",
            },
        ),
        (
            'num_threads',
            int,
            0, # WHAT SHOULD BE DEFAULT FOR N_THREADS?
            {
                'argstr': "-n",
                "help_string": "Number of threads",
            },
        ),
    ],
    bases=(pydra.specs.ShellSpec,),
)

SynthStrip = pydra.ShellCommandTask(
    name='SynthStrip',
    executable="nipreps-synthstrip",
    input_spec = _SynthStripInputSpec
)
