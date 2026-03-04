FROM alpine AS builder

RUN apk add --no-cache \
		cmake \
		git \
		gperf \
		g++ \
		linux-headers \
		make \
		openssl-dev \
		zlib-dev \
	&& git clone --recursive https://github.com/tdlib/telegram-bot-api.git \
	&& cd telegram-bot-api \
	&& mkdir build \
	&& cd build \
	&& cmake -DCMAKE_BUILD_TYPE=Release .. \
	&& cmake --build . --target install

FROM alpine

RUN apk add --no-cache libstdc++

COPY --from=builder /telegram-bot-api/build/telegram-bot-api /usr/local/bin

