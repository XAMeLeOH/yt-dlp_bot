FROM debian AS curl-impersonate

RUN apt-get update \
	&& apt-get install -y \
                autoconf \
                automake \
                build-essential \
                cmake \
                curl \
		git \
                golang-go \
                libtool \
                libzstd-dev \
                ninja-build \
                pkg-config \
                unzip \
                zstd \
	&& rm -fr /var/cache/apt /var/lib/apt \
	&& git clone https://github.com/lexiforest/curl-impersonate.git \
	&& cd curl-impersonate \
	&& mkdir build \
	&& cd build \
	&& ../configure --prefix=/usr/local/ci \
	&& make build \
	&& make install

FROM python:3

COPY --from=curl-impersonate /usr/local/ci/bin /usr/bin
COPY --from=curl-impersonate /usr/local/ci/lib /usr/lib
COPY --from=denoland/deno:bin /deno /usr/bin/deno

RUN apt-get update \
	&& apt-get install -y ffmpeg \
	&& rm -fr /var/cache/apt /var/lib/apt \
	&& curl -fsSL https://github.com/lexiforest/curl-impersonate/releases/download/v1.5.1/curl-impersonate-v1.5.1.$(uname -m)-linux-gnu.tar.gz | tar -zxC /usr/bin

RUN --mount=type=bind,source=requirements.txt,target=/tmp/requirements.txt \
	pip install --requirement /tmp/requirements.txt

COPY tgbot.py /app/

