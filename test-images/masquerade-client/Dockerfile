# Use the official Rust image as the base
FROM rust:1.80-slim as builder

RUN apt update
RUN apt-get install -y --no-install-recommends git cmake make g++ gcc
RUN git clone https://github.com/ErikBcd/masquerade.git 

#COPY ./masquerade ./masquerade
WORKDIR /masquerade
#COPY server_config.toml /masquerade/config/server_config.toml
RUN cargo build --release

# Use a minimal base image to run the compiled program
FROM debian:bookworm-slim

# Install necessary tools
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    iproute2 iputils-ping iptables libc6 procps && \
    rm -rf /var/lib/apt/lists/*

# Copy the compiled program from the builder stage
COPY --from=builder /masquerade/target/release/connect_ip_client /usr/local/bin/connect_ip_client
COPY client_config.toml ./client_config.toml
#COPY --from=builder /masquerade/config ./config/

# Ensure the container has necessary capabilities for networking
RUN apt-get install -y  iproute2 iputils-ping && \
    mkdir -p /dev/net && \
    if [ ! -c /dev/net/tun ]; then \
        mknod /dev/net/tun c 10 200; \
    fi && \
    chmod 600 /dev/net/tun

# Copy entrypoint script
COPY start.sh /usr/local/bin/start.sh
RUN chmod +x /usr/local/bin/start.sh

# Expose necessary ports

# Command to run when the container starts
ENTRYPOINT ["/usr/local/bin/start.sh"]