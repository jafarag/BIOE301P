import os

scr = os.environ['SCRATCH']
DATA_RAW = os.environ['DATA_RAW']
DATASET_ID = os.environ['SLURM_ARRAY_TASK_ID']
DATA_DERIV = os.environ['DATA_DERIV']
SES_ID = os.environ['PART_ID']
HOME = os.environ['HOME']
import numpy as np
freq = np.fft.rfftfreq(np.arange(0,20,0.0005).shape[0])
import numpy as np 
import plotly.express as px 

fft = np.load(HOME+'/hw3/ses'+DATASET_ID+'.npy')
fig = px.line(x=freq, y = fft[:,0], labels={'x':'Frequency (Hz)', 'y':'Amplitude'})
fig.write_html(DATA_DERIV+'/previs.html')


with open(data_deriv+"/previs.html") as f:
    str_viz = f.read()

# load jinja and render
from jinja2 import Environment, FileSystemLoader
print()
env = Environment(loader=FileSystemLoader(HOME+"/hw3/templates"), autoescape=False)
template = env.get_template("hw3_template.html")
final_html = template.render(plotly_visualization = str_viz)

# save renderd HTML
with open(HOME+"/hw3/final.html", 'w') as f:
    f.write(final_html)

