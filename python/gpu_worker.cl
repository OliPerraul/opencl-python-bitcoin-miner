
#include "sha256/sha256.cl"

#define PrevHashSize 32U
#define MerkleHashSize 32U
#define BlockSize 80U
#define HashSize 32U
#define NonceSize 16U

#define __memcpy(dst,src,num) { for (int i = 0; i < num; i++) { (dst)[i] = (char)((src)[i]); } }
// size = sizeof(start) < sizeof(sequence); 
bool prefix_0(char* sequence, int difficulty)
{
    for(int i = 0; i < difficulty; i++)
    {   
        if(sequence[i] != '\0')
            return false;
    }

    return true;
}

void hash_sha256(char *content, char* hash){
	SHA256_CTX ctx;
    
    sha256_init(&ctx);
	sha256_update(&ctx, (BYTE*)hash, HashSize);
    sha256_final(&ctx, (BYTE*)hash);
}
void Copy_unsigned_int(char* buffer, unsigned int timestamp, int offset){
    buffer[offset + 3] = (timestamp >> 24) & 0xFF;
    buffer[offset + 2] = (timestamp >> 16) & 0xFF;
    buffer[offset + 1] = (timestamp >> 8) & 0xFF;
    buffer[offset + 0] = timestamp & 0xFF;
}
void Copy_unsigned_int2(__global char* buffer, unsigned int timestamp, int offset){
    buffer[offset + 0] = (timestamp >> 24) & 0xFF;
    buffer[offset + 1] = (timestamp >> 16) & 0xFF;
    buffer[offset + 2] = (timestamp >> 8) & 0xFF;
    buffer[offset + 3] = timestamp & 0xFF;
}

__kernel void compute_blockchain(
    unsigned int globalSize,
    unsigned int numNonceTrials,
    unsigned int version,
    // Timestamp greater than median timestamp over of last 11 blocks
    unsigned int timestamp,
    int difficulty,
    __global char* prevHash,
    __global char* merkleHash,
    __global int* found,
    __global char* outputNonceBuffer,
    __global char* outputBuffer,
    __global char* blockBuffer)
{
    unsigned int start = numNonceTrials * get_global_id(0);
    unsigned int end = start + numNonceTrials;
    volatile __global int* foundPtr = found;
    char block[BlockSize];
    char hash[HashSize];
    
    __memcpy(&(block[0]), &version, 4);
    __memcpy(&(block[4]), prevHash, PrevHashSize);
    __memcpy(&(block[PrevHashSize + 4]), merkleHash, MerkleHashSize);
    Copy_unsigned_int(block, timestamp, PrevHashSize + MerkleHashSize + 4);
    __memcpy(&(block[PrevHashSize + MerkleHashSize + 2*4]), &difficulty, 4);
    
    for (unsigned int nonce = start; nonce < end && nonce < globalSize; nonce++) 
    {
        Copy_unsigned_int(block, nonce, PrevHashSize + MerkleHashSize + 3*4);
        hash_sha256(block, hash);

        if(prefix_0(hash, difficulty))
        {
            __memcpy(outputBuffer, hash, HashSize);
            __memcpy(blockBuffer, block, BlockSize);
            Copy_unsigned_int2(outputNonceBuffer, nonce, 0);

            atomic_inc(foundPtr);
            return;
         }
         if(*found != 0){
             return;
         }

    }
    return;    
}
