#include <bits/stdc++.h>
using namespace std;

#define FOR(x,y) for (int x = 0; x < y; ++x)
#define For(x,y,z) for (int x = y; x <= z; ++x)
#define ms(x,y) memset (x, y, sizeof(x))
typedef long long ll;
typedef unsigned long long ull;
typedef pair<int,int> pii;
typedef pair<ll,int> pli;
typedef vector<int> vi;
//const double EPS = 1e-8;
//const int MAX_N = 1e5 + 5;
//const ll MOD = 1e9 + 7;
//const int INF = 0x3f3f3f3f;

inline int ran (int n) // create a random num [0,n)
{
    return rand() % n;
}

int main ()
{
    srand(time(NULL));
    int n;
    cin >> n;
    FILE * f = fopen("data.in", "w");
    int m = 10 * n;
    fprintf (f, "%d\n", n);
    FOR(i,n) fprintf(f, "%d\n", ran(m));
	fclose(f);
    return 0;
}
