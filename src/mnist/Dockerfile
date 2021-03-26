FROM ufoym/deepo:keras-py36

# copy local files into container
COPY mnistapp.py /tmp/
COPY mnist.h5 /tmp/
COPY requirements.txt /tmp/

ENV PORT 80

# change directory
WORKDIR /tmp

# install dependencies
RUN apt-get update 
RUN apt-get install -y libgl1-mesa-glx 
RUN pip install -r requirements.txt

# run commands
CMD ["streamlit", "run", "mnistapp.py"]
