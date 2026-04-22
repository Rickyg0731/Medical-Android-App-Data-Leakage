def calculate_risk(leaks, third_party_count):
    score = 0

    for leak in leaks:
        score += 3  # source: directly accesses sensitive data, so it weighs more
        score += 2  # sink: transmits or exposes data, slightly lower weight

        # external endpoint found = data likely leaving the device
        if leak["endpoint"]:
            score += 3

    # each third-party library is a potential supply-chain risk
    score += 2 * third_party_count

    if score > 20:
        return "HIGH", score
    elif score > 10:
        return "MEDIUM", score
    else:
        return "LOW", score
