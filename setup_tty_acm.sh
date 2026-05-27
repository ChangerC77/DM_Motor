#!/usr/bin/env bash
set -euo pipefail

shopt -s nullglob
ports=(/dev/ttyACM*)

if ((${#ports[@]} == 0)); then
  echo "No /dev/ttyACM* serial ports found."
  exit 1
fi

echo "Found serial port(s):"
ls -l "${ports[@]}"
echo

if ((${#ports[@]} == 1)); then
  port="${ports[0]}"
else
  echo "Select the serial port to authorize:"
  for i in "${!ports[@]}"; do
    printf '  [%d] %s\n' "$((i + 1))" "${ports[$i]}"
  done

  read -rp "Enter number: " choice
  if ! [[ "$choice" =~ ^[0-9]+$ ]] || ((choice < 1 || choice > ${#ports[@]})); then
    echo "Invalid selection: $choice"
    exit 1
  fi

  port="${ports[$((choice - 1))]}"
fi

echo "Setting permission: sudo chmod 777 $port"
sudo chmod 777 "$port"

echo "Done:"
ls -l "$port"
