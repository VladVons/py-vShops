#!/bin/bash

#curl -X POST -H "Content-Type: application/json" -d '{"key1":"value1", "key2":"value2"}' http://localhost:8080/tenant/?route=common/filemanager
curl -X POST -H "Content-Type: application/json" -d '{"method": "ajax", "key1":"value1"}' http://localhost:8080/tenant/api/?route=common/filemanager
#
#curl -X POST -H "Content-Type: application/json" -d '{"key1":"value1", "key2":"value2"}' http://localhost:8080/post-example
#curl -X POST -H "Content-Type: application/json" -d '{"name": "John", "age": 25}' http://127.0.0.1:8080/post-example
#curl -X POST -d "key1=value1&key2=value2" http://127.0.0.1:8080/post-example
