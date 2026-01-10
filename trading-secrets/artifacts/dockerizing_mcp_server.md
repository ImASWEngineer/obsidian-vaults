# Dockerizing the Zettelkasten MCP Server

This document outlines the process of containerizing the Zettelkasten MCP server using Docker. This approach provides a consistent, isolated, and reproducible environment for running the server, simplifying dependency management and deployment.

## Analysis of Similar Projects

To inform the process, I analyzed existing MCP server projects that utilize Docker:

*   **`ckreiling/mcp-server-docker`**: This repository was a key reference. It demonstrated a standard pattern for dockerizing a Python-based MCP server, although it used `pip` and `requirements.txt`. The core concepts of using a Python base image, installing dependencies, copying source code, and defining a `CMD` were adopted from this example.
*   **`Automata-Labs-team/code-sandbox-mcp`**: This Node.js project confirmed the general Docker pattern across different languages: define a base image, manage dependencies, copy application code, and specify a startup command.

These examples provided a solid foundation for creating a `Dockerfile` tailored to the `zettelkasten-mcp` project's use of the `uv` package manager.

## Dockerfile

Here is the `Dockerfile` created to build an image for the Zettelkasten MCP server. It is placed in the root of the `zettelkasten-mcp` repository.

```dockerfile
# Dockerfile for zettelkasten-mcp

# Stage 1: Build environment with uv
FROM python:3.11-slim-bookworm AS builder

# Install curl to download uv
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Stage 2: Final application image (using a more specific base image)
FROM python:3.11-slim-bookworm AS final

# Set environment variables to prevent buffering of stdout/stderr
ENV PYTHONUNBUFFERED=1

# Copy uv from the builder stage
COPY --from=builder /root/.cargo/bin/uv /usr/local/bin/

# Set the working directory in the container
WORKDIR /app

# Copy dependency definition and source code
COPY pyproject.toml ./
COPY src/ ./src/

# Install the project and its dependencies using uv.
# We install into the system Python environment, which is standard for containers.
RUN uv pip install --system -e . --all-extras

# Default environment variables for data paths inside the container.
# These can be overridden at runtime.
ENV ZETTELKASTEN_NOTES_DIR=/data/notes
ENV ZETTELKASTEN_DATABASE_PATH=/data/db/zettelkasten.db
ENV ZETTELKASTEN_LOG_LEVEL=INFO
# Default to SSE in Docker
ENV ZETTELKASTEN_TRANSPORT=sse
# Listen on all interfaces
ENV ZETTELKASTEN_HOST=0.0.0.0
ENV ZETTELKASTEN_PORT=8052 # Default SSE port

# Create mount points for data and declare them as volumes for persistent storage.
RUN mkdir -p /data/notes /data/db
VOLUME ["/data/notes", "/data/db"]

# Expose the port for SSE transport (matching ZETTELKASTEN_PORT)
EXPOSE 8052

# Command to run the application in SSE mode
CMD ["python", "-m", "zettelkasten_mcp.main", "--transport", "sse", "--host", "0.0.0.0", "--port", "8052"]
```

### Key Decisions in the Dockerfile

*   **Base Image**: `python:3.11-slim` was chosen for its small footprint while providing a standard Python environment.
*   **Multi-Stage Build**: A multi-stage build is used to install `uv` in a temporary `builder` stage. Only the `uv` binary is copied to the final image, keeping it clean and small without including `curl` and other build-time tools.
*   **Dependency Management**: `uv` is used for package installation, as specified in the project's `README.md`. The command `uv pip install --system -e . --all-extras` installs the project in editable mode along with all its dependencies, including optional ones, directly into the system's Python environment.
*   **Data Persistence**: The container's data directories (`/data/notes` and `/data/db`) are managed via Docker volumes. This crucial step separates the application's stateless container from the user's stateful knowledge base, ensuring that notes and the database index are not lost when the container is stopped or removed.
*   **Configuration**: Key settings like data paths are controlled via environment variables (`ZETTELKASTEN_NOTES_DIR`, `ZETTELKASTEN_DATABASE_PATH`), making the image flexible and easily configurable at runtime.
*   **Entrypoint**: The `CMD` is set to `["python", "-m", "zettelkasten_mcp.main"]`, which is the standard command to run the server.

## Docker Compose

For a better user experience, a `docker-compose.yml` file is recommended. It simplifies running the container with the correct volume mounts and environment variables.

```yaml
# docker-compose.yml
version: '3.8'

services:
  zettelkasten:
    build: .
    image: zettelkasten-mcp-server
    container_name: zettelkasten-mcp
    volumes:
      - ./data/notes:/data/notes
      - ./data/db:/data/db
    # Since this is an stdio server, we run it interactively.
    # For Claude Desktop, it will manage the process.
    # For local testing, you can use 'docker-compose run'.
    stdin_open: true # -i
    tty: true        # -t
```

## How to Build and Run

1.  **Build the Docker image**: Navigate to the `zettelkasten-mcp` project root and run:
    ```bash
    docker build -t zettelkasten-mcp-server .
    ```
2.  **Run using Docker Compose**:
    *   Create the `docker-compose.yml` file in the project root.
    *   Ensure you have local `data/notes` and `data/db` directories.
    *   Run the server: `docker-compose up`.

## Integrating with Claude Desktop

To use the Dockerized server with Claude Desktop, you must configure it to execute a `docker run` command. Edit your `claude_desktop_config.json` file as follows.

**Important**: Replace `/absolute/path/to/zettelkasten-mcp` with the actual absolute path to your project directory on your host machine.

```json
{
  "mcpServers": {
    "zettelkasten-docker": {
      "command": "docker",
      "args": [
        "run", "--rm", "-i",
        "-v", "/absolute/path/to/zettelkasten-mcp/data/notes:/data/notes",
        "-v", "/absolute/path/to/zettelkasten-mcp/data/db:/data/db",
        "zettelkasten-mcp-server"
      ]
    }
  }
}
```

This configuration instructs Claude to start a new, temporary (`--rm`) container from the `zettelkasten-mcp-server` image for each interaction. The `-i` flag enables interactive mode for the `stdio` transport, and the `-v` flags mount your local data directories into the container.