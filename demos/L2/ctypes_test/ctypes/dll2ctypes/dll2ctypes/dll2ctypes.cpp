// dll2ctypes.cpp : ���� DLL Ӧ�ó���ĵ���������
//

#include "stdafx.h"
#include <math.h>
   
int WINAPI c_Add(int a, int b)
{
	return a+b;
}



int WINAPI c_check_prime(int a)
{
	int c;
	for ( c = 2 ; c <= sqrt((float)a) ; c++ ) {
		if ( a%c == 0 )
			return 0;
	}

	return 1;

}