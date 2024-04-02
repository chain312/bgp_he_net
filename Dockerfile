FROM python:3.8-alpine

MAINTAINER chain312 <wqi648761@gmail.com>

WORKDIR /app

COPY ./requirements.txt .

# apk repository
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories
RUN apk update


# timezone
RUN apk add -U tzdata && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && apk del tzdata
RUN pip install --upgrade pip -i https://mirrors.aliyun.com/pypi/simple/
# runtime environment
RUN apk add musl-dev gcc libffi-dev libxml2-dev  libxslt-dev && \
    pip install --no-cache-dir -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ && \
    apk del gcc musl-dev

COPY . .

EXPOSE 45501

ENTRYPOINT [ "sh", "start.sh" ]
