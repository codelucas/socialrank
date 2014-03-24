#!/bin/bash

LOCKFILE=/tmp/update_lock.txt
if [ -e ${LOCKFILE} ] && kill -0 `cat ${LOCKFILE}`; then
    #echo "update already running"
    #exit
    pkill -TERM -P `cat ${LOCKFILE}`;
    echo "We just killed" `cat ${LOCKFILE}` "and are proceding with updating news";
fi

# make sure the lockfile is removed when we exit and then claim it
trap "rm -f ${LOCKFILE}; exit" INT TERM EXIT
echo $$ > ${LOCKFILE}

cd /home/lucas/www/socialrank.lucasou.com/socialrank-env/socialrank; ../bin/python2.7 manage.py update;

rm -f ${LOCKFILE}
