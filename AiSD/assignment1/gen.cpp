#include<iostream>
#include<vector>
#include<string>
#include<map>
#include<unistd.h>

using namespace std;

#define PII pair<int,int>
#define st first 
#define nd second 

#define cerr if(0) cout 
#define _upgrade ios_base::sync_with_stdio(0), cin.tie(0), cout.tie(0)

const int MXN = 2000;

int draw( int a, int b ){ return a + random()%(b-a+1); }

int main( ){
    _upgrade;
    srand(time(NULL) + getpid());

    int n, m;
    n = MXN, m = MXN;
    // n = 5, m = 6;
    char letters[] = {'A', 'B', 'C', 'D', 'E', 'F'};

    cout<<n<<' '<<m<<'\n';
    for( int i=0; i<n; i++ ){
        for( int j=0; j<m; j++ ){
            int number = draw(1,6);
            cout<<letters[number - 1];
        }
        cout<<'\n';
    }
}