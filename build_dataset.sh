#!/bin/bash
# train_model.sh

export LIM="64" # Set default project numbers as 64

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

cd ..

buildmt build --p raw_projects --l $LIM
echo "Projects download and preprocess finished, start libSA4Py process"

buildmt split --p raw_projects
echo "Projects splitted ..."

libsa4py process --p raw_projects --o results --s dataset_split.csv --pyre --j 8
echo "Projects processed finished"