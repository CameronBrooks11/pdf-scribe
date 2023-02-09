from matplotlib.widgets import RectangleSelector
import numpy as np
import matplotlib.pyplot as plt
from pdf2image import convert_from_path
from pathlib import Path
from io import StringIO
from PIL import Image
import cv2
#import processor

# paths to the required directories
pdf_inputpath = 'tests/test-files/Lesson_2_Memory_Mapping.pdf'
temppath = 'playground/box-selection/temp/'
outputpath = 'tests/test-output/bb/' 

class IndexTracker(object):
    def __init__(self, ax, doclen):
        self.doclen = doclen
        self.ax = ax
        self.fig = fig
        self.i = 0
        ax.set_title('use scroll wheel to navigate images')
        self.update()

    def onscroll(self, event):
        print("%s %s" % (event.button, event.step))
        if event.button == 'up':
            self.i-=1
            if(self.i<0):self.i=0
        else:
            self.i+=1
            if(self.i>doclen):self.i=doclen
        self.update(self.i)

    def update(self, i):
        targetimage = temppath + f'/tempimage-{i}.png'
        print(targetimage)
        self.im = ax.cla()
        image = plt.imread(targetimage)
        self.im = ax.imshow(image)
        self.im.axes.figure.canvas.draw()

def line_select_callback(eclick, erelease):
    'eclick and erelease are the press and release events'
    x1, y1 = eclick.xdata, eclick.ydata
    x2, y2 = erelease.xdata, erelease.ydata
    print("(%3.2f, %3.2f) --> (%3.2f, %3.2f)" % (x1, y1, x2, y2))
    #print(" The button you used were: %s %s" % (eclick.button, erelease.button))


def toggle_selector(event):
    print(' Key pressed.')
    if event.key in ['Z', 'z'] and toggle_selector.RS.active:
        print(' RectangleSelector deactivated.')
        toggle_selector.RS.set_active(False)
    if event.key in ['A', 'a'] and not toggle_selector.RS.active:
        print(' RectangleSelector activated.')
        toggle_selector.RS.set_active(True)
    if event.key in ['S', 's']:
        print(' Image saved activated.')
        targetimage = temppath + f'cut-temp/tempimage-{i}.png'
        image = cv2.imread(targetimage)
        crop_image = image[toggle_selector.RS.geometry()]
        cv2.imshow("Cropped", crop_image)
        cv2.waitKey(0)

    if event.key in ['X', 'x']:
        #text = processor('text')
        print(' Text extracted ')

fig, ax = plt.subplots()                 # make a new plotting range

pages = convert_from_path(pdf_inputpath)
doclen = len(pages)
for num, page in enumerate(pages):
        tempfile = temppath + f'/tempimage-{num}.png'
        page.save(tempfile, 'PNG')

tracker = IndexTracker(ax, doclen)

# scroll event 
fig.canvas.mpl_connect('scroll_event', tracker.onscroll)

# drawtype is 'box' or 'line' or 'none'
toggle_selector.RS = RectangleSelector(ax, line_select_callback,
                                       drawtype='box', useblit=True,
                                       button=[1, 3],  # don't use middle button
                                       minspanx=5, minspany=5,
                                       spancoords='pixels',
                                       interactive=True)
plt.connect('key_press_event', toggle_selector)
plt.show()