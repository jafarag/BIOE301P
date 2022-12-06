scr = os.environ['SCRATCH']
scr = os.environ['SCRATCH']
DATA_RAW = os.environ['DATA_RAW']
DATASET_ID = os.environ['SLURM_ARRAY_TASK_ID']
DATA_DERIV = os.environ['DATA_DERIV']
SES_ID = os.environ['PART_ID']
HOME = os.environ['HOME']

import os
import rclone

with open(os.path.join(os.path.expanduser('~'), '.config', 'rclone', 'rclone.conf')) as f:
    cfg = f.read()

rclone.with_config(cfg).copy(HOME+"/final.html", "firstremote:")
rclone.with_config(cfg).copy(HOME+"/final.html", "soe-bioe-301p:22s-bioe-301p-yfaragal")
