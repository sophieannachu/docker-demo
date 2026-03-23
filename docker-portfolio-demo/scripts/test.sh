#!/usr/bin/env bash
set -e

echo "[1] health check"
curl -s http://localhost:5000/health | jq .

echo "[2] home"
curl -s http://localhost:5000/ | jq .

echo "[3] visits"
curl -s http://localhost:5000/visits | jq .
