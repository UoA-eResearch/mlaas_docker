FROM tensorflow/tensorflow:latest-gpu
RUN pip install keras
RUN apt-get update && apt-get install python-tk python3-pip --yes
RUN pip3 install jupyterhub notebook numpy scipy
COPY sitecustomize.py /etc/python3.5/sitecustomize.py
COPY sitecustomize.py /etc/python2.7/sitecustomize.py
COPY *.sh /usr/local/bin/
CMD ["start-notebook.sh"]

ENV SHELL /bin/bash
ENV NB_USER jovyan
ENV NB_UID 1000
ENV HOME /home/$NB_USER
ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8

# Create jovyan user with UID=1000 and in the 'users' group
RUN useradd -m -s /bin/bash -N -u $NB_UID $NB_USER

USER $NB_USER

# Setup work directory for backward-compatibility
RUN mkdir /home/$NB_USER/work

# TensorBoard
EXPOSE 6006
# IPython
EXPOSE 8888

COPY notebooks/* $HOME/

