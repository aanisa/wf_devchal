if [ -e `pwd -P`/config/$1.py ]; then
  m=$1
  shift
else
  m="test"
fi
export APP_CONFIG_MODE=$m
export FLASK_APP=app

python -m unittest $@
