__author__ = 'mayank'


def get_score(matched_attribute_list, query_doc):
    num_attributes_matched = len(matched_attribute_list)
    num_total_attributes = len(query_doc.keys())
    match_ratio = float(num_attributes_matched) / float(num_total_attributes)
    score = ranking_function(match_ratio, matched_attribute_list)
    normalized_score = normalize_score(score)
    return normalized_score


def ranking_function(match_ratio, matched_attribute_list):
    """
    sigma (i to no. of matched attributes) (matchRatio * ith weight)
    """
    score = 0
    for attribute in matched_attribute_list:
        score += match_ratio * attribute.get('weight')
    return score


def normalize_score(value):
    MIN_SCORE = 1
    MAX_SCORE = 10
    normalized_score = abs(value - MIN_SCORE / MAX_SCORE - MIN_SCORE)
    return normalized_score

