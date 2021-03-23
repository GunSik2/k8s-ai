# GPU 테스트

## Jupyter notebook GPU 확인
```
import os

def is_available():

    """
        Check NVIDIA with nvidia-smi command
        Returning code 0 if no error, it means NVIDIA is installed
        Other codes mean not installed
    """
    code = os.system('nvidia-smi')
    return code == 0

print(is_available())
```
