#!/bin/bash
# train_model.sh

export LIM="64" # Set default project numbers as 64
export JOB = "4"

while [[ $# -gt 0 ]]; do
  key="$1"

  case $key in
    -l|--level)
      export LIM="$2"
      shift  # past argument
      shift  # past value
      ;;
    -j|--job)
      export JOB="$2"
      shift  # past argument
      shift  # past value
      ;;
    *)
      # Unknown option
      shift
      ;;
  esac
done

echo "Dataset is build based on : $LIM projects"
echo "Dataset processed based on : $JOB multi-processors"

cd ..

buildmt build --p raw_projects --l $LIM --j $JOB
echo "Projects download and preprocess finished, start libSA4Py process"

buildmt split --p raw_projects
echo "Projects split ..."

libsa4py process --p raw_projects --o results --s dataset_split.csv --pyre --j $JOB
echo "Projects processed finished"