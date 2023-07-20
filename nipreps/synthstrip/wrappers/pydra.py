import nest_asyncio
nest_asyncio.apply()
import pydra
import os
import attr

_fs_home = os.getenv("FREESURFER_HOME", None)
_default_model_path = Path(_fs_home) / "models" / "synthstrip.1.pt" if _fs_home else None


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
            # MAKE DEFAULT HERE BASED ON 'in_file'
            {
                'argstr': "-o",
                "help_string": "Save stripped image to path",
            },
        ),
        (
            'out_mask',
            str,
            # MAKE DEFAULT HERE BASED ON 'in_file'
            {
                'argstr': "-m",
                "help_string": "Save binary brain mask to path",
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
                "help_string": "file containing model's weights",
            },
        )
    ],
    bases=(pydra.specs.ShellSpec,),
)

_SynthStripOutputSpec = pydra.specs.SpecInfo(
    name='SynthStripOutputSpec',
    fields=[
        (
            'out_file',
            pydra.specs.File,
            'tmp' # SET THIS TO 'out_file' of input_spec
        ),
        (
            'out_mask',
            pydra.specs.File,
            'tmp' # SET THIS TO 'out_mask' of input_spec
        ),
    ],

    bases=(pydra.specs.ShellOutSpec,),
)

SynthStrip = pydra.ShellCommandTask(
    name='SynthStrip', executable="nipreps-synthstrip", input_spec = _SynthStripInputSpec, output_spec=_SynthStripOutputSpec
)
