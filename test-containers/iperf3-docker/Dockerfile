# iperf3 in a container

FROM archlinux:latest
# install binary and remove cache
#RUN apt-get update \
#   && apt-get install -y iperf3 iproute2 iputils-ping iptables \
#   && apt-get clean \
#   && rm -rf /var/lib/apt/lists/*

RUN pacman -Syu --noconfirm \
    && pacman -Sy --noconfirm iperf3

# Expose the default iperf3 server port
EXPOSE 7070/tcp
EXPOSE 7070/udp

# Include the script that executes the iperf3 command

# Copy entrypoint script
COPY start.sh /usr/local/bin/start.sh
RUN chmod +x /usr/local/bin/start.sh

# entrypoint allows you to pass your arguments to the container at runtime
# very similar to a binary you would run. For example, in the following
# docker run -it <IMAGE> --help' is like running 'iperf3 --help'
ENTRYPOINT ["/usr/local/bin/start.sh"]