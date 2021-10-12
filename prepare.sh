pip install --target ./package pytz
pip install --target ./package python-decouple

cd package

# Download Pandas
curl -O https://files.pythonhosted.org/packages/21/b6/3a61175ae2b1cac872ecfa271f7887d4f33d0f3cdfee8cf3dcfdfb8c3a62/pandas-1.1.3-cp39-cp39-manylinux1_x86_64.whl

# Download Numpy
curl -O https://files.pythonhosted.org/packages/7a/4c/dd00ce768b0f0f7de5c486cbd9f5b922bc3af2f3a5da30121d7f7dc03130/numpy-1.21.2-cp39-cp39-manylinux_2_12_x86_64.manylinux2010_x86_64.whl

# unZip Pandas
unzip pandas-1.1.3-cp39-cp39-manylinux1_x86_64.whl

# unZip Numpy
unzip numpy-1.21.2-cp39-cp39-manylinux_2_12_x86_64.manylinux2010_x86_64.whl

rm -r *.whl *.dist-info __pycache__

zip -r9 ${OLDPWD}/scriptLambda.zip .

cd ${OLDPWD}

rm -rf package __pycache__
