if [ -e `pwd -P`/config/$1.py ]; then
  e=$1
  shift
else
  e="test"
fi
export APP_CONFIG_FILE=`pwd -P`/config/$e.py
export FLASK_APP=app

python -m unittest $@
