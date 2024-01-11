import cv2
import numpy as np


def draw_clock(hour, minute, add_noise=True):
    """
    This function generates clock images based on hour and minute as an input.
    """
    height = 227
    width = 227
    center = 227 // 2
    img = np.zeros((height, width, 3))
    background_color = (np.random.randint(0, 256), np.random.randint(0, 256), np.random.randint(0, 256))
    img[:, :, :] = background_color
    random_color = (np.random.randint(0, 256), np.random.randint(0, 256), np.random.randint(0, 256))
    img = cv2.circle(img, (center, center), 112, color=random_color, thickness=-1)
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.7
    font_thickness = 2
    deg = -60
    pos_dict = {}
    deg_hour_dict = {}
    deg_minute_dict = {}
    for i in range(1, 13):
        pos = (int(center - 8 + 100 * np.cos(np.deg2rad(deg))), int(center + 100 * np.sin(np.deg2rad(deg))))
        img = cv2.putText(img, f"{i}", (
            int(center - 8 + 100 * np.cos(np.deg2rad(deg))), int(center + 100 * np.sin(np.deg2rad(deg)))), font, font_scale,
                          (0, 0, 0), font_thickness, cv2.LINE_AA)
        pos_dict[str(i)] = pos
        deg_hour_dict[str(i)] = deg
        deg += 30

    deg = -90
    for i in range(0, 60):
        deg_minute_dict[str(i)] = deg
        deg += 6

    hour_angle = 2 * np.pi * ((hour % 12) + minute / 60) / 12 - np.pi / 2
    minute_angle = 2 * np.pi * (minute % 60) / 60 - np.pi / 2
    img = cv2.line(img, (center, center),
                   (int(center + 45 * np.cos(hour_angle)), int(center + 45 * np.sin(hour_angle))), thickness=5,
                   color=(0, 0, 0))
    img = cv2.line(img, (center, center),
                   (int(center + 90 * np.cos(minute_angle)), int(center + 90 * np.sin(minute_angle))), thickness=3,
                   color=(0, 0, 0))
    noise = np.zeros(img.shape, np.uint8)
    cv2.randn(noise, mean=0, stddev=50)
    if add_noise:
        img = cv2.add(img.astype(np.uint8), noise)
    else:
        img = cv2.add(img.astype(np.uint8), noise) if np.random.randn() > 0.5 else img
    return img
