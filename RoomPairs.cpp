#include <bits/stdc++.h>
using namespace std;
#define ll long long
#define pb push_back
#define mp make_pair
#define ve vector<long long>
#define mi map<int,int>
#define repi(i,a,b) for(ll i=a;i>=b;i--)
#define rep(i,a,b) for(long long i=a;i<b;i++)
#define all(a)   (a).begin(),(a).end()
#define hell 1000000007
#define tr(it,m) for(auto it=m.begin();it!=m.end();it++)
#define clr(x) memset(x,0,sizeof(x))

class RoomPairs {
	public:
	vector <string> construct(int R, int C, int N) {
		
	}
};
// BEGIN CUT HERE
#include <cstdio>
#include <ctime>
#include <iostream>
#include <string>
#include <vector>
namespace moj_harness {
	using std::string;
	using std::vector;
	int run_test_case(int);
	void run_test(int casenum = -1, bool quiet = false) {
		if (casenum != -1) {
			if (run_test_case(casenum) == -1 && !quiet) {
				std::cerr << "Illegal input! Test case " << casenum << " does not exist." << std::endl;
			}
			return;
		}
		
		int correct = 0, total = 0;
		for (int i=0;; ++i) {
			int x = run_test_case(i);
			if (x == -1) {
				if (i >= 100) break;
				continue;
			}
			correct += x;
			++total;
		}
		
		if (total == 0) {
			std::cerr << "No test cases run." << std::endl;
		} else if (correct < total) {
			std::cerr << "Some cases FAILED (passed " << correct << " of " << total << ")." << std::endl;
		} else {
			std::cerr << "All " << total << " tests passed!" << std::endl;
		}
	}
	
	template<typename T> std::ostream& operator<<(std::ostream &os, const vector<T> &v) { os << "{"; for (typename vector<T>::const_iterator vi=v.begin(); vi!=v.end(); ++vi) { if (vi != v.begin()) os << ","; os << " " << *vi; } os << " }"; return os; }
	template<> std::ostream& operator<<(std::ostream &os, const vector<string> &v) { os << "{"; for (vector<string>::const_iterator vi=v.begin(); vi!=v.end(); ++vi) { if (vi != v.begin()) os << ","; os << " \"" << *vi << "\""; } os << " }"; return os; }

	int verify_case(int casenum, const vector <string> &expected, const vector <string> &received, std::clock_t elapsed) { 
		std::cerr << "Example " << casenum << "... "; 
		
		string verdict;
		vector<string> info;
		char buf[100];
		
		if (elapsed > CLOCKS_PER_SEC / 200) {
			std::sprintf(buf, "time %.2fs", elapsed * (1.0/CLOCKS_PER_SEC));
			info.push_back(buf);
		}
		
		if (expected == received) {
			verdict = "PASSED";
		} else {
			verdict = "FAILED";
		}
		
		std::cerr << verdict;
		if (!info.empty()) {
			std::cerr << " (";
			for (size_t i=0; i<info.size(); ++i) {
				if (i > 0) std::cerr << ", ";
				std::cerr << info[i];
			}
			std::cerr << ")";
		}
		std::cerr << std::endl;
		
		if (verdict == "FAILED") {
			std::cerr << "    Expected: " << expected << std::endl; 
			std::cerr << "    Received: " << received << std::endl; 
		}
		
		return verdict == "PASSED";
	}

	int run_test_case(int casenum__) {
		switch (casenum__) {
		case 0: {
			int R                     = 2;
			int C                     = 4;
			int N                     = 1;
			string expected__[]       = {"+-+-+-+-+", "| |   | |", "+ + +-+ +", "|   |   |", "+-+-+-+-+" };

			std::clock_t start__      = std::clock();
			vector <string> received__ = RoomPairs().construct(R, C, N);
			return verify_case(casenum__, vector <string>(expected__, expected__ + (sizeof expected__ / sizeof expected__[0])), received__, clock()-start__);
		}
		case 1: {
			int R                     = 3;
			int C                     = 3;
			int N                     = 4;
			string expected__[]       = {"+-+-+-+", "| | | |", "+-+ +-+", "|     |", "+-+ +-+", "| | | |", "+-+-+-+" };

			std::clock_t start__      = std::clock();
			vector <string> received__ = RoomPairs().construct(R, C, N);
			return verify_case(casenum__, vector <string>(expected__, expected__ + (sizeof expected__ / sizeof expected__[0])), received__, clock()-start__);
		}
		case 2: {
			int R                     = 3;
			int C                     = 4;
			int N                     = 3;
			string expected__[]       = {"+-+-+-+-+", "|       |", "+ +-+-+ +", "| | | | |", "+ +-+-+ +", "|       |", "+-+-+-+-+" };

			std::clock_t start__      = std::clock();
			vector <string> received__ = RoomPairs().construct(R, C, N);
			return verify_case(casenum__, vector <string>(expected__, expected__ + (sizeof expected__ / sizeof expected__[0])), received__, clock()-start__);
		}
		case 3: {
			int R                     = 4;
			int C                     = 5;
			int N                     = 31;
			string expected__[]       = {"+-+-+-+-+-+", "| | | | | |", "+-+-+-+-+-+", "| | | | | |", "+-+-+-+-+-+", "| | | | | |", "+-+-+-+-+-+", "| | | | | |", "+-+-+-+-+-+" };

			std::clock_t start__      = std::clock();
			vector <string> received__ = RoomPairs().construct(R, C, N);
			return verify_case(casenum__, vector <string>(expected__, expected__ + (sizeof expected__ / sizeof expected__[0])), received__, clock()-start__);
		}

		// custom cases

/*      case 4: {
			int R                     = ;
			int C                     = ;
			int N                     = ;
			string expected__[]       = ;

			std::clock_t start__      = std::clock();
			vector <string> received__ = RoomPairs().construct(R, C, N);
			return verify_case(casenum__, vector <string>(expected__, expected__ + (sizeof expected__ / sizeof expected__[0])), received__, clock()-start__);
		}*/
/*      case 5: {
			int R                     = ;
			int C                     = ;
			int N                     = ;
			string expected__[]       = ;

			std::clock_t start__      = std::clock();
			vector <string> received__ = RoomPairs().construct(R, C, N);
			return verify_case(casenum__, vector <string>(expected__, expected__ + (sizeof expected__ / sizeof expected__[0])), received__, clock()-start__);
		}*/
/*      case 6: {
			int R                     = ;
			int C                     = ;
			int N                     = ;
			string expected__[]       = ;

			std::clock_t start__      = std::clock();
			vector <string> received__ = RoomPairs().construct(R, C, N);
			return verify_case(casenum__, vector <string>(expected__, expected__ + (sizeof expected__ / sizeof expected__[0])), received__, clock()-start__);
		}*/
		default:
			return -1;
		}
	}
}

#include <cstdlib>
int main(int argc, char *argv[]) {
	if (argc == 1) {
		moj_harness::run_test();
	} else {
		for (int i=1; i<argc; ++i)
			moj_harness::run_test(std::atoi(argv[i]));
	}
}
// END CUT HERE
