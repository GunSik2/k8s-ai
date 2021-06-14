# ML Docker 이미지 관리

## Deepo 
Deepo 를 이용한 이미지 관리

## Docker 파일 생성하기
- Deepo 준비 및 설정
```
$ git clone https://github.com/GunSik2/deepo
$ cd deepo
$ cd scripts

$ vi make-gen-docker.py
        generate(f, '10.2', '7')
        generate(f, '11.0', '8')  # CUDA 11.0, cudnn 8 추가
$ ./build.sh && cd ..
```
- 이미지 빌드
```
$ docker build -f  docker/Dockerfile.keras-py36-cu110 -t crossentpx/keras-py36-cu110 .
$ docker build -f  docker/Dockerfile.keras-py36-cpu -t crossentpx/keras-py36-cu110 .
```

## 패치
- keras 생성 오류 조치
```
$ vi generator/modules/keras.p
            $PIP_INSTALL \
                'h5py<3.0.0'\
```
## 참고자료
- https://hub.docker.com/r/nvidia/cuda/tags
