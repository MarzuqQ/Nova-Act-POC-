#!/bin/bash
set -e

host="$1"
port="$2"
shift 2
cmd="$@"

echo "Waiting for $host:$port to be available..."

until curl -f "http://$host:$port/api/health" > /dev/null 2>&1; do
  echo "Waiting for $host:$port..."
  sleep 2
done

echo "$host:$port is available!"
exec $cmd 