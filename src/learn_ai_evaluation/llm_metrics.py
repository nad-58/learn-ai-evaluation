"""Dependency-free educational metrics for LLM evaluation."""
from collections import Counter
from math import exp, log


def perplexity(token_probabilities):
    """PPL = exp(-mean(log p(token))). Lower is better."""
    if not token_probabilities or any(p <= 0 or p > 1 for p in token_probabilities):
        raise ValueError("Probabilities must be a non-empty sequence in (0, 1]")
    return exp(-sum(log(p) for p in token_probabilities) / len(token_probabilities))


def exact_match(prediction, reference, normalise=True):
    """Return 1.0 for an exact match and 0.0 otherwise."""
    if normalise:
        prediction = " ".join(prediction.lower().strip().split())
        reference = " ".join(reference.lower().strip().split())
    return float(prediction == reference)


def token_f1(prediction, reference):
    """Bag-of-token precision, recall and F1."""
    pred = prediction.lower().split()
    ref = reference.lower().split()
    if not pred and not ref:
        return {"precision": 1.0, "recall": 1.0, "f1": 1.0}
    overlap = sum((Counter(pred) & Counter(ref)).values())
    precision = overlap / len(pred) if pred else 0.0
    recall = overlap / len(ref) if ref else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {"precision": precision, "recall": recall, "f1": f1}


def ngrams(tokens, n):
    return [tuple(tokens[i:i+n]) for i in range(len(tokens) - n + 1)]


def rouge_n_recall(prediction, reference, n=1):
    """Simplified ROUGE-N recall using clipped n-gram overlap."""
    pred = Counter(ngrams(prediction.lower().split(), n))
    ref = Counter(ngrams(reference.lower().split(), n))
    total = sum(ref.values())
    return sum((pred & ref).values()) / total if total else 0.0


def lcs_length(a, b):
    previous = [0] * (len(b) + 1)
    for x in a:
        current = [0]
        for j, y in enumerate(b, 1):
            current.append(previous[j-1] + 1 if x == y else max(previous[j], current[-1]))
        previous = current
    return previous[-1]


def rouge_l_f1(prediction, reference):
    """Simplified ROUGE-L F1 based on longest common subsequence."""
    pred = prediction.lower().split()
    ref = reference.lower().split()
    common = lcs_length(pred, ref)
    precision = common / len(pred) if pred else 0.0
    recall = common / len(ref) if ref else 0.0
    return 2 * precision * recall / (precision + recall) if precision + recall else 0.0


def bleu_1(prediction, reference):
    """Simplified unigram BLEU with brevity penalty."""
    pred = prediction.lower().split()
    ref = reference.lower().split()
    if not pred:
        return 0.0
    precision = sum((Counter(pred) & Counter(ref)).values()) / len(pred)
    penalty = 1.0 if len(pred) > len(ref) else exp(1 - len(ref) / len(pred))
    return penalty * precision
