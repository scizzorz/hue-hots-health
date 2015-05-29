import gtk.gdk
import phue
import time

def pixel_at(x, y):
  rw = gtk.gdk.get_default_root_window()
  pixbuf = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, 1, 1)
  pixbuf = pixbuf.get_from_drawable(rw, rw.get_colormap(), x, y, 0, 0, 1, 1)
  return tuple(pixbuf.pixel_array[0, 0])

# begin healthbar @ 220, 1000
# end healthbar @ 440, 1000

Y = 1000
BEGIN_X = 220
END_X = 440

def get_health(ox, oy):
  for x in range(BEGIN_X, END_X):
    r, g, b = pixel_at(ox+x, oy+Y)

    if r == 30 and g == 18 and b == 40:
      return 0.0 # dead

    if g < 40:
      return 1.0 * (x - BEGIN_X) / (END_X - BEGIN_X) # missing health

  return 1.0 # full health


def main():
  bridge = phue.Bridge('192.168.1.144')
  bridge.connect()

  last_hp = None

  while True:
    hp = round(get_health(1920, 0)*100) / 100.0

    if hp == last_hp:
      continue

    last_hp = hp

    if hp <= 0.0:
      print 'you\'re a shitter'
      hue = 0.75 * 65536
      bri = 127
    else:
      print 'you\'re at %.2f' % hp
      bri = 254
      hue = int(hp * 65536 / 3.0)

    try:
      bridge.set_light(8, {'hue': hue, 'bri': bri}, transitiontime=0)
    except phue.PhueRequestTimeout:
      print 'timed out'
      pass

    time.sleep(0.1)

if __name__ == '__main__':
  main()
