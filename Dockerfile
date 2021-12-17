#FROM python:3.8.7-alpine3.12
#FROM python:3.8.8-alpine3.13
#FROM python:3.8.8-alpine3.13-0.0.1
#FROM classification:base
FROM colorization:base

ARG APP_NAME="colorization"
#ARG APP_NAME="classification"

WORKDIR /opt/app
COPY ./app.conf ./dist/*.whl ./ai_app/${APP_NAME}.* /opt/app/

## 构建 python:3.8.7-alpine3.12-0.0.1
#RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apk/repositories && \ 
#    apk add --no-cache gcc g++ make libffi-dev openssl-dev python3-dev sshpass openssh tzdata && \
#    \cp -rf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
#    echo 'Asia/Shanghai' > /etc/timezone && \
#    apk del tzdata && \
#    pip install --upgrade pip -i https://mirrors.aliyun.com/pypi/simple && \
#    pip install paramiko -i https://mirrors.aliyun.com/pypi/simple && \
#    apk del gcc g++ make libffi-dev openssl-dev python3-dev

## 完整构建
#RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apk/repositories && \ 
#    apk add --no-cache gcc g++ make libffi-dev openssl-dev python3-dev sshpass openssh tzdata && \
#    \cp -rf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
#    echo 'Asia/Shanghai' > /etc/timezone && \
#    apk del tzdata && \
#    pip install paramiko -i https://mirrors.aliyun.com/pypi/simple && \ 
#    pip install *.whl && \
#    ln -sf /dev/stdout /var/log/app.log 

# 增量构建
RUN pip install *.whl --force-reinstall && \
    ln -sf /dev/stdout /var/log/app.log

CMD [ "app" ]
