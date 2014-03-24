#!/bin/bash

LOCKFILE=/tmp/generate_lock.txt
if [ -e ${LOCKFILE} ] && kill -0 `cat ${LOCKFILE}`; then
    #echo "generate already running"
    #exit
    #kill $(cat ${LOCKFILE});
    pkill -TERM -P `cat ${LOCKFILE}`;
    echo "We just killed" `cat ${LOCKFILE}` "and are proceding to generate news";
fi

# make sure the lockfile is removed when we exit and then claim it
trap "rm -f ${LOCKFILE}; exit" INT TERM EXIT
echo $$ > ${LOCKFILE}

cd /home/lucas/www/socialrank.lucasou.com/socialrank-env/socialrank; ../bin/python2.7 manage.py generate;

rm -f ${LOCKFILE}
