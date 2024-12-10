def get_exposure(value):
    if not value:  # Not exposed
        return 0
    elif isinstance(value, int) and value == 0:  # Count fields with no data
        return 0
    else:  # Publicly exposed
        return 2

def calculate_risk(weights, data):
    total_risk = 0
    for field, weight in weights.items():
        exposure = get_exposure(data.get(field))
        total_risk += exposure * weight
    return total_risk

def calculate_overall_privacy_score(all_user_info):
    weights = {
        "YouTube": {
            "id": 5,
            "snippet": 10,
            "location": 25,
            "contentDetails": 15,
            "statistics": 10,
            "privacyStatus": 10,
            "isLinked": 5,
        },
        "Reddit": {
            "username": 10,
            "user_id": 5,
            "account_created": 5,
            "is_employee": 5,
            "is_moderator": 10,
        },
        "Instagram": {
            "id": 5,
            "username": 10,
            "bio": 10,
            "connections": 15,
            "profile_picture": 5,
        },
        "Twitter": {
            "id": 5,
            "name": 10,
            "location": 25,
            "bio": 10,
            "connections": 15,
        },
        "LinkedIn": {
            "id": 5,
            "name": 10,
            "email": 15,
            "number": 20,
            "headline": 20,  # job
            "location": 25,
            "education": 15,
            "connections": 15,
        },
    }

    total_risk = 0
    max_risk = 0
    platforms_found = 0

    for platform, user_info in all_user_info.items():
        platform_weights = weights.get(platform, {})
        if user_info:  # If user is found on this platform
            platforms_found += 1
            total_risk += calculate_risk(platform_weights, user_info)
        max_risk += sum(platform_weights.values()) * 2

    if platforms_found == 0:
        return 100.0  # Full privacy score if user is not found anywhere

    # Adjust score based on platforms found
    normalized_risk = total_risk / max_risk
    privacy_score = 100 - (normalized_risk * 100)
    return round(privacy_score, 2)
