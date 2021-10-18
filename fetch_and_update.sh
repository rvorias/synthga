#/bin/sh

FROM=code
TO=secp256k1_fast_unsafe

git clone https://github.com/llamasoft/secp256k1_fast_unsafe.git
cp $FROM/tests.c $TO/src/tests.c
cp $FROM/closed_beta.py $TO/closed_beta.py
cp $FROM/bprivvy.c $TO/bprivvy.c
cp $FROM/find_params.sh $TO/find_params.sh

