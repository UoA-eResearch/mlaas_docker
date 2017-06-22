FROM tensorflow/tensorflow:latest-gpu
RUN pip install keras
RUN apt-get update && apt-get install python-tk --yes
COPY sitecustomize.py /etc/python2.7/sitecustomize.py
COPY *.sh /usr/local/bin/
CMD ["start-notebook.sh"]
