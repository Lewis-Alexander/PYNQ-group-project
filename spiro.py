#!/usr/bin/env python
# coding: utf-8
import math
import numpy as np
import matplotlib.pyplot as plt

def hypotrochoid(R, r, d, num_points): #traced by a point attached to a circle of radius r rolling around the inside of a fixed circle of radius R, where the point is a distance d from the center of the interior circle
    """
    Compute the x, y coordinates of a hypotrochoid:
      - R: radius of fixed outer circle
      - r: radius of rolling inner circle
      - d: offset ratio (distance from inner circle center to drawing point, relative to r)
    Returns two 1D numpy arrays of length num_points.
    """
    lowestCommonMultiple = np.lcm(int(r), int(R))/r
    theta = np.linspace(0, 2 * math.pi*lowestCommonMultiple, num_points)
    x = (R - r) * np.cos(theta) + d * np.cos(((R - r) / r)*theta)
    y = (R - r) * np.sin(theta) - d * np.sin(((R - r) / r)*theta)
    return x, y

def epitrochoid(R, r, d, num_points): #traced by a point attached to a circle of radius r rolling around the outside of a fixed circle of radius R, where the point is at a distance d from the center of the exterior circle
    """
    Compute the x, y coordinates of an epitrochoid:
      - R: radius of fixed circle
      - r: radius of rolling circle outside
      - d: offset ratio (distance from rolling circle center to drawing point, relative to r)
    Returns two 1D numpy arrays of length num_points.
    """
    theta = np.linspace(0, 2 * math.pi, num_points) # list of all a values
    x = (R + r) * np.cos(theta) - d * np.cos(((R + r) / r) * theta)
    y = (R + r) * np.sin(theta) - d * np.sin(((R + r) / r) * theta)
    return x, y


# # Show several parameter combinations
# patterns = [
#     ("Hypotrochoid", 5, 3, 5, 2000),
#     ("Hypotrochoid", 8, 6, 0.5, 2000),
#     ("Epitrochoid", 10, -0.1, 10, 2000),
#     ("Epitrochoid", 3, 1, 0.5, 2000),
# ]

# fig, axs = plt.subplots(2, 2, figsize=(10, 10))

# for ax, (ptype, R, r, d, numPoints) in zip(axs.flat, patterns):
#     if ptype == "Hypotrochoid":
#         x, y = hypotrochoid(R, r, d, numPoints)
#     else:
#         x, y = epitrochoid(R, r, d, numPoints)

#     ax.plot(x, y)
#     ax.set_title(f"{ptype}\nR={R}, r={r}, d={d}, number of points generate={numPoints}")
#     ax.set_aspect("equal")
#     ax.axis("off")

# plt.tight_layout()
# plt.show()
# exit(1)