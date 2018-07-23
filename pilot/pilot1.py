import libs
from multithread import Intervention
import controller as hue
import oscilliate_group as oscilliate
import reset

hue.init()
cmd = hue.make_command(255, 240, 230, 255, 5)
hue.set_group(hue.group, cmd)
