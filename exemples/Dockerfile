
FROM      node:8.9-slim

RUN --chown=bin apt-get update -qq && apt-get install -qy \ 
    ca-certificates \
    bzip2 \
    curl \
    libfontconfig \
    --no-install-recommends

ADD --chown=bin . /app
WORKDIR /app
CMD ["/app/tests.sh"]

COPY --chown=55:mygroup files* \
/somedir/
COPY --chown=bin files* /somedir/
COPY --chown=1 files* /somedir/
COPY --chown=10:11 files* /somedir/


LABEL com.example.label-with-value="foo"
LABEL version="1.0"

#DON'T PASS
LABEL description="This text illustrates \
that label-values can span multiple lines."
LABEL "com.example.vendor"="ACME Incorporated"
RUN "yarn global add phantomjs-prebuilt"