// Michał Fica 
#include<iostream>
#include<vector>
#include<string>
#include<map>

using namespace std;

#define PII pair<int,int>
#define st first 
#define nd second 
#define cerr if(0) cout 
#define _upgrade ios_base::sync_with_stdio(0), cin.tie(0), cout.tie(0)

const int MXT = 5e5;
const int M = 999979;

int t;
int n, m;

map<PII,int> tunels;
vector<int> graph[2*MXT+5];
int dp[2*MXT+5];

int main()
{
    _upgrade;

    cin>>m>>n>>t;
    int inputOrder = 0;
    for( int i=0; i<t; i++ ){
        int a1, b1, a2, b2;
        cin>>a1>>b1>>a2>>b2;

        if(tunels.find({a1,b1})==tunels.end()) tunels[{a1,b1}] = ++inputOrder;
        if(tunels.find({a2,b2})==tunels.end()) tunels[{a2,b2}] = ++inputOrder;
        
        graph[tunels[{a2,b2}]].push_back(tunels[{a1,b1}]);
    }

    fill(dp,dp+t+1,0);
    dp[ tunels[{0,0}] ] = 1;

    for(auto v : tunels){
        for(auto u : graph[v.second]){
            dp[v.second]=(dp[v.second] + dp[u])%M;
        }
    }

    int result = 0;
    if (tunels.find({m,n})!=tunels.end()){
        result = dp[ tunels[{m,n}] ]%M;
    }

    cout<<result<<'\n';
}