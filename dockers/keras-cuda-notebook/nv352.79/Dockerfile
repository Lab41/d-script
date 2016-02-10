# Start with Ubuntu base image
FROM ubuntu:14.04
MAINTAINER Kai Arulkumaran <design@kaixhin.com>

ENV DEBIAN_FRONTEND noninteractive

# Install wget and build-essential
RUN apt-get update && apt-get install -y \
  build-essential \
  wget

# Use .deb method to install CUDA 7.5 + NVidia drivers (352.79)
RUN cd /tmp && \
    wget -q http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1404/x86_64/cuda-repo-ubuntu1404_7.5-18_amd64.deb && \
    dpkg -i cuda-repo-ubuntu1404_7.5-18_amd64.deb && \
    apt-get update && \
    apt-get install -y cuda

# Add to path
ENV PATH=/usr/local/cuda/bin:$PATH \
  LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH

# Install cuDNN v4
ENV ML_REPO_PKG=nvidia-machine-learning-repo_4.0-2_amd64.deb
RUN wget http://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1404/x86_64/$ML_REPO_PKG && \
  dpkg -i $ML_REPO_PKG && \
  apt-get update && apt-get install -y libcudnn4

# Install git, python-dev, pip and other dependencies
RUN apt-get update && apt-get install -y \
  git \
  libopenblas-dev \
  python-dev \
  python-pip \
  python-nose \
  python-numpy \
  python-scipy

# Set CUDA_ROOT
ENV CUDA_ROOT /usr/local/cuda/bin
# Install bleeding-edge Theano
RUN pip install --upgrade --no-deps git+git://github.com/Theano/Theano.git
# Set up .theanorc for CUDA
RUN echo "[global]\ndevice=gpu\nfloatX=float32\n[lib]\ncnmem=1\n[nvcc]\nfastmath=True" > /root/.theanorc

RUN apt-get update && apt-get install -y \
  libhdf5-dev \
  python-h5py \
  python-yaml

# Upgrade six
RUN pip install --upgrade six && \
    cd /root && git clone https://github.com/fchollet/keras.git && cd keras && \
    python setup.py install && \
    sudo apt-get -y install vim

RUN pip install jupyter && \
    sudo apt-get -y build-dep python-matplotlib
RUN pip install matplotlib seaborn bokeh pandas scikit-learn scikit-image
RUN cd /root && \
    wget https://pypi.python.org/packages/source/t/tornado/tornado-4.1.tar.gz && \
    gunzip tornado-4.1.tar.gz && tar -xvf tornado-4.1.tar && \
    cd tornado-4.1 && python setup.py install && \
    pip install notebook 

# Startup script
RUN printf '#!/bin/bash\n\njupyter notebook --no-browser --ip="*"' > /bootstrap.sh && \
    chmod +x /bootstrap.sh

EXPOSE 8888

CMD ["/bootstrap.sh"]
#CMD ["jupyter", "notebook", "--ip='*'", "--no-browser"]
