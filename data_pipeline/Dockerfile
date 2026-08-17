FROM python:3.13.11-slim

# --from indica ao comando COPY para copiar o conteúdo de uma docker image e não da host machine.
# o que o comando faz é pega o /uv da docker image do uv e insere o conteúdo dentro do diretório /bin/ dos containers desta docker image.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

WORKDIR /code
# makes linux checks first the given path for binaries, if it encounters (for instance python), it will execute it first than other binaries located on the default folders (e.g. usr/local/bin)
ENV PATH="/code/.venv/bin:$PATH"
# this also avoids defining uv run command on the ENTRYPOINT, which avoids the overhead existing when using the uv to search for its environment binaries. 
# Linux launches uv -> uv validates project state & .venv -> uv spawns python. UV overhead process.

# Whereas running the python binary within the uv venv directy, it takes zero overhead.
# files created by uv locally and necessary for its right work and dependency assurance,
COPY pyproject.toml .python-version uv.lock ./

# install dependencies created locally (stored on uv.lock). UV also checks for changes made.
RUN uv sync --locked 

COPY pipeline.py .

ENTRYPOINT ["python", "pipeline.py"]