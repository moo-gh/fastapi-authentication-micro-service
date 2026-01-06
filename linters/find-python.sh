#!/usr/bin/env bash

set -e

find app \
	-type f -name "*.py" \
	-exec "$@" {} +
