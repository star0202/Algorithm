#ifdef LOCAL
#include "debug.h"
#else
#include <bits/stdc++.h>
#define debug(...)
#endif

using namespace std;

// macros
#define all(x) x.begin(), x.end()
#define rep(i, s, e) for (int i = s; i < e; i++)
#define tc(t) \
    int t;    \
    cin >> t; \
    while (t--)
int sz(auto x) { return (int)x.size(); }
void ms(auto &x, auto v) { memset(x, v, sizeof(x)); }

// shortcuts
#define fi first
#define se second
#define pb push_back
#define sp " "
#define nl "\n"

// types
#define int int64_t
using str = string;
using vi = vector<int>;
using pii = pair<int, int>;
template <class T>
using pqg = priority_queue<T, vector<T>, greater<T>>;

// constants
const int INF = INT64_MAX;
int dx[] = {0, 0, 1, -1}, dy[] = {1, -1, 0, 0};

// configs
const int PRECISION = 0;

signed main() {
    cin.tie(0)->sync_with_stdio(0);
    cout << fixed << setprecision(PRECISION);
}
