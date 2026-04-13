def get_action(state):

    irrigation = 0.5

    if state["soil_moisture"] < 0.3:
        irrigation += 0.3

    if state["pH"] < 6 or state["pH"] > 8:
        irrigation -= 0.1

    if state["EC"] > 3:
        irrigation -= 0.2

    return max(0, min(irrigation, 1))