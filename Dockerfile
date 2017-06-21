FROM tensorflow/tensorflow:latest-gpu
RUN pip install keras
COPY sitecustomize.py /etc/python2.7/sitecustomize.py
CMD ["/run_jupyter.sh", "--allow-root"]
