if [ ${APP_CONFIG_MODE} ]; then
  echo "APP_CONFIG_MODE set from enviroment variable to ${APP_CONFIG_MODE}"
else
  if [ -e `pwd -P`/config/$1.py ]; then
    m=$1
    shift
  else
    m="test"
  fi
  export APP_CONFIG_MODE=$m
fi

export FLASK_APP=app
python -m unittest $@
