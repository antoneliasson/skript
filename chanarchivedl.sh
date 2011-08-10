#!/bin/bash
# Downloads every image in a chanarchive thread, preserving the original filename
# and modification time.

if [ "$1" = "" ]; then # no arguments
	echo "Usage: `basename $0` <chanarchive url> [optional download directory]"
	exit 1
fi

if [ "$2" = "" ]; then # only one argument
	LOC=$(echo "$1" | awk -F / '{print $7}' ) # find out the thread nickname
else
	LOC=$2 # use download dir specified by user
fi
echo "chanarchive downloader"
echo "Downloading to \"$LOC\""

if [ ! -d $LOC ]; then # fixa detta, ladda inte ner om katalogen finns och ladda verkligen inte ner om namnet är en fil som existerar!
	mkdir -- $LOC
fi

cd -- $LOC # new directory named after the thread number

	# chanarchive uses both the org and com topdomains
	LINK=$(echo $1 | sed 's/chanarchive.com/chanarchive.org/')

	TMP1=`mktemp` # the html thread
	TMP2=`mktemp` # image links extracted from the thread
	TMP3=`mktemp` # original image links extracted from the thread

    # get thread
    echo "Updating..."
	wget -k -q -O "$TMP1" "$LINK"
	if [ "$?" != "0" ]; then
		echo "Update failed, exiting"
		rm $TMP1 $TMP2 $TMP3
		exit 1
	fi

    # get file list, space separated
	grep -E -o 'http://chanarchive.org/content/[a-z0-9_]+/[0-9]+/([0-9]*).(jpg|png|gif)' "$TMP1" | uniq | tr "\n" " " > "$TMP2"

	# get original file name list, space separated (spaces in filenames changed to underlines)
	sed 's/ /_/g' "$TMP1" | grep -E -o '<span_title=\"[[:alnum:]_-]*.*(jpg|png|gif)' | awk -F \" '{print $2}' | tr "\n" " " > "$TMP3"

	COUNT=`cat $TMP3 | wc -w` # total number of files/names
	for ((i=1; i<=$COUNT; i++)); do
		# chanarchive requires a HTTP referer field in the header. The referer could be anybody or none though.
		wget --referer= -nv -nc -O `cut -d ' ' -f $i $TMP3` `cut -d ' ' -f $i $TMP2` # now download all files, one by one
	done # hojta till om vilket nummer i ordningen vi är på mellan varje
	
	rm $TMP1 $TMP2 $TMP3

