FROM debian:12.5-slim
RUN apt update && apt install -y dnsmasq
EXPOSE 53 53/udp
ENTRYPOINT ["dnsmasq", "-k"]
