// Michał Fica 

#include<iostream>
#include<vector>
#include<string>

using namespace std;

#define PII pair<int,int>
#define st first 
#define nd second 

#define cerr if(0) cout 
#define _upgrade ios_base::sync_with_stdio(0), cin.tie(0), cout.tie(0)

const int MXN = 2000;

vector<PII> moves[] = { {}, {{0,-1},{1,0}}, {{0,-1},{-1,0}}, {{-1,0},{0,1}}, {{1,0},{0,1}}, {{0,-1},{-1,0},{0,1},{1,0}}}; 
vector<PII> getVertexMoves( char c ){
    if( c=='A' ) return moves[0];
    if( c=='B' ) return moves[1];
    if( c=='C' ) return moves[2];
    if( c=='D' ) return moves[3];
    if( c=='E' ) return moves[4];
    return moves[5];
}

bool checkEdge( char c, PII move ){
    for( auto m : getVertexMoves(c) )
        if( m==move ) return true;
    return false;
}

bool checkMove( pair<char,PII> p1, PII p2Wyniki.2022 ){                     // sprawdza czy możliwe jest przejście z pola p1 do pola p2 
    return checkEdge(p1.st, {p2.st-p1.nd.st,p2.nd-p1.nd.nd}); 
}

int n, m;
char board[MXN+1][MXN+1];

bool inBoard( PII p ){
    return 0<=p.st and p.st<n and 0<=p.nd and p.nd<m;
}

bool visited[MXN+1][MXN+1];
void dfs( PII position ){

    visited[position.st][position.nd] = true;
    char c = board[position.st][position.nd];

    for( auto mv : getVertexMoves(c) ){
        PII newpos = {position.st+mv.st,position.nd+mv.nd};
        if( !inBoard(newpos) ) continue;
        if( visited[newpos.st][newpos.nd] ) continue;

        char newc  =  board[newpos.st][newpos.nd];
        if( checkMove({newc,newpos},position) ){
            dfs(newpos);
        }
    }
}

int solve(){
    int cnt = 0;
    for( int i=0; i<n; i++ ){
        for( int j=0; j<m; j++ ){
            if( !visited[i][j] and board[i][j]!='A' ){
                cnt++;
                dfs({i,j});
            }
        }
    }
    return cnt;
}

void init(){
    cin>>n>>m;
    for( int i=0; i<n; i++ )
        for( int j=0; j<m; j++ )
            cin>>board[i][j];
}

int main( ){
     _upgrade;

    init();
    int result = 0; //solve();

    for( int i=0; i<n; i++ ){
    for( int j=0; j<m; j++ ){
        if( !visited[i][j] and board[i][j]!='A' ){
            result++;
            dfs({i,j});
        }
    }
}
    cout<<result<<'\n';
}