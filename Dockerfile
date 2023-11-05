# ==============================================================================
# This is the dockerfile movie index.
# ==============================================================================
FROM python:3.10.13-bookworm

# ------------------------------------------------------------------------------
# Add arguments and ENV variables.
# ------------------------------------------------------------------------------
ARG USERNAME=u_movie_index \
    USER_UID=1000 \
    USER_GID=1000 \
    HOMEDIR=/home/u_movie_index

# ------------------------------------------------------------------------------
# Install apt packages.
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Add non-root user.
# ------------------------------------------------------------------------------
ARG USERNAME=u_movie_index \
    USER_UID=1000 \
    USER_GID=1000 \
    HOMEDIR=/home/u_movie_index

RUN groupadd --gid $USER_GID $USERNAME && \
    useradd --uid $USER_UID --gid $USER_GID -m $USERNAME && \
    chown $USER_UID:$USER_GID $HOMEDIR

WORKDIR $HOMEDIR
USER $USERNAME

# ------------------------------------------------------------------------------
# Install python into this docker container.
# ------------------------------------------------------------------------------
COPY --chown=$USER_UID:$USER_GID .dist ./.dist
RUN python3 -m pip install .dist/* && \
    rm -rf ./dist

# ------------------------------------------------------------------------------
# Entry point for this docker container.
# ------------------------------------------------------------------------------
ENTRYPOINT [ "/usr/local/bin/python3", "-m", "movie_index" ]
