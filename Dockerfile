# ベースとするDockerイメージ
FROM python:3.8

# メタ情報をラベルで定義
LABEL version="1.0"
LABEL description="sample todo app"
LABEL maintainer="ihch"

# 環境変数
ENV USERNAME ihch

# ディレクトリの移動
WORKDIR /app

# ホストマシンのデータをコピー
COPY ./requirements.txt .

# Dockerコンテナを動かすときに必要なパッケージをインストール
RUN pip install -r requirements.txt

# ソースコードのコピー
# 命令の内容に変更があるとその命令以降のビルドキャッシュが
# 無効になるので変更が起こりやすいコピーなどは後がいい
COPY ./main.py .

# docker runした時に動く命令
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--reload"]
