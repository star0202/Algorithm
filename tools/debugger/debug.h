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
#define COMMA GRAY
#define OPERATOR BOLD + CYAN
#define INDENT "  "

template <class T>
string _to_str(T x);

string to_string(string s) { return STRING + '"' + s + '"' + RESET; }

string to_string(const char *s) { return to_string((string)s); }

string to_string(bool b) { return (b ? "true" : "false"); }

template <class T>
struct is_iterable : false_type {};

template <class T, size_t SZ>
struct is_iterable<array<T, SZ>> : true_type {};

template <class T>
struct is_iterable<set<T>> : true_type {};

template <class T>
struct is_iterable<deque<T>> : true_type {};

template <class T>
struct is_iterable<vector<T>> : true_type {};

template <class T>
typename enable_if<is_iterable<T>::value, string>::type to_string(T v) {
    bool first = true;
    string res = CONTAINER + "{ ";
    for (auto &x : v) {
        res += (first ? "" : COMMA + ", " + CONTAINER) + _to_str(x);
        first = false;
    }
    res += CONTAINER + " }" + RESET;
    return res;
}

template <class T, class V>
string to_string(pair<T, V> p) {
    auto [first, second] = p;
    return CONTAINER + "[" + _to_str(first) + COMMA + ", " + CONTAINER +
           _to_str(second) + CONTAINER + "]" + RESET;
}

template <class... T>
string to_string(tuple<T...> t) {
    bool first = true;
    string res = CONTAINER + "{ ";
    apply(
        [&](auto &&...args) {
            ((res += (first ? "" : COMMA + ", " + CONTAINER) + _to_str(args),
              first = false),
             ...);
        },
        t);
    res += CONTAINER + " }" + RESET;
    return res;
}

template <class T>
typename enable_if<!is_iterable<T>::value, string>::type to_string(T) {
    return ERROR + "to_string not implemented" + RESET;
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

template <class T, class... V>
void _print_value(istream_iterator<string> it, T a, V... v) {
    cerr << INDENT << *it << OPERATOR << " = " << RESET << _to_str(a) << "\n";
    _print_value(++it, v...);
}
