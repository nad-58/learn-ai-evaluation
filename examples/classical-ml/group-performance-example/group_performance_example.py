"""Example: compare simple metrics across two groups."""

from learn_ai_evaluation.group_metrics import (
    positive_rate,
    true_positive_rate,
    false_positive_rate,
    rate_ratio,
)


def main():
    group_a_positive_rate = positive_rate(300, 1000)
    group_b_positive_rate = positive_rate(200, 800)

    print("Positive prediction rate")
    print("Group A:", round(group_a_positive_rate, 4))
    print("Group B:", round(group_b_positive_rate, 4))
    print("Ratio:", round(rate_ratio(group_a_positive_rate, group_b_positive_rate), 4))

    group_a_tpr = true_positive_rate(tp=80, fn=20)
    group_b_tpr = true_positive_rate(tp=60, fn=40)

    print("\nTrue positive rate")
    print("Group A:", round(group_a_tpr, 4))
    print("Group B:", round(group_b_tpr, 4))
    print("Ratio:", round(rate_ratio(group_a_tpr, group_b_tpr), 4))

    group_a_fpr = false_positive_rate(fp=20, tn=900)
    group_b_fpr = false_positive_rate(fp=10, tn=950)

    print("\nFalse positive rate")
    print("Group A:", round(group_a_fpr, 4))
    print("Group B:", round(group_b_fpr, 4))
    print("Ratio:", round(rate_ratio(group_a_fpr, group_b_fpr), 4))


if __name__ == "__main__":
    main()
