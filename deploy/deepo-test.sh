docker run --runtime=nvidia -it -p 8881:8888 --ipc=host ufoym/deepo:all-jupyter-py36-cu100 bash 
#jupyter notebook --no-browser --ip=0.0.0.0 --allow-root --NotebookApp.token='password' --notebook-dir='/root'
