FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

ARG NON_ROOT_USER="user"
ARG NON_ROOT_UID="2222"
ARG NON_ROOT_GID="2222"
ARG HOME_DIR="/home/${NON_ROOT_USER}"
ARG REPO_DIR="."

RUN useradd -l -m -s /bin/bash -u ${NON_ROOT_UID} ${NON_ROOT_USER}

ENV PATH "${HOME_DIR}/.local/bin:${PATH}"
RUN mkdir -p ${HOME_DIR}/.cache/uv && chown -R ${NON_ROOT_UID}:${NON_ROOT_GID} ${HOME_DIR}/.cache
ENV UV_CACHE_DIR "${HOME_DIR}/.cache/uv"

COPY --chown=${NON_ROOT_USER}:${NON_ROOT_GID} ${REPO_DIR}/app.py ${HOME_DIR}/app/app.py
COPY --chown=${NON_ROOT_USER}:${NON_ROOT_GID} ${REPO_DIR}/pyproject.toml ${HOME_DIR}/app/pyproject.toml
WORKDIR ${HOME_DIR}/app

RUN uv sync
RUN chown -R ${NON_ROOT_UID}:${NON_ROOT_GID} ${HOME_DIR}

CMD ["uv", "run", "app.py", "--no-cache", " --no-sync"]