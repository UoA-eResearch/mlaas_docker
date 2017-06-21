# mlaas_docker
Custom docker image based on tensorflow, with keras and a sitecustomize.py to auto-choose the least utilised GPU, and then default tensorflow session to allow_growth=True, which won't use all the GPU RAM :)
