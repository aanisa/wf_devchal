#!/bin/sh

if [ ${APP_CONFIG_MODE} ]; then
  echo "APP_CONFIG_MODE set from enviroment variable to ${APP_CONFIG_MODE}"
else
  if [ -e `pwd -P`/config/$1.py ]; then
    m=$1
    shift
  else
    m="development"
  fi
  export APP_CONFIG_MODE=$m
fi

if [ $m = "development" ]; then
  export FLASK_DEBUG=1
fi

export FLASK_APP=app
python -m flask $@
