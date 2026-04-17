# Experiment Report — Iris classification

- Dataset: Iris (scikit-learn builtin)
- Model: RandomForestClassifier (n_estimators=50)
- Test accuracy: 1.0000 (measured on held-out 20% split)

How to reproduce (local):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python train.py
pytest -q
```

Artifacts produced:
- `outputs/model.joblib` — trained model
- `tests/test_train.py` — basic unit test verifying model file creation

Quick demo:

```powershell
python predict.py
# prints a sample prediction and class probabilities
```

What I did:
- Implemented a simple training script and unit test.
- Added GitHub Actions workflow to submit an Azure ML job.
- Added CI artifact upload so the trained model (if present) is attached to workflow runs.

What to show your teacher:
- Link to the GitHub repository (code and `report.md`).
- Show run logs or download the model artifact from the Actions run (Actions → latest run → Artifacts).
- Optionally run `python train.py` live and show `outputs/model.joblib`.
