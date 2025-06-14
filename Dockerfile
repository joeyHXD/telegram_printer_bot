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
USER ${NON_ROOT_USER}
WORKDIR ${HOME_DIR}

COPY --chown=${NON_ROOT_USER}:${NON_ROOT_GID} ${REPO_DIR} ${HOME_DIR}/app
WORKDIR ${HOME_DIR}/app

RUN uv sync

CMD ["uv", "run", "app.py"]