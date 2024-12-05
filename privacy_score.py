# src/scoring/privacy_score.py

def get_exposure(value):
    """
    Determine the exposure level of a given value.
    Args:
        value: The value to evaluate.
    Returns:
        int: Exposure level (0 = not exposed, 1 = private, 2 = public).
    """
    if not value:  # Not exposed
        return 0
    elif isinstance(value, int) and value == 0:  # Count fields with no data
        return 0
    else:  # Publicly exposed
        return 2


def calculate_risk(weights, data):
    """
    Calculate the total privacy risk for a given dataset.
    Args:
        weights (dict): Dictionary of category weights.
        data (dict): User data to evaluate.
    Returns:
        int: Total risk score.
    """
    total_risk = 0
    for field, weight in weights.items():
        exposure = get_exposure(data.get(field))
        total_risk += exposure * weight
    return total_risk


def calculate_privacy_score(user_info):
    """
    Calculate a privacy score based on user information.
    Args:
        user_info (dict): Dictionary containing user data.
    Returns:
        float: Privacy score (0-100).
    """
    # Define weights for each privacy category
    weights = {
        "id": 5,
        "name": 10,
        "username": 5,
        "location": 20,
        "description": 10,
        "followers_count": 10,
        "following_count": 10,
        "tweet_count": 5,
    }

    # Maximum possible risk (all fields public)
    max_risk = sum(weights.values()) * 2

    # Calculate the total risk
    total_risk = calculate_risk(weights, user_info)

    # Normalize the score to a scale of 0-100
    privacy_score = 100 - (total_risk / max_risk * 100)
    return round(privacy_score, 2)
