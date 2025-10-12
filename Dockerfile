FROM python:3.14.0-slim

# Install system dependencies (Terraform, curl, wget, git)
RUN apt-get update && apt-get install -y \
    bash \
    wget \
    unzip \
    curl \
    git \
    sudo \
    nano \
    && apt-get clean

RUN echo "vscode ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

SHELL ["/bin/bash", "-c"]
# Install Terraform
RUN wget https://releases.hashicorp.com/terraform/1.7.5/terraform_1.7.5_linux_amd64.zip && \
    unzip terraform_1.7.5_linux_amd64.zip && \
    mv terraform /usr/local/bin/ && \
    rm terraform_1.7.5_linux_amd64.zip


# Set up a non-root user for security
RUN useradd -m vscode

# Set environment PATH globally for all shells (interactive & non-interactive)
ENV PATH="/home/vscode/.local/bin:${PATH}"

USER vscode

# Set the working directory for the app
WORKDIR /workspace

EXPOSE 8000