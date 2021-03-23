
## MNIST App 

- mnist-demo.yml
```
apiVersion: batch/v1
kind: Job
metadata:
  labels:
    app: mnist-demo
  name: mnist-demo
spec:
  template:
    metadata:
      labels:
        app: mnist-demo
    spec:
      containers:
      - name: mnist-demo
        image: lachlanevenson/tf-mnist:gpu
        args: ["--max_steps", "500"]
        imagePullPolicy: IfNotPresent
        resources:
          limits:
           nvidia.com/gpu: 1
      restartPolicy: OnFailure
```

- 배포 및 시험
```
$ kubectl create -f mnist-demo.yaml 

$  kubectl get jobs
NAME         COMPLETIONS   DURATION   AGE
mnist-demo   0/1           4s         4s

$ kubectl get pods
NAME               READY   STATUS              RESTARTS   AGE
mnist-demo-lt7p2   0/1     ContainerCreating   0          10s

$ kubectl logs mnist-demo-lt7p2
2020-08-31 02:09:59.535996: I tensorflow/core/platform/cpu_feature_guard.cc:137] Your CPU supports instructions that this TensorFlow binary was not compiled to use: SSE4.1 SSE4.2 AVX AVX2 AVX512F FMA
2020-08-31 02:09:59.679508: I tensorflow/stream_executor/cuda/cuda_gpu_executor.cc:892] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero
2020-08-31 02:09:59.680945: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1030] Found device 0 with properties: 
name: Quadro RTX 6000 major: 7 minor: 5 memoryClockRate(GHz): 1.62
pciBusID: 0000:00:06.0
totalMemory: 22.17GiB freeMemory: 22.00GiB
2020-08-31 02:09:59.680975: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1120] Creating TensorFlow device (/device:GPU:0) -> (device: 0, name: Quadro RTX 6000, pci bus id: 0000:00:06.0, compute capability: 7.5)
2020-08-31 02:13:34.822072: I tensorflow/stream_executor/dso_loader.cc:139] successfully opened CUDA library libcupti.so.8.0 locally
Successfully downloaded train-images-idx3-ubyte.gz 9912422 bytes.
Extracting /tmp/tensorflow/input_data/train-images-idx3-ubyte.gz
Successfully downloaded train-labels-idx1-ubyte.gz 28881 bytes.
Extracting /tmp/tensorflow/input_data/train-labels-idx1-ubyte.gz
Successfully downloaded t10k-images-idx3-ubyte.gz 1648877 bytes.
Extracting /tmp/tensorflow/input_data/t10k-images-idx3-ubyte.gz
Successfully downloaded t10k-labels-idx1-ubyte.gz 4542 bytes.
Extracting /tmp/tensorflow/input_data/t10k-labels-idx1-ubyte.gz
Accuracy at step 0: 0.106
….
Adding run metadata for 99
```
