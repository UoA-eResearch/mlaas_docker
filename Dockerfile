FROM tensorflow/tensorflow:latest-gpu
RUN pip install keras
RUN apt-get update && apt-get install python-tk python3-pip --yes
RUN pip3 install jupyterhub notebook
COPY notebooks/* /notebooks
COPY sitecustomize.py /etc/python3.5/sitecustomize.py
COPY sitecustomize.py /etc/python2.7/sitecustomize.py
COPY *.sh /usr/local/bin/
CMD ["start-notebook.sh"]
