#include <bits/stdc++.h>

using namespace std;

#define debug(...)                                                  \
    cerr << "\033[1;31m"                                            \
         << "[" << __FILE__ << ":" << __LINE__ << " - " << __func__ \
         << "]\033[0m "                                             \
         << "\033[36m" << #__VA_ARGS__ << "\033[0m: \033[33m";      \
    _debug(__VA_ARGS__);

string to_string(string s) { return '"' + s + '"'; }

string to_string(const char *s) { return to_string((string)s); }

string to_string(bool b) { return (b ? "true" : "false"); }

template <class T, class V>
string to_string(pair<T, V> p) {
    return "(" + to_string(p.first) + ", " + to_string(p.second) + ")";
}

template <class T>
string to_string(T v) {
    bool first = true;
    string res = "{";
    for (const auto &x : v) {
        if (!first) {
            res += ", ";
        }
        first = false;
        res += to_string(x);
    }
    res += "}";
    return res;
}

void _debug() { cerr << "\n\033[0m"; }

template <class Head, class... Tail>
void _debug(Head H, Tail... T) {
    cerr << to_string(H);
    _debug(T...);
}
