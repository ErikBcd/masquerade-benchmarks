#!/bin/bash

docker buildx build --tag wg_lossy . --network=host 