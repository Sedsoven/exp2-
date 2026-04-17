import os
from train import main


def test_main_creates_model(tmp_path):
    outdir = tmp_path / "out"
    rc = main(str(outdir))
    assert rc == 0
    model_file = outdir / "model.joblib"
    assert model_file.exists()
