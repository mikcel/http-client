#!/usr/bin/env bash
HTTPC_LIB="../httpc/dist/httpc"

echo "==== GENERAL HELP ===="
${HTTPC_LIB} help

echo "==== GET HELP ===="
${HTTPC_LIB} help get

echo "==== POST HELP ===="
${HTTPC_LIB} help post


echo "==== GET REQUEST ===="
${HTTPC_LIB} get "http://httpbin.org/get?course=networking&assignment=1"

echo "==== GET REQUEST (with verbose) ===="
${HTTPC_LIB} get -v "http://httpbin.org/get?course=networking&assignment=1"

echo "==== GET REQUEST (with headers) ===="
${HTTPC_LIB} get "http://httpbin.org/get?course=networking&assignment=1" -h Content-Type:application/json

echo "==== GET REQUEST (write to file) ===="
${HTTPC_LIB} get "http://httpbin.org/get?course=networking&assignment=1" -o test_get.json
echo ""
echo ""

echo "==== GET REQUEST (redirect) ===="
${HTTPC_LIB} get "http://httpbin.org/redirect/3"


echo "==== POST REQUEST (inline-data & headers) ===="
${HTTPC_LIB} post "http://httpbin.org/post" -h Content-Type:application/json -d '{"Assignment": 1}'

echo "==== POST REQUEST (inline-data & headers & verbose) ===="
${HTTPC_LIB} post -v "http://httpbin.org/post" -h Content-Type:application/json -d '{"Assignment": 1}'

echo "==== POST REQUEST (from file & headers) ===="
${HTTPC_LIB} post "http://httpbin.org/post" -h Content-Type:application/json -f '../tests/post_data'

echo "==== POST REQUEST (headers & save file) ===="
${HTTPC_LIB} post "http://httpbin.org/post" -h Content-Type:application/json -d '{"Assignment": 1}' -o test_post.json
