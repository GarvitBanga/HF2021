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

class GridSpiral {
	public:
	long long findCell(int d) {
		if(d%2==0)return -1;
		if(d<=7)return 0;
		if(d==9)return 1;
		if(d==11)return 2;
		if(d==13)return 4;
		if(d==15)return 6;
		if(d==17)return 9;
		//rep(i,0,1000)
		ll ans=0;
		if((d-11)%8==0){
			ans=1;
			ll x=5,y=(d-11)/8;
			rep(i,0,y)
				ans+=(x+4*(i));
				ans*=2;
			
		}
		else if((d-13)%8==0){
			ans=2;
			ll x=6,y=(d-13)/8;
			rep(i,0,y)
				ans+=(x+4*(i));
				ans*=2;
		}
		else if((d-15)%8==0){
			ans=3;
			ll x=7,y=(d-15)/8;
			rep(i,0,y)
				ans+=(x+4*(i));
				ans*=2;
		}
		else if((d-17)%8==0){
			ans=4;
			ll x=8,y=(d-17)/8;
			rep(i,0,y)
				ans+=(x+4*(i));
				ans*=2;
			
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
	
	int verify_case(int casenum, const long long &expected, const long long &received, std::clock_t elapsed) { 
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
			int D                     = 5;
			long long expected__      = 0;

			std::clock_t start__      = std::clock();
			long long received__      = GridSpiral().findCell(D);
			return verify_case(casenum__, expected__, received__, clock()-start__);
		}
		case 1: {
			int D                     = 11;
			long long expected__      = 2;

			std::clock_t start__      = std::clock();
			long long received__      = GridSpiral().findCell(D);
			return verify_case(casenum__, expected__, received__, clock()-start__);
		}
		case 2: {
			int D                     = 47;
			long long expected__      = 110;

			std::clock_t start__      = std::clock();
			long long received__      = GridSpiral().findCell(D);
			return verify_case(casenum__, expected__, received__, clock()-start__);
		}
		case 3: {
			int D                     = 100;
			long long expected__      = -1;

			std::clock_t start__      = std::clock();
			long long received__      = GridSpiral().findCell(D);
			return verify_case(casenum__, expected__, received__, clock()-start__);
		}

		// custom cases

/*      case 4: {
			int D                     = ;
			long long expected__      = ;

			std::clock_t start__      = std::clock();
			long long received__      = GridSpiral().findCell(D);
			return verify_case(casenum__, expected__, received__, clock()-start__);
		}*/
/*      case 5: {
			int D                     = ;
			long long expected__      = ;

			std::clock_t start__      = std::clock();
			long long received__      = GridSpiral().findCell(D);
			return verify_case(casenum__, expected__, received__, clock()-start__);
		}*/
/*      case 6: {
			int D                     = ;
			long long expected__      = ;

			std::clock_t start__      = std::clock();
			long long received__      = GridSpiral().findCell(D);
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
