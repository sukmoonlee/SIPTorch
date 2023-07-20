#!/bin/bash
################################################################################
# Generate Report based on output file
# 2023.07.19 created by smlee@sk.com
################################################################################

filename=$1
if [ ! -f "$filename" ] ; then
	echo "error: file is not exist ($filename)"
	echo ""
	echo "Usage: $0 [filename]"
	exit 1
fi

declare -A report_array
flag=0
while read -r i_line
do
	#echo "$flag $i_line"
	if [ "${i_line:0:9}" == "### Test:" ] ; then
		test_title=${i_line:10}
	fi
	if [ "${i_line:0:11}" == "- Category:" ] ; then
		test_category=${i_line:12}
	fi
	if [ "${i_line:0:5}" == "- ID:" ] ; then
		test_id=${i_line:6}
		test_id=${test_id//\`/}
	fi
	if [ "${i_line:0:11}" == "- Response:" ] ; then
		flag=1
	fi
	if [ "${i_line:0:26}" == "- Response Received Later:" ] ; then
		flag=1
	fi
	if [ "$flag" == "0" ] ; then continue; fi
	if [ "$flag" == "1" ] && [ "${i_line:0:3}" == "\`\`\`" ] ; then flag=2; test_result=; continue; fi
	if [ "$flag" == "2" ] && [ "$test_result" == "" ] ; then test_result="$i_line"; fi
	if [ "$flag" == "2" ] && [ "${i_line:0:3}" == "\`\`\`" ] ; then
		flag=0
		if [ "${test_result:0:3}" == "\`\`\`" ] ; then test_result=; fi
		#echo "$test_category|$test_id|$test_title|$test_result"
		report_array["$test_category|$test_title|$test_id"]="$test_result"
	fi
done < <(cat "$filename")

for key in "${!report_array[@]}"
do
	echo "$key|${report_array[$key]}"
done | sort
