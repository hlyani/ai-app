#!/bin/bash

export LD_LIBRARY_PATH=/home/HwHiAiUser/Ascend/acllib/lib64:/home/HwHiAiUser/ascend_ddk/arm/lib:/home/HwHiAiUser/ascend_ddk/arm/lib

echo "Prepare input data..."
ssh-keygen -R ${OUT_HOST}
echo "sshpass -p ${OUT_PASSWORDD} scp -o StrictHostKeyChecking=no -r ${OUT_USER}@${OUT_HOST}:${IN_PATH}/* $HOME/data/"
sshpass -p ${OUT_PASSWORDD} scp -o StrictHostKeyChecking=no -r ${OUT_USER}@${OUT_HOST}:${IN_PATH}/* $HOME/data/

echo "Unpack model..."
mkdir -p $HOME/AscendProjects
tar -zxvf $HOME/colorization.tgz -C $HOME/AscendProjects/
# cd $HOME/AscendProjects/colorization
# mkdir -p build/intermediates/host
# cd build/intermediates/host
# cmake ../../../src -DCMAKE_CXX_COMPILER=g++ -DCMAKE_SKIP_RPATH=TRUE
# make
echo "AI calculation..."
cd $HOME/AscendProjects/colorization/out
chmod +x main
./main $HOME/data

retry_count=0
for ((retry_count = 1; retry_count <= 3; retry_count++)); do
    echo sshpass -p ${OUT_PASSWORDD} scp -o StrictHostKeyChecking=no -r $HOME/AscendProjects/colorization/out/output ${OUT_USER}@${OUT_HOST}:${OUT_PATH}
    sshpass -p ${OUT_PASSWORDD} scp -o StrictHostKeyChecking=no -r $HOME/AscendProjects/colorization/out/output ${OUT_USER}@${OUT_HOST}:${OUT_PATH}
    if [ $? -eq 0 ]; then
        break
    fi
done

if [ $retry_count -le 3 ]; then
    echo "Return result to "${OUT_USER}@${OUT_HOST}:${OUT_PATH}/colorization
else
    echo "Return result failed."
fi

echo "Clean and reset Atlas environment..."
rm -rf $HOME/colorization.*
rm -rf $HOME/data/*
rm -rf $HOME/AscendProjects
