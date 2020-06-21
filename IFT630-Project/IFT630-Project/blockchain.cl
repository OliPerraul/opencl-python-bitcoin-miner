#include "sha256/sha256.cl"

#define PrevHashSize 32U
#define MerkleHashSize 32U
#define BlockSize 80U
#define HashSize 32U
#define NonceSize 4U
#define __memcpy(dst,src,num) { for (int i = 0; i < num; i++) { (dst)[i] = (char)((src)[i]); } }

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

// size = sizeof(start) < sizeof(sequence); 
bool prefix_0(char* sequence, unsigned int difficulty)
{
    for(unsigned int i = 0; i < difficulty; i++)
    {   
        if(sequence[i] != 0)
            return false;
    }

    return true;
}

void hash_sha256(char *content, char* hash, unsigned int nonce){

	SHA256_CTX ctx;
	sha256_init(&ctx);
	sha256_update(&ctx, nonce, (BYTE*)content, BlockSize);
    sha256_final(&ctx, (BYTE*)hash);
}

__kernel void compute_blockchain(
    unsigned int globalSize,
    unsigned int numNonceTrials,
    unsigned int version,
    // Timestamp greater than median timestamp over of last 11 blocks
    unsigned int timestamp,
    unsigned int difficulty,
    __constant const char* prevHash,
    __constant const char* merkleHash,
    __global bool* found,
    __global char* outputNonceBuffer,
    __global char* outputBuffer,
    __global char* blockOutputBuffer)
{
    
    // nonce = threadId * numNonceTrials
    unsigned int start = numNonceTrials * get_global_id(0);
    unsigned int end = start + numNonceTrials;

    char block[BlockSize];
    char hash[HashSize];

    // res = input->version + self->prevHash + self->merkleHash + self->time + self->difficulty + self->nonce
    __memcpy(&(block[0]), &version, 4);
    __memcpy(&(block[4]), &prevHash, PrevHashSize);
    __memcpy(&(block[PrevHashSize + 4]), &merkleHash, MerkleHashSize);
    //__memcpy(&(block[PrevHashSize + MerkleHashSize + 4]), &timestamp, 4);
    Copy_unsigned_int(block, timestamp, 4);
    __memcpy(&(block[PrevHashSize + MerkleHashSize + 2*4]), &difficulty, 4);

    unsigned int nonce;
    for (nonce = start; nonce < end && nonce < globalSize; nonce++) 
    {
        if(*found)
            break;

        __memcpy(&(block[PrevHashSize + MerkleHashSize + 3*4]), &nonce, 4);
        hash_sha256(block, hash, nonce);

        if(prefix_0(hash, difficulty))
        {
            __memcpy(outputBuffer, hash, HashSize);
            __memcpy(blockOutputBuffer, block, BlockSize);
            Copy_unsigned_int2(outputNonceBuffer, nonce, NonceSize);
            *found = true;
            return;
        }
    }

    return;    
}