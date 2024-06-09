/*
    Debugging macro for C++ by Starcea
    colormap is optimized with vscode theme "Gruvbox Dark Hard"
*/

#define debug(...)                                       \
    {                                                    \
        _print_header(__FILE__, __LINE__, __FUNCTION__); \
        std::string _s = #__VA_ARGS__;                   \
        std::replace(_s.begin(), _s.end(), ',', ' ');    \
        std::stringstream _ss(_s);                       \
        std::istream_iterator<std::string> _it(_ss);     \
        _print_value(_it, __VA_ARGS__);                  \
    }

const std::string ESC = "\033[";
const std::string RESET = ESC + "0m";
const std::string BOLD = ESC + "1m";
const std::string RED = ESC + "31m";
const std::string CYAN = ESC + "36m";
const std::string YELLOW = ESC + "33m";
const std::string BR_MAGENTA = ESC + "95m";
const std::string BR_GREEN = ESC + "92m";
const std::string BLUE = ESC + "34m";
const std::string GRAY = ESC + "90m";

const std::string HEADER = BOLD + YELLOW;
const std::string ERROR = BOLD + RED;

const std::string DEFAULT = BR_MAGENTA;
const std::string STRING = BR_GREEN;
const std::string BOOL = BR_GREEN;
const std::string CONTAINER = BLUE;
const std::string SEP = GRAY;
const std::string OPERATOR = BOLD + CYAN;
const std::string INDENT = "  ";

namespace filter {
template <class T>
struct is_iterable : std::false_type {};

template <class T, size_t SZ>
struct is_iterable<std::array<T, SZ>> : std::true_type {};

template <class T>
struct is_iterable<std::set<T>> : std::true_type {};

template <class T>
struct is_iterable<std::unordered_set<T>> : std::true_type {};

template <class T>
struct is_iterable<std::multiset<T>> : std::true_type {};

template <class T>
struct is_iterable<std::deque<T>> : std::true_type {};

template <class T>
struct is_iterable<std::vector<T>> : std::true_type {};

template <class T>
struct is_iterable<std::list<T>> : std::true_type {};

template <class T>
struct is_map : std::false_type {};

template <class K, class V>
struct is_map<std::map<K, V>> : std::true_type {};

template <class K, class V>
struct is_map<std::unordered_map<K, V>> : std::true_type {};

template <class T>
struct is_supports_top : std::false_type {};

template <class T>
struct is_supports_top<std::stack<T>> : std::true_type {};

template <class T>
struct is_supports_top<std::priority_queue<T>> : std::true_type {};

template <class T>
struct is_supports_top<std::priority_queue<T, std::vector<T>, std::greater<T>>>
    : std::true_type {};

template <class T>
struct is_implemented {
    static constexpr bool value =
        is_iterable<T>::value || is_map<T>::value || is_supports_top<T>::value;
};
}  // namespace filter

template <class T>
std::string _to_str(T x);

std::string to_string(std::string s) { return STRING + '"' + s + '"' + RESET; }

std::string to_string(char c) { return STRING + "'" + c + "'" + RESET; }

std::string to_string(char *s) { return to_string((std::string)s); }

std::string to_string(const char *s) { return to_string((std::string)s); }

std::string to_string(bool b) { return (b ? "true" : "false"); }

template <class T>
typename std::enable_if<filter::is_iterable<T>::value, std::string>::type
to_string(T v) {
    bool first = true;
    std::string res = CONTAINER + "{ ";
    for (auto &x : v) {
        res += (first ? "" : SEP + ", " + CONTAINER) + _to_str(x);
        first = false;
    }
    res += CONTAINER + " }" + RESET;
    return res;
}

template <class T>
typename std::enable_if<filter::is_map<T>::value, std::string>::type to_string(
    T m
) {
    bool first = true;
    std::string res = CONTAINER + "{ ";
    for (auto &[k, v] : m) {
        res += (first ? "" : SEP + ", " + CONTAINER) + _to_str(k) + SEP + ": " +
               CONTAINER + _to_str(v);
        first = false;
    }
    res += CONTAINER + " }" + RESET;
    return res;
}

template <class T>
typename std::enable_if<filter::is_supports_top<T>::value, std::string>::type
to_string(T v) {
    T t = v;
    bool first = true;
    std::string res = CONTAINER + "{ ";
    while (!t.empty()) {
        res += (first ? "" : SEP + ", " + CONTAINER) + _to_str(t.top());
        t.pop();
        first = false;
    }
    res += CONTAINER + " }" + RESET;
    return res;
}

template <class T>
std::string to_string(std::queue<T> q) {
    queue<T> t = q;
    bool first = true;
    std::string res = CONTAINER + "{ ";
    while (!t.empty()) {
        res += (first ? "" : SEP + ", " + CONTAINER) + _to_str(t.front());
        t.pop();
        first = false;
    }
    res += CONTAINER + " }" + RESET;
    return res;
}

template <class T, class F>
std::string to_string(std::pair<T, F> p) {
    auto [first, second] = p;
    return CONTAINER + "{ " + _to_str(first) + SEP + ", " + CONTAINER +
           _to_str(second) + CONTAINER + " }" + RESET;
}

template <class... T>
std::string to_string(std::tuple<T...> t) {
    bool first = true;
    std::string res = CONTAINER + "{ ";
    apply(
        [&](auto &&...args) {
            ((res += (first ? "" : SEP + ", " + CONTAINER) + _to_str(args),
              first = false),
             ...);
        },
        t
    );
    res += CONTAINER + " }" + RESET;
    return res;
}

template <class T>
typename std::enable_if<!filter::is_implemented<T>::value, std::string>::type
to_string(T x) {
    return ERROR + "Not implemented" + RESET;
}

template <class T>
std::string _to_str(T x) {
    return DEFAULT + to_string(x) + RESET;
}

void _print_header(std::string file, int line, std::string func) {
    std::cerr << HEADER << "[" << file << ":" << line
              << (func == "main" ? "" : " - " + func) << "]" << RESET << "\n";
}

void _print_value(std::istream_iterator<std::string> it) {}

template <class T, class... Tail>
void _print_value(std::istream_iterator<std::string> it, T a, Tail... v) {
    cerr << INDENT << *it << OPERATOR << " = " << RESET << _to_str(a) << "\n";
    _print_value(++it, v...);
}
