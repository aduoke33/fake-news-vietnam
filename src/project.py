"""End-to-end Vietnamese fake-news text classification project utilities."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import yaml

ROOT = Path(__file__).resolve().parents[1]
CONFIG = yaml.safe_load((ROOT / "config.yaml").read_text(encoding="utf-8"))
SEED = int(CONFIG["seed"])
LABELS = {"real": "Real", "true": "Real", "thật": "Real", "that": "Real", "0": "Real",
          "fake": "Fake", "false": "Fake", "giả": "Fake", "gia": "Fake", "1": "Fake"}
TEXT_HINTS = ("text", "content", "article", "news", "body", "title", "headline", "content", "nội dung", "tiêu đề", "tin")
LABEL_HINTS = ("label", "class", "target", "y", "is_fake", "fake", "truth", "nhãn", "loại")


def normalize_label(value: Any) -> str:
    key = str(value).strip().lower()
    if key in LABELS:
        return LABELS[key]
    # Support common numeric labels stored as strings/floats.
    if key in {"0.0", "1.0"}:
        return "Fake" if key == "1.0" else "Real"
    raise ValueError(f"Nhãn không nhận diện được: {value!r}. Hãy ánh xạ về Real/Fake trong dữ liệu.")


def _pick_label_column(df: pd.DataFrame) -> str:
    cols = list(df.columns)
    ranked = sorted(cols, key=lambda c: (not any(h in str(c).lower() for h in LABEL_HINTS), str(c)))
    for col in ranked:
        vals = set(df[col].dropna().astype(str).str.strip().str.lower().unique())
        if vals and len(vals) <= 5 and vals.issubset(set(LABELS) | {"0.0", "1.0"}):
            return col
    raise ValueError(f"Không tìm thấy cột nhãn Real/Fake. Các cột hiện có: {cols}")


def load_split(path: Path, has_label: bool = True) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Thiếu dữ liệu: {path}\nTải train_data.csv và test_data.csv theo README.")
    df = pd.read_csv(path)
    if df.empty:
        raise ValueError(f"File rỗng: {path}")
    df.columns = [str(c).strip() for c in df.columns]
    label_col = _pick_label_column(df) if has_label else None
    text_cols = [c for c in df.columns if c != label_col and any(h in c.lower() for h in TEXT_HINTS)]
    if not text_cols:
        text_cols = [c for c in df.columns if c != label_col and (df[c].dtype == "object" or pd.api.types.is_string_dtype(df[c]))]
    if not text_cols:
        raise ValueError(f"Không tìm thấy cột văn bản trong {path}. Cột: {list(df.columns)}")
    # Use one input field where possible; join title/body fields when present.
    df["text"] = df[text_cols].fillna("").astype(str).agg(" ".join, axis=1).map(lambda s: re.sub(r"\s+", " ", s).strip())
    df = df[df["text"].str.len() > 0].copy()
    if has_label:
        df["label"] = df[label_col].map(normalize_label)
        df = df[df["label"].isin(["Real", "Fake"])].copy()
    # Normalised key for deduplication: lowercase + collapse non-word chars.
    # On this dataset the text is already lowercase, so the normalisation
    # only collapses punctuation/whitespace differences.  The column stores
    # the full normalised string, not a cryptographic hash.
    df["text_norm"] = df["text"].str.lower().str.replace(r"\W+", " ", regex=True).str.strip()
    return df.reset_index(drop=True)


def make_pipeline(name: str):
    from sklearn.dummy import DummyClassifier
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression
    from sklearn.naive_bayes import MultinomialNB
    from sklearn.pipeline import Pipeline
    from sklearn.svm import LinearSVC
    # token_pattern splits on whitespace/punctuation boundaries.
    # For Vietnamese, each "token" is a syllable, not a linguistic word
    # (e.g. "Việt Nam" → two tokens "việt", "nam").  So unigrams and
    # bigrams here are syllable-level n-grams.  A Vietnamese word
    # segmenter (e.g. underthesea) would be needed for true word-level
    # tokenization, but is not used in this baseline.
    vec = TfidfVectorizer(ngram_range=(1, 2), min_df=1, max_features=int(CONFIG["text_max_features"]),
                          strip_accents=None, sublinear_tf=True, lowercase=True,
                          token_pattern=r"(?u)\b\w+\b")
    clf = {
        "dummy": DummyClassifier(strategy="most_frequent"),
        "naive_bayes": MultinomialNB(alpha=0.5),
        "logistic_regression": LogisticRegression(C=2.0, max_iter=2000, class_weight="balanced", random_state=SEED),
        "linear_svm": LinearSVC(C=1.0, class_weight="balanced", random_state=SEED),
    }[name]
    return Pipeline([("tfidf", vec), ("classifier", clf)])


def metrics_for(y_true, y_pred, scores=None) -> dict:
    from sklearn.metrics import (accuracy_score, f1_score, precision_score,
                                 recall_score, roc_auc_score)
    out = {"accuracy": float(accuracy_score(y_true, y_pred)),
           "precision_macro": float(precision_score(y_true, y_pred, average="macro", zero_division=0)),
           "recall_macro": float(recall_score(y_true, y_pred, average="macro", zero_division=0)),
           "f1_macro": float(f1_score(y_true, y_pred, average="macro", zero_division=0)),
           "precision_fake": float(precision_score(y_true, y_pred, pos_label="Fake", zero_division=0)),
           "recall_fake": float(recall_score(y_true, y_pred, pos_label="Fake", zero_division=0)),
           "f1_fake": float(f1_score(y_true, y_pred, pos_label="Fake", zero_division=0))}
    if scores is not None and len(set(y_true)) == 2:
        out["roc_auc"] = float(roc_auc_score(np.asarray(y_true) == "Fake", scores))
    return out


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def eda() -> None:
    train_path = ROOT / CONFIG["dataset"]["train_file"]
    test_path = ROOT / CONFIG["dataset"]["test_file"]
    train, test = load_split(train_path), load_split(test_path)
    # The official split is retained. Report cross-split exact duplicates because these inflate scores.
    train_groups = train.groupby("text_norm").agg(rows=("label", "size"), labels=("label", "nunique"))
    test_groups = test.groupby("text_norm").agg(rows=("label", "size"), labels=("label", "nunique"))
    overlap_norms = set(train.text_norm) & set(test.text_norm)
    clean_test = test.drop_duplicates("text_norm", keep="first")
    clean_train = train.drop_duplicates("text_norm", keep="first")
    clean_train = clean_train.loc[~clean_train.text_norm.isin(set(clean_test.text_norm))]
    overlap_rows = train.drop_duplicates("text_norm").loc[lambda d: d.text_norm.isin(overlap_norms)]
    stats = {"train_rows_after_empty_filter": len(train), "test_rows_after_empty_filter": len(test),
             "train_label_counts": train.label.value_counts().to_dict(), "test_label_counts": test.label.value_counts().to_dict(),
             "missing_text_train": int(train.text.isna().sum()), "duplicate_text_train": int(train.text_norm.duplicated().sum()),
             "train_unique_texts": int(train.text_norm.nunique()),
             "train_duplicate_groups": int((train_groups.rows > 1).sum()),
             "train_conflicting_duplicate_groups": int((train_groups.labels > 1).sum()),
             "test_unique_texts": int(test.text_norm.nunique()),
             "test_duplicate_rows_removed_if_deduplicated": int(test.text_norm.duplicated().sum()),
             "test_conflicting_duplicate_groups": int((test_groups.labels > 1).sum()),
             "exact_train_test_overlap_unique_texts": len(overlap_norms),
             "exact_train_test_overlap_label_counts": overlap_rows.label.value_counts().to_dict(),
             "clean_train_rows_after_dedup_and_test_decontamination": int(train.drop_duplicates("text_norm").loc[lambda d: ~d.text_norm.isin(set(test.text_norm))].shape[0]),
             "clean_train_label_counts": clean_train.label.value_counts().to_dict(),
             "clean_test_label_counts": clean_test.label.value_counts().to_dict(),
             "train_length_chars": train.text.str.len().describe().to_dict(),
             "test_length_chars": test.text.str.len().describe().to_dict()}
    write_json(ROOT / "outputs/metrics/eda_summary.json", stats)
    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=(6, 4)); sns.countplot(data=train, x="label", order=["Real", "Fake"], ax=ax)
    ax.set_title("Phân bố nhãn - train"); ax.set_xlabel("Nhãn"); ax.set_ylabel("Số mẫu")
    fig.tight_layout(); fig.savefig(ROOT / "outputs/figures/label_distribution.png", dpi=160); plt.close(fig)
    fig, ax = plt.subplots(figsize=(7, 4)); sns.histplot(data=train.assign(chars=train.text.str.len()), x="chars", hue="label", bins=40, element="step", stat="density", common_norm=False, ax=ax)
    ax.set_title("Độ dài văn bản theo nhãn"); ax.set_xlabel("Số ký tự"); fig.tight_layout()
    fig.savefig(ROOT / "outputs/figures/text_length.png", dpi=160); plt.close(fig)
    print(json.dumps(stats, ensure_ascii=False, indent=2))


def train() -> None:
    from sklearn.metrics import classification_report, confusion_matrix
    from sklearn.model_selection import train_test_split
    train_path, test_path = ROOT / CONFIG["dataset"]["train_file"], ROOT / CONFIG["dataset"]["test_file"]
    raw_train = load_split(train_path)
    raw_test = load_split(test_path)
    # Decontaminate the official split: keep one copy per text, then exclude from
    # training any text that occurs in test. Keep the test labels untouched.
    official_test = raw_test.drop_duplicates("text_norm", keep="first").reset_index(drop=True)
    test_hashes = set(official_test.text_norm)
    train_unique = raw_train.drop_duplicates("text_norm", keep="first")
    overlap = set(train_unique.text_norm) & test_hashes
    df = train_unique.loc[~train_unique.text_norm.isin(test_hashes)].reset_index(drop=True)
    if len(df.label.unique()) < 2 or len(official_test.label.unique()) < 2:
        raise ValueError("Sau khử trùng lặp, cần còn đủ hai nhãn trong train và test.")
    print(f"Raw train={len(raw_train)}, unique train={len(train_unique)}, train/test overlap removed={len(overlap)}, clean train={len(df)}")
    print(f"Raw test={len(raw_test)}, unique test={len(official_test)}")
    x_train, x_val, y_train, y_val = train_test_split(df.text, df.label, test_size=float(CONFIG["test_size_validation"]),
                                                       random_state=SEED, stratify=df.label)
    models_dir = ROOT / "models"; metrics_dir = ROOT / "outputs/metrics"; models_dir.mkdir(exist_ok=True)
    rows = []
    for name in CONFIG["default_models"]:
        pipe = make_pipeline(name)
        pipe.fit(x_train, y_train)
        pred = pipe.predict(x_val)
        scores = None
        if hasattr(pipe.named_steps["classifier"], "predict_proba"):
            classes = list(pipe.classes_); scores = pipe.predict_proba(x_val)[:, classes.index("Fake")]
        elif hasattr(pipe.named_steps["classifier"], "decision_function"):
            raw = pipe.decision_function(x_val)
            scores = raw if list(pipe.classes_)[1] == "Fake" else -raw
        row = {"model": name, **metrics_for(y_val, pred, scores)}
        rows.append(row)
        write_json(metrics_dir / f"validation_{name}.json", {**row, "classification_report": classification_report(y_val, pred, labels=["Real", "Fake"], output_dict=True, zero_division=0)})
        print(f"Validation {name}: macro-F1={row['f1_macro']:.4f}")
    results = pd.DataFrame(rows).sort_values("f1_macro", ascending=False)
    results.to_csv(metrics_dir / "validation_comparison.csv", index=False)
    chosen = str(results.iloc[0].model)
    # Final fit on all official train data; test is opened only after model selection.
    final_model = make_pipeline(chosen); final_model.fit(df.text, df.label)
    y_pred = final_model.predict(official_test.text)
    scores = None
    clf = final_model.named_steps["classifier"]
    if hasattr(clf, "predict_proba"):
        scores = final_model.predict_proba(official_test.text)[:, list(final_model.classes_).index("Fake")]
    elif hasattr(clf, "decision_function"):
        raw = final_model.decision_function(official_test.text)
        scores = raw if list(final_model.classes_)[1] == "Fake" else -raw
    test_metrics = metrics_for(official_test.label, y_pred, scores)
    test_metrics.update({"selected_model": chosen, "seed": SEED, "test_rows": len(official_test),
                         "train_rows_after_dedup_and_decontamination": len(df),
                         "raw_train_rows": len(raw_train), "train_duplicate_rows_removed": len(raw_train) - len(train_unique),
                         "train_test_overlap_texts_removed_from_train": len(overlap),
                         "raw_test_rows": len(raw_test), "test_duplicate_rows_removed": len(raw_test) - len(official_test),
                         "test_exact_overlap_with_train_after_cleaning": 0,
                         "warning": "Test metrics are only valid if the dataset split is independent and labels are reliable."})
    write_json(metrics_dir / "test_metrics.json", {**test_metrics, "classification_report": classification_report(official_test.label, y_pred, labels=["Real", "Fake"], output_dict=True, zero_division=0)})
    pd.DataFrame({"text": official_test.text, "true_label": official_test.label, "predicted_label": y_pred,
                  "correct": official_test.label.to_numpy() == y_pred}).to_csv(metrics_dir / "test_predictions.csv", index=False)
    cm = confusion_matrix(official_test.label, y_pred, labels=["Real", "Fake"])
    fig, ax = plt.subplots(figsize=(5, 4)); sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=["Real", "Fake"], yticklabels=["Real", "Fake"], ax=ax)
    ax.set(xlabel="Dự đoán", ylabel="Nhãn thật", title=f"Confusion matrix - {chosen}"); fig.tight_layout()
    fig.savefig(ROOT / "outputs/figures/confusion_matrix.png", dpi=160); plt.close(fig)
    joblib.dump(final_model, models_dir / "best_model.joblib")
    write_json(models_dir / "model_metadata.json", {"selected_model": chosen, "labels": list(final_model.classes_), "input": "text", "seed": SEED})
    print("\nTEST (chỉ chạy sau khi chọn model trên validation):")
    print(json.dumps(test_metrics, ensure_ascii=False, indent=2))
    print(f"Saved model: {models_dir / 'best_model.joblib'}")


def predict(text: str) -> dict:
    model_path = ROOT / "models/best_model.joblib"
    if not model_path.exists():
        raise FileNotFoundError("Chưa có model. Chạy: python -m src.project train")
    if not text.strip():
        raise ValueError("Văn bản đầu vào đang rỗng.")
    model = joblib.load(model_path)
    label = str(model.predict([text])[0])
    clf = model.named_steps["classifier"]
    result = {"prediction": label, "confidence": None, "score_type": None}
    if hasattr(clf, "predict_proba"):
        p = model.predict_proba([text])[0]
        result.update(confidence=float(p[list(model.classes_).index(label)]), score_type="xác suất mô hình (chưa hiệu chuẩn / uncalibrated)")
    elif hasattr(clf, "decision_function"):
        score = float(model.decision_function([text])[0])
        if list(model.classes_)[1] != "Fake": score = -score
        result.update(confidence=score, score_type="signed_margin (không phải xác suất)")
    return result


def main():
    parser = argparse.ArgumentParser(description="Vietnamese fake-news classification project")
    parser.add_argument("command", choices=["eda", "train", "predict"])
    parser.add_argument("--text", default="", help="Văn bản cần phân loại (command predict)")
    args = parser.parse_args()
    if args.command == "eda": eda()
    elif args.command == "train": train()
    else:
        try:
            print(json.dumps(predict(args.text), ensure_ascii=False, indent=2))
        except (FileNotFoundError, ValueError) as exc:
            print(f"Lỗi: {exc}", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__": main()
