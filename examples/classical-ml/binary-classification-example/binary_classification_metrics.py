"""Example: binary classification metrics on synthetic data."""

from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

from learn_ai_evaluation.metrics import binary_classification_metrics, metrics_as_dict


def main():
    X, y = make_classification(
        n_samples=1000,
        n_features=10,
        n_informative=5,
        n_redundant=2,
        weights=[0.7, 0.3],
        random_state=42,
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.25,
        stratify=y,
        random_state=42,
    )

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    results = metrics_as_dict(binary_classification_metrics(y_test, y_pred))

    for metric, value in results.items():
        print(f"{metric}: {value:.3f}")


if __name__ == "__main__":
    main()
