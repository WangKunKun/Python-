 #!/bin/bash

 PATH=/bin:/usr/local/bin:~/bin:/sbin:/usr/bin
 export PATH

: 函数区域

filter()
{
	filtArr=("guide_" "_support") #过滤 某些组合的 防止误删，组合形式真的太糟心·· 
	num=${#filtArr[@]}
	fileName=$1
	result="0"
	for (( i = 0; i < $num; i++ )); do
		name=${filtArr[i]}
		if [[ "$fileName" =~ "$name" ]];then
			result="1"
			break
		fi
	done
	echo $result
}


#find太慢了
echo "=========开始检测======="
for i in `find ./MKWeekly/MKWeekly/Assets.xcassets -name "*.imageset"`; do
	file=`basename -s .jpg "$i" | xargs basename -s .imageset`
	echo "图片名 $file"
	numfile=`echo $file | sed 's:[0-9]*$::'` #如果最后以数字结尾，则数字替换
	result=`ack "\"$file\""`
	if [[ "$file" = "$numfile" ]]; then
		if [ -z "$result" ]; then 
			echo "=========开始过滤======="
			filterResult=`filter $file`
			if [[ "$filterResult" = "0" ]]; then
				echo "需要删除 $i"
				rm -rf $i
			fi
			echo "=========完成过滤======="
	 	fi
	else
	 	numfile="\"${numfile}%ld\""
	 	if [ -z "$result" ]; then 
		 	result=`ack -i "$numfile"`
	     	if [ -z "$result" ]; then 
				echo "=========开始过滤======="
				filterResult=`filter $file`
	    		if [[ "$filterResult" = "0" ]]; then
	    			echo "需要删除 $i"
	    			rm -rf $i
	    		fi
	    		echo "=========完成过滤======="
	  		fi
	 	fi
	fi
done
echo "========检测完毕========"