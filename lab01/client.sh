#!/bin/bash

echo "Number: "
read number
echo '' > wyniki.txt
echo $number > clientResult.txt

cond=0
value=`cat wyniki.txt`
while [ $cond -eq 0 ]
do
    if [[ $value -ne '' ]]
    then
        echo '' > wyniki.txt
        ((cond++))
    else
        value=`cat wyniki.txt`
    fi
    
done

echo $value
# echo '' > wyniki.txt
