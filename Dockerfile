# syntax=docker/dockerfile:1

# Define a default value for the argument PY_VER
ARG PY_VER=3.12

# Define a default value for the argument PY_SCRIPT_NAME
ARG PY_SCRIPT_NAME=must_pass_as_docker_build_arg.py

# slim version of Python 3.## to minimize the size of the container and make it as lightweight as possible
FROM python:${PY_VER}-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Optimize pip
ENV PIP_DEFAULT_TIMEOUT=100 \
    # Allow statements and log messages to immediately appear
    PYTHONUNBUFFERED=1 \
    # disable a pip version check to reduce run-time & log-spam
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    # cache is useless in docker image, so disable to reduce image size
    PIP_NO_CACHE_DIR=1

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
#ENV VAR="VALUE"

# set the default executable for a container 
ENTRYPOINT [ "python3" ]

# Define the command to run your Python script
#CMD ["${PY_SCRIPT_NAME}"]
CMD ["gcp_run_vol_mt.py"]
#CMD ["python", "gcp_run_vol_mt.py"]
#CMD ["python", "${PY_SCRIPT_NAME}"]

