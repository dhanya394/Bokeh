from bokeh.plotting import figure, curdoc
from bokeh.models.widgets import FileInput
from bokeh.layouts import column,row
from bokeh.models.widgets import Button
from bokeh.models import Slider, ColumnDataSource, CustomJS
from bokeh.io import reset_output
import cv2
import os
import numpy as np
from bokeh.io import export_png
import io
from pybase64 import b64decode
from PIL import Image
from skimage.io import imsave, imread

x_range = (-20, -10)
y_range = (20, 30)

directory = '../../Bokeh/server_folder/static/'
directory1 = '../../Bokeh/'

p = figure(x_range=x_range, y_range=y_range, tools="crosshair,pan,reset,save,wheel_zoom")
source = ColumnDataSource()

img_path = 'server_folder/static/dummy.jpeg'
url = img_path
source = ColumnDataSource(data=dict(
    url=[url]
))
p.image_url(url='url', x=x_range[0], y=y_range[1], w=x_range[1] - x_range[0], h=y_range[1] - y_range[0],
                source=source)

btn1 = Button(label="RGB2Gray", button_type="success")
btn2 = Button(label="Median Filter", button_type="success")
btn3 = Button(label="Reset Image", button_type="success")
btn4 = Button(label="Download Image", button_type="success")

gsmooth = Slider(title="Gaussian Smooth", value=1, start=1, end=49, step=2)
threshold = Slider(title="Threshold Image", value=0, start=0, end=255, step=1)

val=''

##########################RGB to Grayscale Conversion###############################################

def callback(event):
    image = cv2.imread('../../Bokeh/server_folder/static/image1.jpeg')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    os.chdir(directory)
    cv2.imwrite('gray.jpeg', gray)
    cv2.imwrite('image1.jpeg', gray)
    os.chdir(directory1)
    img_path = 'server_folder/static/gray.jpeg'
    url = img_path
    source.data = dict(
        url=[url]
    )

btn1.on_click(callback)

######################################################################################################

##################################Gaussian Smoothening#################################################

def update_data(attrname, old, new):
   k=gsmooth.value
   print("Gaussian filter : ",k)
   img = cv2.imread('../../Bokeh/server_folder/static/image1.jpeg')
   gaussian = cv2.GaussianBlur(img, (k, k), 0)
   os.chdir(directory)
   cv2.imwrite('gaussian.jpeg', gaussian)
   cv2.imwrite('image1.jpeg', gaussian)
   os.chdir(directory1)
   img_path = 'server_folder/static/gaussian.jpeg'
   url = img_path
   source.data = dict(
       url=[url]
   )

gsmooth.on_change('value', update_data)

########################################################################################################

################################Median Filter###########################################################

def callback1(event):
    image = cv2.imread('../../Bokeh/server_folder/static/image1.jpeg')
    median = cv2.medianBlur(image,5)
    os.chdir(directory)
    cv2.imwrite('median.jpeg', median)
    cv2.imwrite('image1.jpeg', median)
    os.chdir(directory1)
    img_path = 'server_folder/static/median.jpeg'
    url = img_path
    source.data = dict(
        url=[url]
    )

btn2.on_click(callback1)

########################################################################################################

##################################Threshold Image#######################################################

def update_data1(attrname, old, new):
   k=threshold.value
   print("Threshold : ",k)
   img = cv2.imread('../../Bokeh/server_folder/static/image1.jpeg')
   ret,thresh = cv2.threshold(img,k,255,cv2.THRESH_BINARY)
   os.chdir(directory)
   cv2.imwrite('thresh.jpeg', thresh)
   cv2.imwrite('image1.jpeg', thresh)
   os.chdir(directory1)
   img_path = 'server_folder/static/thresh.jpeg'
   url = img_path
   source.data = dict(
       url=[url]
   )

threshold.on_change('value', update_data1)

#########################################################################################################

############################Reset Image###############################################################

def callback2(event):
    image = cv2.imread('../../Bokeh/server_folder/static/image.jpeg')
    os.chdir(directory)
    cv2.imwrite('image1.jpeg', image)
    os.chdir(directory1)
    img_path = 'server_folder/static/image.jpeg'
    url = img_path
    source.data = dict(
        url=[url]
    )

btn3.on_click(callback2)

###############################################################################################

#######################Image File Upload##############################

def upload_data(attr, old, new):
    print("File Uploaded successfully")
    print(type(file_input.filename))
    decoded = b64decode(file_input.value)
    f = io.BytesIO(decoded)
    image = Image.open(f)
    print(image.size)
    print(type(image))
    img_array = np.array(image, dtype=np.uint8)
    os.chdir(directory)
    imsave("image.jpeg", img_array)
    imsave("image1.jpeg", img_array)
    os.chdir(directory1)
    img_path = 'server_folder/static/image1.jpeg'
    url = img_path
    source.data = dict(
        url=[url]
    )

file_input = FileInput(accept=".jpeg")
file_input.on_change('value', upload_data)

########################################################################

btn4 = Button(label="Download Image", button_type="success")
btn4.js_on_click(CustomJS(args=dict(source=source), code="""
        var data = source.data;
        value1=data['url'];
        var file = new Blob([value1], {type: 'image/jpeg'});
        var elem = window.document.createElement('output');
        elem.href = window.URL.createObjectURL(file);
        elem.download = 'downloaded_image.jpeg';
        document.body.appendChild(elem);
        elem.click();
        document.body.removeChild(elem);
        """))

doc = curdoc()
doc.add_root(row(column(file_input,p) , column(btn1,gsmooth,btn2,threshold,btn3,btn4)))
curdoc.title = "Image Processing Demo"

#bokeh serve server_folder --show
