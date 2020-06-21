#include <stdio.h>
#include <stdint.h>

#include "sha256/sha256.cuh"

#define PrevHashSize 32U
#define MerkleHashSize 32U
#define BlockSize 80U


typedef uint32_t uint;

__device__
// size = sizeof(start) < sizeof(sequence); 
bool prefix_0(char* sequence, uint difficulty)
{
    for(uint i = 0; i < difficulty; i++)
    {
        if(sequence[i] != '\0')
            return false;
    }

    return true;
}

__device__
void hash_sha256(char *content, char *hash){

	SHA256_CTX ctx;
	sha256_init(&ctx);
	sha256_update(&ctx, reinterpret_cast<BYTE*>(content), BlockSize);
    sha256_final(&ctx, reinterpret_cast<BYTE*>(hash));
    
    sha256_init(&ctx);
	sha256_update(&ctx, reinterpret_cast<BYTE*>(hash), BlockSize);
    sha256_final(&ctx, reinterpret_cast<BYTE*>(hash));
    
    sha256_init(&ctx);
	sha256_update(&ctx, reinterpret_cast<BYTE*>(hash), BlockSize);
	sha256_final(&ctx, reinterpret_cast<BYTE*>(hash));
}

__global__ void compute_blockchain(
    uint numNonceTrials,
    uint version,
    // Timestamp greater than median timestamp over of last 11 blocks
    uint timestamp,
    uint difficulty,
    const char* prevHash,
    const char* merkleHash,
    bool* found,
    char* outputBuffer,
    char* blockOutputBuffer)
{
    const uint threadsPerBlock = blockDim.x * blockDim.y * blockDim.z;
    const uint threadNumInBlock = threadIdx.x + threadIdx.y *(blockDim.x) + threadIdx.z * (blockDim.x*blockDim.y);
    const uint blockNumInGrid = blockIdx.x  + blockIdx.y * gridDim.x + blockIdx.z * ( gridDim.x * gridDim.y);
    
    // nonce = threadId * numNonceTrials
    uint nonce = (blockNumInGrid * threadsPerBlock + threadNumInBlock) * numNonceTrials;
    //

    char block_content[BlockSize];
    char check_buffer[BlockSize];

    // res = input->version + self->prevHash + self->merkleHash + self->time + self->difficulty + self->nonce
    memcpy(&(block_content[0]), &version, 4);
    memcpy(&(block_content[4]), &prevHash, PrevHashSize);
    memcpy(&(block_content[PrevHashSize + 4]), &merkleHash, MerkleHashSize);
    memcpy(&(block_content[PrevHashSize + MerkleHashSize + 4]), &timestamp, 4);
    memcpy(&(block_content[PrevHashSize + MerkleHashSize + 2*4]), &difficulty, 4);

    uint i = 0;
    do
    {
        if(i >= numNonceTrials)
        {
            break;
        }

        memcpy(&(block_content[PrevHashSize + MerkleHashSize + 3*4]), &nonce, 4);
        hash_sha256(block_content, check_buffer);
        
        if(prefix_0(check_buffer, difficulty))
        {
            (*found) = true;
            memcpy(&(outputBuffer[0]), &(check_buffer[0]), BlockSize);
            memcpy(&(blockOutputBuffer[0]), &(block_content[0]), BlockSize);
        }

        i++;
        nonce++;

    } while(!(*found));
}
