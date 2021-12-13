FROM --platform=linux/arm64/v8 ubuntu as os-base

ARG BITCOIN_VERSION
ENV PATH=/opt/bitcoin-${BITCOIN_VERSION}/bin:$PATH

FROM os-base as bitcoind-install
RUN apt-get update -y \
  && apt-get install -y curl gosu curl unzip jq bash-completion \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN curl -SLO \
https://bitcoin.org/bin/bitcoin-core-22.0/bitcoin-22.0-arm-linux-gnueabihf.tar.gz \
#https://bitcoin.org/bin/bitcoin-core-${BITCOIN_VERSION}/bitcoin-${BITCOIN_VERSION}-x86_64-linux-gnu.tar.gz \
  && tar -xzf *.tar.gz -C /opt \
  && rm *.tar.gz
# Install runtime scripts, bash-completion and configuration files

# bash completion for bitcoind and bitcoin-cli
ENV GH_URL https://raw.githubusercontent.com/bitcoin/bitcoin/master/
ENV BC /usr/share/bash-completion/completions/
ADD $GH_URL/contrib/bitcoin-cli.bash-completion $BC/bitcoin-cli
ADD $GH_URL/contrib/bitcoind.bash-completion $BC/bitcoind
ADD $GH_URL/contrib/bitcoin-tx.bash-completion $BC/bitcoin-tx

# Copy bitcoind configuration directory
COPY bitcoind /bitcoind
RUN ln -s /bitcoind /root/.

# Copy support scripts
COPY bashrc /root/.bashrc
COPY bitcoind-entrypoint.sh /usr/local/bin
RUN chmod +x /usr/local/bin/bitcoind-entrypoint.sh
COPY mine.sh /usr/local/bin
RUN chmod +x /usr/local/bin/mine.sh
COPY cli /usr/local/bin
RUN chmod +x /usr/local/bin/cli

# bitcoind P2P
EXPOSE 18444/tcp
# bitcoind regtest RPC
EXPOSE 18443/tcp
# zmqpubrawblock
EXPOSE 12005/tcp
# zmqpubrawtx
EXPOSE 12006/tcp

WORKDIR /bitcoind
ENTRYPOINT ["/usr/local/bin/bitcoind-entrypoint.sh"]

# Mine new block every 10 seconds
CMD ["/usr/local/bin/mine.sh"]
