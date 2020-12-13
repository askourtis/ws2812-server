#!/bin/bash

NAME=smart-leds-server
LOCK=./lock.pid

if [[ "$#" -ne 1 ]]; then
    echo "Accepting exactly one argument, start or stop" >&2
    exit 1
fi

if [[ "$1" == "start" ]]; then
    if ! [[ -f "$LOCK" ]]; then
        screen -dmS "$NAME" bash -c "sudo ./src/script.py" &
        echo $! > $LOCK
        echo "Started"
    else
        echo "Already started" >&2
        exit 1
    fi
elif [[ "$1" == "stop" ]]; then
    if [[ -f "$LOCK" ]]; then
        screen -X -S "$NAME" stuff "^C"
        rm $LOCK
        echo "Stopped"
    else
        echo "Not started" >&2
        exit 1
    fi
else
    echo "Argument $1 was not recognized, only start or stop is allowed" >&2
    exit 1
fi
