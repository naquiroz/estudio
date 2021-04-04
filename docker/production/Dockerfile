# Environment setter image
FROM python:3.9-slim-buster AS environment

WORKDIR /app
RUN mkdir estudio
COPY ./estudio ./estudio

# Set up environmental variables
ENV DJANGO_ENV=PRODUCTION \
    LANG=C.UTF-8 \
    # python:
    PYTHONFAULTHANDLER=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # poetry
    POETRY_VERSION=1.1.5

# Set up base workdir
WORKDIR /app

# Install OS package dependencies
RUN apt-get update && \
    rm -rf /var/lib/apt/lists/* && \
    # Install poetry
    pip install "poetry==$POETRY_VERSION"

# Setup the virtualenv
RUN python -m venv /venv

# Copy project dependency files to image
COPY pyproject.toml poetry.lock ./

# Export and install all of our dependencies and subdependencies with pip.
# While tempting, we *should not* use a pipe operator for this process,
# as we may run into issues if Poetry throws a warning into the stdout.
RUN poetry export --format requirements.txt --output fulldependencies.txt && \
    /venv/bin/pip install --requirement fulldependencies.txt && \
    rm fulldependencies.txt

# --------------------------------------------------------

# Final image
FROM python:3.9-slim-buster AS final

# Add django secret key
ARG DJANGO_SECRET_KEY

# Set up environmental variables
ENV LANG=C.UTF-8 \
    DJANGO_ENV=PRODUCTION

# Set up base workdir
WORKDIR /app

# Get virtual environment
COPY --from=environment /venv /venv

# Use executables from the virtual env
ENV PATH="/venv/bin:$PATH"

# Copy files to image
COPY . .

# Get web build
COPY --from=web-build /app/estudio/static/ ./estudio/static

# Move to project folder
WORKDIR /app/estudio

# Collect static assets
RUN /venv/bin/python manage.py collectstatic --noinput

# Add a script to be executed every time the container starts.
COPY entrypoint.sh /usr/bin/
RUN chmod +x /usr/bin/entrypoint.sh
ENTRYPOINT ["entrypoint.sh"]

# Run as non-root user
RUN useradd -m euser
USER euser

# Start the main process.
CMD ["/bin/bash", "./run.sh"]
