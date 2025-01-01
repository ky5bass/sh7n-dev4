ARG PYTHON_VERSION=3.11.5
# 注 PythonバージョンはCludflare実行環境に準拠した

FROM python:${PYTHON_VERSION} AS export
RUN pip --no-cache-dir install pipenv
COPY --chmod=644 ./requirements.txt ./
RUN pipenv --python ${PYTHON_VERSION} \
&& pipenv install -r requirements.txt \
&& pipenv lock \
# 参考 https://zenn.dev/nekoallergy/articles/py-env-pipenv01
&& pipenv requirements > /requirements.lock

FROM python:${PYTHON_VERSION} AS builder
COPY --from=export /requirements.lock /
RUN pip install --upgrade pip \
&& pip install --no-cache-dir -r /requirements.lock

FROM python:${PYTHON_VERSION}-slim
ENV TZ="Asia/Tokyo"
WORKDIR /myproject/
RUN apt update \
&& apt -y upgrade \
&& apt -y install libpq5 libxml2 \
&& apt clean \
&& rm -rf /var/lib/apt/lists/*
COPY --from=builder /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/
# 注 ↑`PYTHON_VERSION`のマイナーバージョン(3.9.16なら9の部分)を変更した場合は
#      必ずPythonパス(`…/python3.9/…`)のバージョン部分を合わせるように変更すること