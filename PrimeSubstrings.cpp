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

class PrimeSubstrings {
	public:
	string construct(int n, int l) {
		string ans="";
			rep(i,0,n){
				if(i%4==0){
					ans+='3';}
				else if(i%4==1){
					if((i-1)%8)ans+='1';
					else ans+='5';
				}

				else if(i%4==2)ans+='3';
				else ans+='7';
				}
				return ans;
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
	
	int verify_case(int casenum, const string &expected, const string &received, std::clock_t elapsed) { 
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
			std::cerr << "    Expected: \"" << expected << "\"" << std::endl; 
			std::cerr << "    Received: \"" << received << "\"" << std::endl; 
		}
		
		return verdict == "PASSED";
	}

	int run_test_case(int casenum__) {
		switch (casenum__) {
		case 0: {
			int N                     = 4;
			int L                     = 2;
			string expected__         = "5317";

			std::clock_t start__      = std::clock();
			string received__         = PrimeSubstrings().construct(N, L);
			return verify_case(casenum__, expected__, received__, clock()-start__);
		}
		case 1: {
			int N                     = 7;
			int L                     = 7;
			string expected__         = "1301779";

			std::clock_t start__      = std::clock();
			string received__         = PrimeSubstrings().construct(N, L);
			return verify_case(casenum__, expected__, received__, clock()-start__);
		}
		case 2: {
			int N                     = 5;
			int L                     = 4;
			string expected__         = "13079";

			std::clock_t start__      = std::clock();
			string received__         = PrimeSubstrings().construct(N, L);
			return verify_case(casenum__, expected__, received__, clock()-start__);
		}

		// custom cases

/*      case 3: {
			int N                     = ;
			int L                     = ;
			string expected__         = ;

			std::clock_t start__      = std::clock();
			string received__         = PrimeSubstrings().construct(N, L);
			return verify_case(casenum__, expected__, received__, clock()-start__);
		}*/
/*      case 4: {
			int N                     = ;
			int L                     = ;
			string expected__         = ;

			std::clock_t start__      = std::clock();
			string received__         = PrimeSubstrings().construct(N, L);
			return verify_case(casenum__, expected__, received__, clock()-start__);
		}*/
/*      case 5: {
			int N                     = ;
			int L                     = ;
			string expected__         = ;

			std::clock_t start__      = std::clock();
			string received__         = PrimeSubstrings().construct(N, L);
			return verify_case(casenum__, expected__, received__, clock()-start__);
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
