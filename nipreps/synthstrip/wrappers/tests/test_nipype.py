from pathlib import Path

import pytest

try:
    from nipreps.synthstrip.wrappers.nipype import SynthStrip
except ImportError:
    pytest.skip('Nipype not installed.')


@pytest.fixture
def t1w(tmp_path):
    t1w = tmp_path / 'T1w.nii.gz'
    t1w.touch()
    return t1w


@pytest.fixture
def fsdir(tmp_path):
    fs = tmp_path / 'freesurfer'
    (fs / 'models').mkdir(parents=True)
    (fs / 'models' / 'synthstrip.1.pt').touch()
    return fs


def test_nipype_synthstrip_fs(t1w, fsdir, monkeypatch):
    # First with FS environment
    monkeypatch.setenv('FREESURFER_HOME', str(fsdir))
    syn = SynthStrip(in_file=t1w)
    assert 'synthstrip.1.pt' in syn.cmdline

    # now remove the default file
    (fsdir / 'models' / 'synthstrip.1.pt').unlink()
    syn = SynthStrip(in_file=t1w)
    assert 'synthstrip.1.pt' not in syn.cmdline

    monkeypatch.delenv('FREESURFER_HOME')
    syn = SynthStrip(in_file=t1w)
    assert 'synthstrip.1.pt' not in syn.cmdline

    model = Path('model.pt')
    model.touch()
    syn = SynthStrip(in_file=t1w, model=model)
    assert 'model.pt' in syn.cmdline
    model.unlink()
