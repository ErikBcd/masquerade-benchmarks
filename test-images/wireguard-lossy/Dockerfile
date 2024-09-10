FROM lscr.io/linuxserver/wireguard:latest

COPY start.sh /usr/local/bin/start.sh
RUN chmod +x /usr/local/bin/start.sh

# Command to run when the container starts
ENTRYPOINT ["/usr/local/bin/start.sh"]