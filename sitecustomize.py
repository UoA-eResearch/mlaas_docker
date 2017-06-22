import sys
if not sys.getfilesystemencoding():
  sys.getfilesystemencoding = lambda: 'UTF-8'

import subprocess, re, os, sys

# GPU picking
# http://stackoverflow.com/a/41638727/419116
# Nvidia-smi GPU memory parsing.
# Tested on nvidia-smi 370.23

def run_command(cmd):
    """Run command, return output as string."""
    
    output = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True).communicate()[0]
    return output.decode("ascii")

def list_available_gpus():
    """Returns list of available GPU ids."""
    
    output = run_command("nvidia-smi -L")
    # lines of the form GPU 0: TITAN X
    gpu_regex = re.compile(r"GPU (?P<gpu_id>\d+):")
    result = []
    for line in output.strip().split("\n"):
        m = gpu_regex.match(line)
        assert m, "Couldnt parse "+line
        result.append(int(m.group("gpu_id")))
    return result

def gpu_memory_map():
    """Returns map of GPU id to memory allocated on that GPU."""

    output = run_command("nvidia-smi --query-gpu=memory.free --format=csv,noheader,nounits")
    rows = output.strip().split("\n")
    return rows

def pick_gpu_lowest_memory():
    """Returns GPU with the least allocated memory"""

    memory_gpu_map = [(memory, gpu_id) for (gpu_id, memory) in enumerate(gpu_memory_map())]
    best_memory, best_gpu = sorted(memory_gpu_map)[0]
    return best_gpu

def setup_one_gpu():
    assert not 'tensorflow' in sys.modules, "GPU setup must happen before importing TensorFlow"
    gpu_id = pick_gpu_lowest_memory()
    print("Picking GPU "+str(gpu_id))
    os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"
    os.environ["CUDA_VISIBLE_DEVICES"] = str(gpu_id)

def setup_no_gpu():
    if 'tensorflow' in sys.modules:
        print("Warning, GPU setup must happen before importing TensorFlow")
    os.environ["CUDA_VISIBLE_DEVICES"] = ''

setup_one_gpu()

import tensorflow as tf

oldinit = tf.Session.__init__
def myinit(session_object, target='', graph=None, config=None):
    print("Intercepted!")
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    oldinit(session_object, target='', graph=None, config=config)
tf.Session.__init__ = myinit
