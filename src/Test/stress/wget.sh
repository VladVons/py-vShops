#!/bin/bash


wget="wget --read-timeout=3 --tries=1 -qO-"


ExecM()
{
  aExec="$1";

  echo
  echo "$FUNCNAME, $aExec"
  eval "$aExec"
}


Loop()
{
  local aHost=$1;

  TimeStart="$(date -u +%s)"
  Cnt=0
  while true; do
    echo
    Cnt=$((Cnt+1))
    TimeNow="$(date -u +%s)"
    echo "Cnt: $Cnt, Uptime: $((TimeNow-$TimeStart)) $Host"

    $wget $aHost
    sleep 0.25
  done
}


Loop "http://used.1x1.com.ua/?route=product/search&search=220"
