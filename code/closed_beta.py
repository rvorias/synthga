"""
Base python code: Genesis Loot - bkampsch
Optimization + batch boosting: Genesis Loot - rvorias/dham
"""

import ctypes
from ctypes import *
import time
import sys

import multiprocessing, time
from secrets import token_bytes
from sha3 import keccak_256

# PARAMETERS

difficulty = 8       # how many items of the same order you want
numworkers = 16      # number of threads to use
numiter = int(1e10)  # total amount of iterations (not counting batches)
reportat = int(1e4)  # opted for higher frequency of feedback
logpath = "./found.txt"
enable_progress_messages = True

# ADVANCED SETTINGS
"""
Batch size defines how many private+public keys are generated in one go.
One of the things that makes secp256k1 slow is the mod inversion operation.
Luckily, we are able to batch it! Increasing this gives diminishing returns.
Remember to keep things multiples of 8.
"""
batch_size = 32
"""
bmul_size defines the size of a precomputed table, which can range from
4 (original) to 24 bits. Larger values should be faster at the cost of higher
RAM. See https://github.com/llamasoft/secp256k1_fast_unsafe#variably-sized-precomputed-tables
for more information.
"""
bmul_size = 16

# .SO SETUP
hypersecp = CDLL("./bprivvy.so")
priv = ctypes.create_string_buffer(32*batch_size)
pub = ctypes.create_string_buffer(65*batch_size)

ctx = hypersecp.get_ctx()
bmul = hypersecp.get_bmul(ctx, bmul_size)
src = hypersecp.get_scr(ctx, batch_size)
       
item_types = ["WEAPON", "CHEST", "HEAD", "WAIST", "FOOT", "HAND", "NECK", "RING"]
item_types_b = [bytes(item_type, "utf-8") for item_type in item_types]

def check_addr(addr):
    suffix = None
    for item_type in item_types_b[:difficulty]:
        rand = int.from_bytes(keccak_256(item_type+addr).digest(), "big", signed=False)
        if rand % 21 > 14:
            if suffix is not None:
                suffix_new = rand % 16 + 1
                if suffix_new != suffix:
                    return False
            else:
                suffix = rand % 16 + 1
        else:
            return False
    return True

def worker():
    name = multiprocessing.current_process().name
    t_next = time.time()
    for i in range(numiter):
        if i % reportat == 0 and name == "000" and enable_progress_messages:
            print( "┍━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╾")
            print(f"│completed:     {i*numworkers*batch_size:,.0f}")
            print(f"│current speed: {reportat*numworkers*batch_size/(time.time()-t_next):.0f} its/s")
            print( "╰─────────────────────────────────")
            t_next = time.time()

        priv = token_bytes(32*batch_size)
        hypersecp.run_batch(pub, priv, ctx, bmul, src, batch_size)

        for j in range(batch_size):
            private_key = priv[32*j:32*(j+1)]
            public_key = pub[65*j:65*(j+1)][1:]
            addr = keccak_256(public_key).digest()[-20:]
            if(check_addr(addr)):
                info =\
                    f"""
                    worker:      {name}
                    difficulty : {difficulty}
                    private key: {private_key.hex()}
                    eth addr   : {addr.hex()}
                    """
                print(info)
                with open(logpath,"a") as f:
                    f.write(info)

def print_info():
    print( "┍━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┑")
    print( "│ Welcome, Searcher                              │") 
    print( "│ This vessel was made by @rvorias (dham)        │")
    print( "│                     and @bkampsch              │")
    print( "│ -------params--------------------------------- │")
    print(f"│ difficulty   {difficulty}                                 │")
    print(f"│ numworkers   {numworkers}                                │")
    print(f"│ batch_size   {batch_size:04d}                              │")
    print(f"│ bmul         {bmul_size:02d}                                │")
    print(f"│ reportat     {reportat:012d}                      │")
    print(f"│ numiter      {numiter:012d}                      │")
    print( "╰────────────────────────────────────────────────╯")

if __name__ == "__main__":
    if len(sys.argv) == 5:
        # python closed_beta.py NUMWORKERS NUMITER BATCH_SIZE BMUL_SIZE
        numworkers = int(sys.argv[1])
        numiter = int(sys.argv[2])
        batch_size = int(sys.argv[3])
        bmul_size = int(sys.argv[4])
        enable_progress_messages = False # you probably know what you are doing
    print_info()

    jobs = []
    beg = time.time()
    for i in range(numworkers):
        p = multiprocessing.Process(target=worker, name=str(i).zfill(3))
        jobs.append(p)
        p.start()
    for j in jobs:
        j.join()
    print(f"searched {numworkers*numiter*batch_size/(time.time()-beg)} wallets / second")
