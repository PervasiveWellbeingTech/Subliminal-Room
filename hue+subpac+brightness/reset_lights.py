import sys
sys.path.insert(0, '/Users/kaandonbekci/dev/pervasivetech/Room')
from rgbxy import Converter

converter = Converter()
def reset(lights, rgb, brightness):
    for light in lights:
        light.xy = converter.rgb_to_xy(rgb[0], rgb[1], rgb[2])
        light.brightness = brightness
    print("resetted lights: color: {}, brightness: {}.".format(rgb, brightness))
