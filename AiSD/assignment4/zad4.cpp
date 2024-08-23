#include<bits/stdc++.h>
using namespace std;

#define PII pair<int,int>
#define st first
#define ns second
#define LL long long

#define cerr if(0) cout

const int MXN=5e5;

int t;

int n, m;
vector<int> tree[MXN+5][2];

map< vector<int>,int > all; int cnt=1;
int hasz[MXN+5][3], paretnt[MXN+5][3];

set<int> hs_subtree;
void dfs( int nr, int v, int fa=0 )
{
  vector<int> hs;
  hs.clear(), hs.push_back(1);
  paretnt[v][nr]=fa;

  for( auto &u : tree[v][nr] )
  {
    if( u==fa ) continue;

    dfs(nr,u,v);
    hs.push_back( hasz[u][nr] );
  }
  sort( hs.begin(), hs.end() );

  if( all.find(hs)==all.end() ) all[hs]=++cnt;
  hasz[v][nr]=all[hs];

  if( nr==1 ) hs_subtree.insert(hasz[v][nr]);
}

set<int> hs_leavs[2];
void count_hasz( int nr, int v )
{
  vector<int> hs;
  hs.clear();

  while( v!=1 )
  {
    hs.push_back(hasz[v][nr]);
    v=paretnt[v][nr];
  }

  if( all.find(hs)==all.end() ) all[hs]=++cnt;
  hs_leavs[nr].insert( all[hs] );
}

void print( set<int> set_z_haszami ){
    for( auto x: set_z_haszami ) cerr<<x<<' ';
    cerr<<'\n'; 
}

int main( )
{
  ios_base::sync_with_stdio(0);
  cin.tie(0);

  cin>>t;

  while( t-- ){

    cin>>n;   
    for( int i=1; i<n; i++ )
    {
        int a, b; cin>>a>>b;
        tree[a][0].push_back(b);
        tree[b][0].push_back(a);
    }
    for( int i=1; i<n; i++ )
    {
        int a, b; cin>>a>>b;
        tree[a][1].push_back(b);
        tree[b][1].push_back(a);
    }

    cerr<<"wczytałem oba drzewa\n";

    dfs(0,1);
    cerr<<"dfs1\n";
    dfs(1,1);
    cerr<<"dfs2\n";
    

    for( int i=2; i<=n; i++ ){
        if( tree[i][0].size()==1 ) {
            count_hasz(0,i);
            // cout<<i<<"liść w 0 drzewie\n";
        }
    }
    
    for( int i=2; i<=n; i++ ){
        if( tree[i][1].size()==1 ) {
            // cout<<i<<" liść w 1 drzewie\n";
            count_hasz(1,i);
        }
    }

    
    cerr<<"hasze1 \n";
    print(hs_leavs[0]);
    cerr<<"hasze2 \n";
    print(hs_leavs[1]);
    
    if( hs_leavs[0]==hs_leavs[1] ){
        cout<<"TAK\n";
    }
    else{
        cout<<"NIE\n";
    }


    for(int i=0; i<n; i++){
        tree[i][0].clear();
        tree[i][1].clear();

        paretnt[i][0]=paretnt[i][1] = 0;
        hasz[i][0]=hasz[i][1]=0;
    }

    hs_leavs[0].clear();
    hs_leavs[1].clear();
  }


}