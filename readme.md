# Synthetic GA search tool

This code is based on @bkampsch's synthga tool. I've added changes such that it now performs
at 3-10x the amount of its/sec.

# Quickstart

Check if gcc is installed:

```bash
$ gcc -v
```

Pull batch-wise keypair generation:
```bash
$ ./fetch_and_update.sh
```

Then:
```bash
$ cd secp256k1_fast_unsafe
$ ./autogen.sh
$ ./configure
$ make
$ ./tests # optional
$ sudo make install # optional
```

Now the secret sauce (ignore warnings):
```bash
$ gcc -Wall -Wno-unused-function -O2 -march=native -I src/ -I ./ -shared bprivvy.c -lgmp -fPIC -o bprivvy.so  
```

Set up python(3):
```bash
[optional] $ pipenv install
[optional] $ pipenv shell
$ pip install pysha3
```

Configure parameters in `closed_beta.py`

Let's go:
```bash
$ python closed_beta.py
```

# Tune parameters

reconfigure and run `$ bash fetch_and_update.sh`

# Troubleshooting

autogen is complaining:
`sudo apt-get install libtool libtool-bin`

make is complaining about future time:
`$ touch */*`

make is complaining about gmpl:
`$sudo apt-get install -y libgmp-dev`


# Install gcc

From https://linuxize.com/post/how-to-install-gcc-compiler-on-ubuntu-18-04/

```bash
$ sudo apt update
$ sudo apt install build-essential
$ sudo apt-get install manpages-dev
$ gcc --version
```
