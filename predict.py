import joblib
import os
from sklearn.datasets import load_iris


def main(model_path: str = "outputs/model.joblib"):
    if not os.path.exists(model_path):
        print(f"Model not found at {model_path}. Run `python train.py` first.")
        return 1

    clf = joblib.load(model_path)
    data = load_iris()
    sample = data.data[0:1]
    pred = clf.predict(sample)
    probs = clf.predict_proba(sample)
    print(f"Sample features: {sample.tolist()}")
    print(f"Predicted class: {pred[0]} ({data.target_names[pred[0]]})")
    print(f"Probabilities: {probs[0].tolist()}" )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
