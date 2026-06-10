def _check_inputs(data, colors):
    if len(data) != len(colors):
        raise ValueError("data and colors must have the same length")
    if not data:
        raise ValueError("data and colors must not be empty")


def learn_theta(data, colors):
    _check_inputs(data, colors)
    blue_points = [x for x, color in zip(data, colors) if color == "blue"]
    red_points = [x for x, color in zip(data, colors) if color == "red"]

    if not blue_points or not red_points:
        raise ValueError("there must be at least one point of each color")

    theta = max(blue_points)
    if theta >= min(red_points):
        raise ValueError("not all blue points are less than all red points")
    return theta


def compute_ell(data, colors, theta):
    _check_inputs(data, colors)
    loss = 0

    for point, color in zip(data, colors):
        if color == "red" and point <= theta:
            loss += 1
        elif color == "blue" and point > theta:
            loss += 1

    return float(loss)


def minimize_ell(data, colors):
    _check_inputs(data, colors)

    best_theta = data[0]
    best_loss = compute_ell(data, colors, best_theta)

    for theta in data[1:]:
        loss = compute_ell(data, colors, theta)
        if loss < best_loss:
            best_theta = theta
            best_loss = loss

    return float(best_theta)


def minimize_ell_sorted(data, colors):
    _check_inputs(data, colors)

    blue_gt_theta = colors.count("blue")
    red_leq_theta = 0
    best_loss = float("inf")
    best_theta = data[0]

    for alpha in range(1, len(data) + 1):
        color = colors[alpha - 1]
        if color == "blue":
            blue_gt_theta -= 1
        elif color == "red":
            red_leq_theta += 1

        loss = blue_gt_theta + red_leq_theta
        if loss < best_loss:
            best_loss = loss
            best_theta = data[alpha - 1]

    return float(best_theta)
