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
    int int_1 = INT_MAX;
    i64 int_2 = __INT64_MAX__;
    string string_1 = "hello";
    char char_1 = 'a';
    vector<int> vec_1 = {1, 2, 3};
    vector<vector<int>> vec_2 = {{1, 2, 3}, {4, 5, 6}};
    pair<int, string> pair_1 = {5, "hello"};
    tuple<int, string, vector<int>> tuple_1 = {5, "hello", {1, 2, 3}};
    array<int, 3> array_1 = {1, 2, 3};
    set<int> set_1 = {1, 2, 3};
    stack<int> unknown_1({1, 2, 3});

    debug(int_1, int_2, string_1, char_1, vec_1, vec_2, pair_1, tuple_1,
          array_1, set_1, unknown_1);

    func();
}
