import numpy

distinct_colors = [
    (230, 25, 75),
    (60, 180, 75),
    # (255, 225, 25),
    (0, 130, 200),
    (245, 130, 48),
    (145, 30, 180),
    (70, 240, 240),
    # (240, 50, 230),
    (210, 245, 60),
    (250, 190, 190),
    # (0, 128, 128),
    # (230, 190, 255),
    # (170, 110, 40),
    # (255, 250, 200),
    (128, 0, 0),
    (170, 255, 195),
    (128, 128, 0),
    (255, 215, 180)
]


def get_label_lut(lut_size=255):
    s4 = (lut_size + 1) * 4
    lut = numpy.random.randint(low=0, high=255, size=s4)
    lut = lut.reshape([lut_size + 1, 4])
    lut[:, 3] = 255
    lut[0, 3] = 0
    lut[1:1 + len(distinct_colors), 0:3] = numpy.array(distinct_colors)
    return lut
