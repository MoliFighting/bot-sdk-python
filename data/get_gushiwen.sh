for i in `seq 1 3`; do 
    # echo $i; 
    url="https://so.gushiwen.org/mingju/default.aspx?p=$i&c=&t=";
    echo $url;
    curl $url > gushiwen/$i.html;
    sleep 5;
done