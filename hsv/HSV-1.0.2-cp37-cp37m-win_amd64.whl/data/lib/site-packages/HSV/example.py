from HSV.hsv import rgb_to_hsv, hsv_to_rgb

import timeit

if __name__ == '__main__':

    ONE_255 = 1.0 / 255.0
    r, g, b = 25, 60, 128
    print("\nOriginal RGB values (R:%s, G:%s, B:%s)\n" % (r, g, b))
    h, s, v = rgb_to_hsv(r * ONE_255, g * ONE_255, b * ONE_255)
    print("HSV values (H:%s, S:%s, V:%s)" % (h * 360.0, s * 100.0, v * 100.0))
    r, g, b = hsv_to_rgb(h, s, v)
    print("Retrieved RGB values (R:%s, G:%s, B:%s)\n" % (r * 255.0, g * 255.0, b * 255.0))

    N = int(1e6)

    r, g, b = 25, 60, 128
    t = timeit.timeit("rgb_to_hsv(r * ONE_255, g * ONE_255, b * ONE_255)",
                      "from __main__ import rgb_to_hsv, r, g, b, ONE_255", number=N)
    print("Performance testing rgb_to_hsv per call %s overall time %s for %s"
          % (round(float(t)/float(N), 10), round(float(t), 5), N))

    h, s, v = rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
    t = timeit.timeit("hsv_to_rgb(h, s, v)", "from __main__ import hsv_to_rgb, h, s, v", number=N)
    print("Performance testing hsv_to_rgb per call %s overall time %s for %s"
          % (round(float(t)/float(N), 10), round(float(t), 5), N))

    try:
        import colorsys
        from colorsys import rgb_to_hsv, hsv_to_rgb
        t = timeit.timeit("rgb_to_hsv(r * ONE_255, g * ONE_255, b * ONE_255)",
                          "from __main__ import rgb_to_hsv, r, g, b, ONE_255", number=N)
        print("\nPerformance testing colorsys.rgb_to_hsv per call %s overall time %s for %s" %
              (round(float(t) / float(N), 10), round(float(t), 5), N))

        h, s, l = rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
        t = timeit.timeit("hsv_to_rgb(h, s, l)", "from __main__ import hsv_to_rgb, h, s, l", number=N)
        print("Performance testing colorsys.hsv_to_rgb per call %s overall time %s for %s" %
              (round(float(t) / float(N), 10), round(float(t), 5), N))

    except ImportError:
        print('\nColorsys is not present on your system for additional performance testing.')

