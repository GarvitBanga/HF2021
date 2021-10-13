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

class FixedNumberOfDigits {
	public:
	long long sum(int start, int step, long long num) {
		int tmp=start;
		//ll ans=1;
		ve a;
		while(tmp){
			a.pb(tmp%10);
			tmp=tmp/10;
		}
		if(a.size()>num){
			int x=0;
			ll ans=0;
			repi(i,a.size()-1,0){
				
				ans=ans*10+a[i];
				x++;
				if(x>=num)return ans;

			}
		}
		else{
			ll diff=pow(10,a.size());
			if(diff==1)diff=10;
			ll count=0;
			ll sz=0;
			if(a.size()==0)sz=1;
			else sz=a.size();
			while(num>=count+sz){
				//cout<<"num"<<num<<endl;
				//cout<<"start"<<start<<endl;
				if(start>=diff){count++; if(num>count+sz)num-=(count+sz); else break;  diff*=10;}
				else {if(num>count+sz)num-=(count+sz); else break;}
				start+=step;
			}
		
		ve b;
		//cout<<start<<endl;
		while(start){
			b.pb(start%10);
			start=start/10;

		}
		int x=0;

		ll ans=0;
			repi(i,b.size()-1,0){
				
				ans=ans*10+b[i];
				x++;
				if(x==num)return ans;
			}

		return ans;
	}

		//return 1;

		
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
			int start                 = 47;
			int step                  = 10;
			long long numberOfDigits  = 7;
			long long expected__      = 7;

			std::clock_t start__      = std::clock();
			long long received__      = FixedNumberOfDigits().sum(start, step, numberOfDigits);
			return verify_case(casenum__, expected__, received__, clock()-start__);
		}
		case 1: {
			int start                 = 98;
			int step                  = 1;
			long long numberOfDigits  = 10;
			long long expected__      = 101;

			std::clock_t start__      = std::clock();
			long long received__      = FixedNumberOfDigits().sum(start, step, numberOfDigits);
			return verify_case(casenum__, expected__, received__, clock()-start__);
		}
		case 2: {
			int start                 = 0;
			int step                  = 1;
			long long numberOfDigits  = 7;
			long long expected__      = 6;

			std::clock_t start__      = std::clock();
			long long received__      = FixedNumberOfDigits().sum(start, step, numberOfDigits);
			return verify_case(casenum__, expected__, received__, clock()-start__);
		}
		case 3: {
			int start                 = 123456789;
			int step                  = 10;
			long long numberOfDigits  = 5;
			long long expected__      = 12345;

			std::clock_t start__      = std::clock();
			long long received__      = FixedNumberOfDigits().sum(start, step, numberOfDigits);
			return verify_case(casenum__, expected__, received__, clock()-start__);
		}
		case 4: {
			int start                 = 123456789;
			int step                  = 10;
			long long numberOfDigits  = 17;
			long long expected__      = 12345679;

			std::clock_t start__      = std::clock();
			long long received__      = FixedNumberOfDigits().sum(start, step, numberOfDigits);
			return verify_case(casenum__, expected__, received__, clock()-start__);
		}

		// custom cases

/*      case 5: {
			int start                 = ;
			int step                  = ;
			long long numberOfDigits  = ;
			long long expected__      = ;

			std::clock_t start__      = std::clock();
			long long received__      = FixedNumberOfDigits().sum(start, step, numberOfDigits);
			return verify_case(casenum__, expected__, received__, clock()-start__);
		}*/
/*      case 6: {
			int start                 = ;
			int step                  = ;
			long long numberOfDigits  = ;
			long long expected__      = ;

			std::clock_t start__      = std::clock();
			long long received__      = FixedNumberOfDigits().sum(start, step, numberOfDigits);
			return verify_case(casenum__, expected__, received__, clock()-start__);
		}*/
/*      case 7: {
			int start                 = ;
			int step                  = ;
			long long numberOfDigits  = ;
			long long expected__      = ;

			std::clock_t start__      = std::clock();
			long long received__      = FixedNumberOfDigits().sum(start, step, numberOfDigits);
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
