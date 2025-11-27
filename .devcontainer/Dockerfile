FROM mcr.microsoft.com/devcontainers/base:ubuntu-22.04

ARG HUGO_VERSION=0.128.0
ARG DART_SASS_VERSION=1.78.0

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        git \
        lftp \
        wget \
    && wget -O /tmp/hugo.deb "https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_extended_${HUGO_VERSION}_linux-amd64.deb" \
    && dpkg -i /tmp/hugo.deb \
    && rm /tmp/hugo.deb \
    && wget -O /tmp/dart-sass.tar.gz "https://github.com/sass/dart-sass/releases/download/${DART_SASS_VERSION}/dart-sass-${DART_SASS_VERSION}-linux-x64.tar.gz" \
    && tar -xzf /tmp/dart-sass.tar.gz -C /opt \
    && ln -sf /opt/dart-sass/dart-sass /usr/local/bin/dart-sass \
    && ln -sf /opt/dart-sass/sass /usr/local/bin/sass \
    && rm /tmp/dart-sass.tar.gz \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
