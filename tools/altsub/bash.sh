result=`python3 test1.py`
temp_index=`echo $result | grep -b -o "server" | cut -d ":" -f1`
index=`expr $temp_index + 10`


server=`echo $result | cut -c$index-| cut -d "," -f1 `
status=`echo $result  | cut -d "{" -f1`

echo $server $status
