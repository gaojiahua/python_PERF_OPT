// dll2ctypes.cpp : 定义 DLL 应用程序的导出函数。
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