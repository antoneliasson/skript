#!/bin/bash

src="$HOME"
dest="hermes:/Athena/Backup/bup"
branch="$(hostname)-$(whoami)"
exclude_file="$HOME/.exclude-from-backup"

bup index --one-file-system --exclude-from="$exclude_file" "$src"

bup save --name="$branch" --remote="$dest" "$src"
