#!/bin/bash

while true
do
        value=`cat clientResult.txt`
        echo '' > clientResult.txt
        result=$(($value))
        echo $result > wyniki.txt
        clear
done
