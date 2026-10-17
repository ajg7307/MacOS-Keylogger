#!/bin/zsh
cd -- "${0:A:h}" || exit 1
./InputDemo
result=$?
printf '\nDemo exited (status %s). Press Return to close.\n' "$result"
read -r
exit "$result"
