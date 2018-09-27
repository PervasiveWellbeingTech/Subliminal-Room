import sys
from rgbxy import Converter

converter = Converter()
def reset_m(lights, rgb, brightness):
    for light in lights:
        light.xy = converter.rgb_to_xy(rgb[0], rgb[1], rgb[2])
        light.brightness = brightness
    print("resetted lights: color: {}, brightness: {}.".format(rgb, brightness))


def reset(lights, options):
    for light in lights:
        light.xy = converter.rgb_to_xy(options['r'], options['g'], options['b'])
        light.brightness = options['brightness']
    print("resetted lights: color: R:{}, G:{}, B:{}, Brightness: {}.".format(options['r'], options['g'], options['b'], options['brightness']))

def reset_group(group, options):
    group.xy = converter.rgb_to_xy(options['r'], options['g'], options['b'])
    group.brightness = options['brightness']
    print("resetted group {}: color: R:{}, G:{}, B:{}, Brightness: {}.".format(group.name, options['r'], options['g'], options['b'], options['brightness']))
