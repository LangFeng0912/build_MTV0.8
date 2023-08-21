#!/bin/bash
# train_model.sh

export LIM="64" # Set default project numbers as 256

while [[ $# -gt 0 ]]; do
  key="$1"

  case $key in
    -l|--level)
      export LIM="$2"
      shift # past argument
      shift # past value
      ;;
    *)
      # Unknown option
      shift
      ;;
  esac
done

echo "Dataset is build based on : $LIM projects"

buildmt build --p raw_projects --l $LIM
libsa4py process --p raw_projects --o results --pyre --j 4
