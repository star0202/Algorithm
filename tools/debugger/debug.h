/*
    Debugging macro for C++ by Starcea
    colormap is optimized with vscode theme "Gruvbox Dark Hard"
*/

#ifndef STARCEA
#include <bits/stdc++.h>
using namespace std;
#endif

#define debug(...)                                       \
    {                                                    \
        _print_header(__FILE__, __LINE__, __FUNCTION__); \
        string _s = #__VA_ARGS__;                        \
        replace(_s.begin(), _s.end(), ',', ' ');         \
        stringstream _ss(_s);                            \
        istream_iterator<string> _it(_ss);               \
        _print_value(_it, __VA_ARGS__);                  \
    }

#define ESC (string) "\033["
#define RESET ESC + "0m"
#define BOLD ESC + "1m"
#define RED ESC + "31m"
#define CYAN ESC + "36m"
#define YELLOW ESC + "33m"
#define BR_MAGENTA ESC + "95m"
#define BR_GREEN ESC + "92m"
#define BLUE ESC + "34m"
#define GRAY ESC + "90m"

#define HEADER BOLD + YELLOW
#define ERROR BOLD + RED

#define DEFAULT BR_MAGENTA
#define STRING BR_GREEN
#define BOOL BR_GREEN
#define CONTAINER BLUE
#define SEP GRAY
#define OPERATOR BOLD + CYAN
#define INDENT "  "

namespace filter {

template <class T>
struct is_iterable : false_type {};

template <class T, size_t SZ>
struct is_iterable<array<T, SZ>> : true_type {};

template <class T>
struct is_iterable<set<T>> : true_type {};

template <class T>
struct is_iterable<unordered_set<T>> : true_type {};

template <class T>
struct is_iterable<multiset<T>> : true_type {};

template <class T>
struct is_iterable<deque<T>> : true_type {};

template <class T>
struct is_iterable<vector<T>> : true_type {};

template <class T>
struct is_iterable<list<T>> : true_type {};

template <class T>
struct is_map : false_type {};

template <class K, class V>
struct is_map<map<K, V>> : true_type {};

template <class K, class V>
struct is_map<unordered_map<K, V>> : true_type {};

template <class T>
struct is_supports_top : false_type {};

template <class T>
struct is_supports_top<stack<T>> : true_type {};

template <class T>
struct is_supports_top<priority_queue<T>> : true_type {};

template <class T>
struct is_implemented {
    static constexpr bool value =
        is_iterable<T>::value || is_map<T>::value || is_supports_top<T>::value;
};
}  // namespace filter

template <class T>
string _to_str(T x);

string to_string(string s) { return STRING + '"' + s + '"' + RESET; }

string to_string(char c) { return STRING + "'" + c + "'" + RESET; }

string to_string(char *s) { return to_string((string)s); }

string to_string(const char *s) { return to_string((string)s); }

string to_string(bool b) { return (b ? "true" : "false"); }

template <class T>
typename enable_if<filter::is_iterable<T>::value, string>::type to_string(T v) {
    bool first = true;
    string res = CONTAINER + "{ ";
    for (auto &x : v) {
        res += (first ? "" : SEP + ", " + CONTAINER) + _to_str(x);
        first = false;
    }
    res += CONTAINER + " }" + RESET;
    return res;
}

template <class T>
typename enable_if<filter::is_map<T>::value, string>::type to_string(T m) {
    bool first = true;
    string res = CONTAINER + "{ ";
    for (auto &[k, v] : m) {
        res += (first ? "" : SEP + ", " + CONTAINER) + _to_str(k) + SEP + ": " +
               CONTAINER + _to_str(v);
        first = false;
    }
    res += CONTAINER + " }" + RESET;
    return res;
}

template <class T>
typename enable_if<filter::is_supports_top<T>::value, string>::type to_string(
    T v) {
    T t = v;
    bool first = true;
    string res = CONTAINER + "{ ";
    while (!t.empty()) {
        res += (first ? "" : SEP + ", " + CONTAINER) + _to_str(t.top());
        t.pop();
        first = false;
    }
    res += CONTAINER + " }" + RESET;
    return res;
}

template <class T>
string to_string(queue<T> q) {
    queue<T> t = q;
    bool first = true;
    string res = CONTAINER + "{ ";
    while (!t.empty()) {
        res += (first ? "" : SEP + ", " + CONTAINER) + _to_str(t.front());
        t.pop();
        first = false;
    }
    res += CONTAINER + " }" + RESET;
    return res;
}

template <class T, class F>
string to_string(pair<T, F> p) {
    auto [first, second] = p;
    return CONTAINER + "[ " + _to_str(first) + SEP + ", " + CONTAINER +
           _to_str(second) + CONTAINER + " ]" + RESET;
}

template <class... T>
string to_string(tuple<T...> t) {
    bool first = true;
    string res = CONTAINER + "{ ";
    apply(
        [&](auto &&...args) {
            ((res += (first ? "" : SEP + ", " + CONTAINER) + _to_str(args),
              first = false),
             ...);
        },
        t);
    res += CONTAINER + " }" + RESET;
    return res;
}

template <class T>
typename enable_if<!filter::is_implemented<T>::value, string>::type to_string(
    T) {
    return ERROR + "Not implemented" + RESET;
}

template <class T>
string _to_str(T x) {
    return DEFAULT + to_string(x) + RESET;
}

void _print_header(string file, int line, string func) {
    cerr << HEADER << "[" << file << ":" << line
         << (func == "main" ? "" : " - " + func) << "]" << RESET << "\n";
}

void _print_value(istream_iterator<string> it) {}

template <class T, class... Tail>
void _print_value(istream_iterator<string> it, T a, Tail... v) {
    cerr << INDENT << *it << OPERATOR << " = " << RESET << _to_str(a) << "\n";
    _print_value(++it, v...);
}
