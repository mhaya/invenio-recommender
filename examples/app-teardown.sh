#!/bin/sh

# quit on errors:
set -o errexit

# quit on unbound symbols:
set -o nounset

DIR=`dirname "$0"`

cd $DIR
export FLASK_APP=app.py

flask db drop --yes-i-know

# Teardown app
[ -e "$DIR/static" ] && rm -Rf $DIR/static/
[ -e "$DIR/instance" ] && rm -Rf $DIR/instance/

[ -e "$DIR/app.db" ] && rm -f $DIR/app.db