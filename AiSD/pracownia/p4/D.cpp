#include<bits/stdc++.h>
using namespace std;

#define PII pair<int,int>
#define st first
#define ns second

#define cerr if(1) cout
const int MXN =5e5;

vector<int> tree[MXN+5][2];
map< vector<int>,int > hash_map;
int subtree_hash[MXN+5][2], cnt;

void count_hash( int nr, int v, int fa=0 ){
    vector<int> hs;
    hs.clear();

    for( auto u : tree[v][nr] ){
        if( u==fa ) continue;
        count_hash(nr,u,v);
        hs.push_back( subtree_hash[u][nr] );
    }
    sort( hs.begin(), hs.end() );
    if( hash_map.find(hs)==hash_map.end() )hash_map[hs]=++cnt;
    subtree_hash[v][nr] = hash_map[hs];
}

int t, n;
void init( ){
    cin>>n; 
    for( int i=1; i<n; i++ ){
        int a, b; cin>>a>>b;
        tree[a][0].push_back(b);
        tree[b][0].push_back(a);
    }
    for( int i=1; i<n; i++ ){
        int a, b; cin>>a>>b;
        tree[a][1].push_back(b);
        tree[b][1].push_back(a);
    }
}

void print_tree( int nr ){
    cerr<<"tree "<<nr<<":\n";
    for( int i=1; i<=n; i++ ){
        cerr<<"hash["<<i<<"] = "<<subtree_hash[i][nr]<<"\n";
    }
}

int dist[MXN+5];
void dfs( int nr, int v, int fa=0 ){
    for( auto u: tree[v][nr] ){
        if( u==fa ) continue;
        dist[u] = dist[v] +1;
        dfs(nr,u,v);
    }
}

vector<int> find_longest_path( int nr ){

    int a=1, b=1;
    fill( dist+1,dist+n+5, 0);
    dfs(nr,1);
    for( int i=1; i<=n; i++ ){
        if( dist[i]>dist[a] ) a=i;
    }

    fill( dist+1,dist+n+5, 0);
    dfs(nr,a);
    for( int i=1; i<=n; i++ ){
        if( dist[i]>dist[b] ) b=i;
    }

    int d = dist[b];
    vector<int> path;
    path.clear();
    int vertex = b;
    path.push_back(vertex);
    for( int i=0; i<d; i++ ){

        for( auto u : tree[vertex][nr] ){
            if( dist[u]+1 == dist[vertex] ){
                vertex = u;
                break;
            }
        }
        path.push_back(vertex);
    }
    return path;
}
void print_path( vector<int> p, int nr ){
    cerr<<"tree: "<<nr<<'\n';
    for( auto v : p ) cerr<<v<<' ';
    cerr<<'\n';
}

void clean(){
    for( int i=0; i<=n+2; i++ ){
        tree[i][0].clear();
        tree[i][1].clear();
        subtree_hash[i][0] = 0;
        subtree_hash[i][1] = 0;
    }
    cnt = 0;
    hash_map.clear();
}

int main( ){

    ios_base::sync_with_stdio(0);
    cin.tie(0);

    cin>>t;
    while( t-- ){
        init();

        vector<int> mx_path1 = find_longest_path(0);
        vector<int> mx_path2 = find_longest_path(1);

        if( (mx_path1.size()!=mx_path2.size()) || (mx_path1.size()%2!=mx_path2.size()%2) ){
            cout<<"NIE\n";
        }
        else{
            int root1, root2;
            if( mx_path1.size()%2==0 ){
                root1=root2=n+1;
                int a, b;
                a = mx_path1[ mx_path1.size()/2 ], b = mx_path1[ (mx_path1.size()/2) -1 ];

                tree[a][0].push_back(root1), tree[root1][0].push_back(a);
                tree[b][0].push_back(root1), tree[root1][0].push_back(b);
                tree[a][0].erase( find(tree[a][0].begin(),tree[a][0].end(),b) );
                tree[b][0].erase( find(tree[b][0].begin(),tree[b][0].end(),a) );

                a = mx_path2[ mx_path2.size()/2 ], b = mx_path2[ (mx_path2.size()/2) -1 ];
                
                tree[a][1].push_back(root2), tree[root2][1].push_back(a);
                tree[b][1].push_back(root2), tree[root2][1].push_back(b);
                tree[a][1].erase( find(tree[a][1].begin(),tree[a][1].end(),b) );
                tree[b][1].erase( find(tree[b][1].begin(),tree[b][1].end(),a) );
            }
            else{
                root1 = mx_path1[ mx_path1.size()/2 ], root2 = mx_path2[ mx_path2.size()/2 ];
            }
            count_hash(0,root1);    
            count_hash(1,root2);

            if( subtree_hash[root1][0]==subtree_hash[root2][1] ) cout<<"TAK\n";
            else cout<<"NIE\n";
        }

        clean();
    }
}