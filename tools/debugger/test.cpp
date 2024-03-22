#include <bits/stdc++.h>
using namespace std;

#ifdef STARCEA
#include "debug.h"
#else
#define debug(...) \
    { __VA_ARGS__; }
#endif

using i64 = int64_t;

struct Unknown {};

void func() {
    int var_in_func = 1234;

    debug(var_in_func);
}

int main() {
    bool bool_1 = true;

    int int_1 = INT_MAX;
    i64 int_2 = __INT64_MAX__;
    float float_1 = 3.14;
    double double_1 = 3.14159;

    string string_1 = "hello";
    char char_1 = 'a';
    char* char_ptr_1 = "hello";
    const char* const_char_ptr_1 = "hello";

    array<int, 3> array_1 = {1, 2, 3};
    set<int> set_1 = {1, 2, 3};
    unordered_set<int> unordered_set_1 = {1, 2, 3};
    deque<int> deque_1 = {1, 2, 3};
    vector<int> vec_1 = {1, 2, 3};
    vector<vector<int>> vec_2 = {{1, 2, 3}, {4, 5, 6}};
    list<int> list_1 = {1, 2, 3};

    map<int, string> map_1 = {{1, "one"}, {2, "two"}};
    unordered_map<int, string> unordered_map_1 = {{1, "one"}, {2, "two"}};

    stack<int> stack_1;
    stack_1.push(1);
    stack_1.push(2);
    stack_1.push(3);

    queue<int> queue_1;
    queue_1.push(1);
    queue_1.push(2);
    queue_1.push(3);

    priority_queue<int> priority_queue_1;
    priority_queue_1.push(1);
    priority_queue_1.push(2);
    priority_queue_1.push(3);

    pair<int, string> pair_1 = {1, "one"};
    tuple<int, string, float> tuple_1 = {1, "one", 3.14};

    Unknown unknown_1;

    debug(bool_1);
    debug(int_1, int_2, float_1, double_1);
    debug(string_1, char_1, char_ptr_1, const_char_ptr_1);
    debug(array_1, set_1, unordered_set_1, deque_1, vec_1, vec_2, list_1);
    debug(map_1, unordered_map_1);
    debug(stack_1, queue_1, priority_queue_1);
    debug(pair_1, tuple_1);
    debug(unknown_1);

    func();
}
