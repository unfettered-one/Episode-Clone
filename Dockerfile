FROM python:3.11-slim

# Install system dependencies (Terraform, curl, wget, git)
RUN apt-get update && apt-get install -y \
    bash \
    wget \
    unzip \
    curl \
    git \
    && apt-get clean
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
# RUN echo 'parse_git_branch() { git branch 2>/dev/null | grep "^*" | awk "{print \\$2}"; }' >> /home/vscode/.bashrc && \
#     echo 'export PS1="\\u@\\h:\\w \\[\\033[32m\\]\\$(parse_git_branch)\\[\\033[00m\\]\\$ "' >> /home/vscode/.bashrc
# Set Git branch in prompt for both bash and sh
# RUN echo 'parse_git_branch() { git branch 2>/dev/null | grep "^*" | awk "{print \\$2}"; }' >> /home/vscode/.bashrc && \
#     echo 'export PS1="\\u@\\h:\\w \\[\\033[32m\\]\\$(parse_git_branch)\\[\\033[00m\\]\\$ "' >> /home/vscode/.bashrc && \
#     echo 'export PS1="\\u@\\h:\\w `git rev-parse --abbrev-ref HEAD 2>/dev/null`\\$ "' >> /home/vscode/.profile

# Set prompt in bash with dynamic git branch
RUN echo 'parse_git_branch() { git branch 2>/dev/null | grep "^*" | awk "{print \$2}"; }' >> /home/vscode/.bashrc && \
    echo 'export PS1="\\u@\\h:\\w \\[\\033[32m\\]\\$(parse_git_branch)\\[\\033[00m\\]\\$ "' >> /home/vscode/.bashrc && \
    \
    # Set prompt in sh (branch resolved once at shell start)
    echo 'BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)' >> /home/vscode/.profile && \
    echo 'export PS1="\\u@\\h:\\w ($BRANCH)\\$ "' >> /home/vscode/.profile
