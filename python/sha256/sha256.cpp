// sha256.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <iostream>
#include "sha256.h"

extern "C" {

	__declspec(dllexport)
	void hash_sha256(char *content, char* hash, unsigned int size) {

		//std::cout << content << std::endl;
	
		SHA256_CTX ctx;

		sha256_init(&ctx);
		sha256_update(&ctx, (BYTE*)hash, size);
		sha256_final(&ctx, (BYTE*)hash);
	}

} // extern "C"


