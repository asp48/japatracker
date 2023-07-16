#!/bin/sh

base_path="$PWD/configs"
dry_run_path="$base_path/dryrun.ini"
prod_run_path="$base_path/prodrun.ini"
config_path=dry_run_path

if [ $# -gt 0 ]; then
  if [ "$1" == "prodrun" ]; then
    config_path="$prod_run_path"
  elif [ "$1" == "dryrun" ]; then
    config_path="$dry_run_path"
  else
    echo "Unsupported mode. Use (dryrun|prod)"
    exit 1
  fi
fi

cd ../src; PYTHONPATH="$PYTHONPATH:$PWD"; /usr/local/bin/python3.9 japa_tracker.py "$config_path"
exit 0