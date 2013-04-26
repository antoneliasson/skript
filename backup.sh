#!/bin/sh

src="$HOME"
dest="file:///Athena/Backup/$(hostname)"

duplicity --full-if-older-than 14D \
    --asynchronous-upload \
    --volsize 50 \
    --no-encryption \
    --log-file "$HOME/duplicity.log" \
    --exclude "$HOME/.cache/" \
    --exclude-other-filesystems \
    --no-print-statistics \
    --verbosity warning \
    "$src" "$dest"
