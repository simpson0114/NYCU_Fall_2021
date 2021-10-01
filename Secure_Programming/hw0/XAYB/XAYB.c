#include <stdio.h>
#include <stdint.h>


int main() {
	int64_t v4; // [rsp+0h] [rbp-30h]
	int64_t v5; // [rsp+8h] [rbp-28h]
  	int64_t v6; // [rsp+10h] [rbp-20h]
  	int64_t v7; // [rsp+18h] [rbp-18h]
  	int64_t v8; // [rsp+20h] [rbp-10h]
  	int v9; // [rsp+28h] [rbp-8h]
  	int16_t v10; // [rsp+2Ch] [rbp-4h]
  	char v11; // [rsp+2Eh] [rbp-2h]

  	v4 = -7078913653395439948LL;
  	v5 = -6358330961596013139LL;
  	v6 = -5075129350575962195LL;
  	v7 = -5937273151547921013LL;
  	v8 = -3763139359601218172LL;
  	v9 = -1213160794;
	v10 = -28779;
  	v11 = 0;
	char *a1 = (char *)&v4;
	for (int l = 0; l < 8; ++l ) {
        	a1[l] ^= 0xF2u;
		printf("%c", a1[l]);
	}
	char *a2 = (char *)&v5;
	for (int l = 0; l < 8; ++l ) {
                a2[l] ^= 0xF2u;
		printf("%c", a2[l]);
	}
	char *a3 = (char *)&v6;
        for (int l = 0; l < 8; ++l ) {
                a3[l] ^= 0xF2u;
		printf("%c", a3[l]);
	}
	char *a4 = (char *)&v7;
        for (int l = 0; l < 8; ++l ) {
                a4[l] ^= 0xF2u;
		printf("%c", a4[l]);
	}
	char *a5 = (char *)&v8;
        for (int l = 0; l < 8; ++l ) {
                a5[l] ^= 0xF2u;
		printf("%c", a5[l]);
	}
	char *a6 = (char *)&v9;
        for (int l = 0; l < 4; ++l ) {
                a6[l] ^= 0xF2u;
		printf("%c", a6[l]);
	}
	char *a7 = (char *)&v10;
        for (int l = 0; l < 2; ++l ) {
                a7[l] ^= 0xF2u;
		printf("%c", a7[l]);
	}
}
