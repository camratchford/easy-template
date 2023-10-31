#!/bin/sh

git clone https://github.com/camratchford/FastAPI-Template template_repo
ezt -d 'template_repo' \
    -V 'template_vars.yml' \
    -o 'GoodServer'