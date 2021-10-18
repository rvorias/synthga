/**********************************************************************
 * Copyright (c) 2016 Llamasoft                                       *
 * Distributed under the MIT software license, see the accompanying   *
 * file COPYING or http://www.opensource.org/licenses/mit-license.php.*
 **********************************************************************/

// After building secp256k1_fast_unsafe, compile benchmarks with:
//   gcc -Wall -Wno-unused-function -O2 --std=c99 -march=native -I src/ -I ./ bench_privkey.c timer.c -lgmp -o bench_privkey


#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "timer.h"

#define HAVE_CONFIG_H
#include "libsecp256k1-config.h"
#include "secp256k1.c"
#include "ecmult_big_impl.h"
#include "secp256k1_batch_impl.h"

secp256k1_context* get_ctx(){
    return secp256k1_context_create(SECP256K1_CONTEXT_VERIFY | SECP256K1_CONTEXT_SIGN);
}

secp256k1_ecmult_big_context* get_bmul(secp256k1_context* ctx, unsigned int bmul_size){
    return secp256k1_ecmult_big_create(ctx, bmul_size);
}

secp256k1_scratch* get_scr(secp256k1_context* ctx, unsigned int batch_size){
    return secp256k1_scratch_create(ctx, batch_size);
}

void run_batch(unsigned char *pubkeys, unsigned char *privkeys, secp256k1_context* ctx, secp256k1_ecmult_big_context* bmul, secp256k1_scratch* scr, unsigned int batch_size) {
    // Wrapped in if to prevent "ignoring return value" warning
    if ( secp256k1_ec_pubkey_create_serialized_batch(ctx, bmul, scr, pubkeys, privkeys, batch_size, 0) );
}

int main(int argc, char **argv) {
    return 0;
}
