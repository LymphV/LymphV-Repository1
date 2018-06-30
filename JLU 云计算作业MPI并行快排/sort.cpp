#include "mpi.h"
#include <ctime>
#include <iostream>
#include <stack>
#include <cstring>
#include <cmath>
#include <algorithm>
#include <Windows.h>
//#define DEBUG cout << rank << "of" << size << ' '
#define DEBUG /##/
#define FOR(x,y) for (int x = 0; x < y; ++x)
#define DEL(x) delete [] x; x = NULL

typedef long long ll;
using namespace std;
const int N = 10;

inline double log2(double x)
{
	return log(x) / log(2);
}

int main(int argc, char* argv[])
{
	int p = 0;
	int rank, size;
	MPI_Init(0, 0);
	MPI_Comm_rank(MPI_COMM_WORLD, &rank);
	MPI_Comm_size(MPI_COMM_WORLD, &size);

	int * arr = NULL;
	int offset = 0, length = 0, count = 0, level = (int)ceil(log2(rank + 1));
	ll startT = 0, endT = 0;
	int * res = NULL, * offsets = NULL, * counts = NULL;

	MPI_Status st;
	
	if (!rank)
	{
		FILE * f = fopen("data.in", "r");
		int x;
		fscanf (f, "%d", &x);
		count = length = x;
		arr = new int[x];
		FOR(i, x) fscanf(f, "%d", &arr[i]);
		fclose(f);

		res = new int[x];
		offsets = new int[size];
		counts = new int[size];
		memset(res, 0, x);
		memset(offsets, 0, size);
		memset(counts, 0, size);
		
		int * temp = new int[x];
		FOR(i, x) temp[i] = arr[i];

		startT = GetTickCount();
		sort(temp, temp + x);
		endT = GetTickCount();

		f = fopen("std.out", "w");
		fprintf(f, "%d\n", length);
		FOR(i, length) fprintf(f, "%d\n", temp[i]);
		fclose(f);
		DEL(temp);

		cout << "串行算法库函数sort：" << endl;
		cout << "开始时间： " << startT << "  结束时间： " << endT << " 消耗时间： " << (endT - startT) << " ms" << endl;

		startT = GetTickCount();
	}

	if (rank)
	{
		int last = rank - (1 << (level - 1));
		DEBUG << "last:" << last << endl;
		MPI_Recv(&length, 1, MPI_INT, last, 1, MPI_COMM_WORLD, &st);
		DEBUG << "last??????? : " << last << " l:" << length << endl;
		if (length)
		{
			arr = new int[length];
			memset(arr, 0, length);

			DEBUG << "last##### : " << last << " l:" << length << endl;
			MPI_Recv(&offset, 1, MPI_INT, last, 2, MPI_COMM_WORLD, &st);
			DEBUG << "last@@@@! : " << last << " l:" << length << " off:" << offset << endl;
			MPI_Recv(arr, length, MPI_INT, last, 3, MPI_COMM_WORLD, &st);
			DEBUG << "last2 : " << last << " l:" << length << endl;
		}
		else 
		{
			arr = new int;
			*arr = 0;
			for (int l = 0;; ++level)
			{
				int next = rank + (1 << level);
				if (next >= size) break;
				DEBUG << "next : " << next << "$$$$$" << endl;
				MPI_Send(&l, 1, MPI_INT, next, 1, MPI_COMM_WORLD);
			}
		}
	}
	if (!length)
	{
		int next = rank + (1 << level);
		if (next < size) MPI_Send(&length, 1, MPI_INT, next, 1, MPI_COMM_WORLD);
	}
	else for (;; ++level)
	{
		int next = rank + (1 << level);
		DEBUG << "next : " << next << " l:" << length << endl;
		if (next >= size)
		{
			sort(arr, arr + length);
			break;
		}
		if (length < N)
		{
			sort(arr, arr + length);
			
			for (int l = 0;; ++level)
			{
				next = rank + (1 << level);
				if (next >= size) break;
				DEBUG << "next : " << next << "$$$$$" << endl;
				MPI_Send(&l, 1, MPI_INT, next, 1, MPI_COMM_WORLD);
			}
			break;  
		}
		int * i = rank ? arr + 1 : arr, * j = arr + length - 1;
		int key = *i;
		while (i < j) 
		{
			while (i < j && key <= *j) --j;
			*i = *j;
			while (i < j && key >= *i) ++i;
			*j = *i;
		}
		*i = key;

		int * nleft = i, * nright = arr + length;
		int nlength = nright - nleft, noffset = offset + nleft - arr;
		length = i - arr;

		MPI_Send(&nlength, 1, MPI_INT, next, 1, MPI_COMM_WORLD);
		if (nlength)
		{
			MPI_Send(&noffset, 1, MPI_INT, next, 2, MPI_COMM_WORLD);
			MPI_Send(nleft, nlength, MPI_INT, next, 3, MPI_COMM_WORLD);
		}
		DEBUG << " l:" << length << " nl:" << nlength << endl;
	}

	DEBUG << "end sort------------------------------------------" << endl;

	MPI_Gather(&length, 1, MPI_INT, counts, 1, MPI_INT, 0, MPI_COMM_WORLD);
	MPI_Gather(&offset, 1, MPI_INT, offsets, 1, MPI_INT, 0, MPI_COMM_WORLD);
	MPI_Gatherv(arr, length, MPI_INT, res, counts, offsets, MPI_INT, 0, MPI_COMM_WORLD);

	DEBUG << "end gather=======================================" << endl;

	endT = GetTickCount();
	ll maxEndT = 0;
	MPI_Reduce(&endT, &maxEndT, 1, MPI_INT, MPI_MAX, 0, MPI_COMM_WORLD);


	if (!rank)
	{
		endT = maxEndT;
		length = count;
		cout << "并行算法：" << endl;
		cout << "开始时间： " << startT << "  结束时间： " << endT << " 消耗时间： " << (endT - startT) << " ms" << endl;

		FILE * f = fopen("data.out", "w");
		fprintf(f, "%d\n", length);
		FOR(i, length) fprintf (f, "%d\n", res[i]);
		fclose(f);
	}
	DEL(arr);
	DEL(offsets);
	DEL(counts);
	DEL(res);
	MPI_Finalize();
	return 0;
}
