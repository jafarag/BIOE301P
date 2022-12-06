import os



#HOME = os.environ['HOME']
import numpy as np
freq = np.fft.rfftfreq(np.arange(0,20,0.0005).shape[0])
import numpy as np
#import plotly.express as px
freq = np.linspace(0,500,16687085)
import numpy as np
#HOME = os.environ['HOME']
from bokeh.plotting import figure
from bokeh.io import curdoc
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Dropdown

# try with fake spectrograms now.
f = np.arange(100)
t = np.arange(1000)
S = np.random.random(size=[3,1000,100])
#os.chdir(HOME+'/hw3/')


freq = np.linspace(0,500,10)
import numpy as np
#HOME = os.environ['HOME']
from bokeh.plotting import figure
from bokeh.io import curdoc, show
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Dropdown

fft = np.random.randn(24,10)

#HOME = os.environ['HOME']
os.chdir(HOME+'/hw4')
fft = np.load('data/ses1_log.npy')
freq = np.linspace(0,50,27811)
data = {str(n): fft[n,:] for n in range(24)}
data['line'] = fft[0,:]
data['freq'] = freq
hi = []; 
for i in range(24):
    hi.append(str(i))

source = ColumnDataSource(data=data)

menu = []

for i in range(len(hi)):
    menu.append((str(hi[i]), str(i)))


dropdown = Dropdown(label="Select electrode",  menu=menu)

plot = figure(aspect_ratio=2,title='1')
plot.line('freq', 'line', source=source)
plot.xaxis.axis_label = 'Frequency (Hz)'
plot.yaxis.axis_label = u'Amplitude Spectrum (log\u2081\u2080 values)'

def update_data(event):
    data['line']=data[event.item]
    source.data = data
    plot.title.text = str(event.item)

# change data source!
dropdown.on_click(update_data)

# first try without CustomJS
layout = column(dropdown,plot)
curdoc().add_root(layout)

#fft = np.load(HOME+'/hw3/ses1.npy')

