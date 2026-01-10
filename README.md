# oneManShow
# Build and run the mcp servers so that windsurf client can connect to them
``` bash
#!/bin/bash
if ! docker image inspect mcp/mem0 > /dev/null 2>&1; then
  echo "Image not found. Building..."
  docker build -t mcp/mem0 --build-arg PORT=8050 .
else
  echo "Image already exists. Skipping build."
fi

docker run --env-file .env -p 8050:8050 mcp/mem0

if ! docker image inspect mcp/crawl4ai-rag > /dev/null 2>&1; then
  echo "Image not found. Building..."
  docker build -t mcp/crawl4ai-rag --build-arg PORT=8051 .
else
  echo "Image already exists. Skipping build."
fi

docker run --env-file .env -p 8051:8051 mcp/crawl4ai-rag

```