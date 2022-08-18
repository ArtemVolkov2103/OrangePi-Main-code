#!/bin/sh
cd '/home/orangepi/Documents/python/'
git fetch
git checkout up-to-date-code
git add -A
git commit -m "ok"
git push origin-master
