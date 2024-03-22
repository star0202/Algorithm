#include <bits/stdc++.h>
using namespace std;

#ifdef STARCEA
#include "debug.h"
#else
#define debug(...) \
    { __VA_ARGS__; }
#endif

using i64 = int64_t;

void func() {
    int var_in_func = 1234;
    debug(var_in_func);
}

int main() {
    int int1 = INT_MAX;
    i64 int2 = __INT64_MAX__;
    string str = "hello";
    vector<int> vec1 = {1, 2, 3};
    vector<string> vec2 = {"hello", "world"};
    pair<int, string> pair1 = {5, "hello"};
    tuple<int, string, vector<int>> tuple1 = {5, "hello", {1, 2, 3}};
    array<int, 3> arr1 = {1, 2, 3};
    set<int> set1 = {1, 2, 3};
    stack<int> unknown1({1, 2, 3});

    debug(int1, int2, str, vec1, vec2, pair1, tuple1, arr1, set1, unknown1);

    func();
}
