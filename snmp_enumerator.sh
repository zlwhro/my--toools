#! /bin/bash

address=$(echo $1 |  awk -F '/' '{print $1}')
subnet=$(echo $address | awk -F '.' '{printf("%s.%s.%s",$1,$2,$3)}')

echo public > community
echo private >> community
echo manager >> community


echo $subnet.1 > ips


for i in {2..254}
do
    echo $subnet.$i >>  ips
done

onesixtyone -c community -i ips > snmp_scan

echo "scan finished"

while IFS= read -r line
do
    echo $line
    if [[ $line == *"Windows"* ]]; then
        echo "start enumeration Window machine"
        while IFS= read -r leaf
        do
            num=$(echo $leaf | cut -d ':' -f 1)            
            value=$(echo $leaf | cut -d ':' -f 2)
            echo "try enumerate $value"

            snmpwalk -c public -v1 -t 10 $(echo $line| cut -f1 )
        done < window_MIB
    fi
done < snmp_scan








