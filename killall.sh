#!/bin/sh
for name in `find /opt/matrix/service/*.py` ; do $name stop;  done
