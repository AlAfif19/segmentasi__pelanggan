def classify_level(value):
    if value < 0.34:
        return "Low"
    if value < 0.67:
        return "Medium"
    return "High"


def build_combination(recency, frequency, monetary):
    return "-".join(
        [
            classify_level(recency),
            classify_level(frequency),
            classify_level(monetary),
        ]
    )
