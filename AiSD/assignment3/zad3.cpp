
// NIE DZIAŁA DP!!


#include<bits/stdc++.h>

using namespace std;

const int MXN = 1e6;

const vector<int> path4 = {1, 8, 3, 4, 11, 6, 7, 2, 9, 10, 5, 12};
const vector< vector<int> > paths ={ {7, 2, 9, 4, 3, 8, 1, 6, 11, 16, 21, 14, 19, 18, 13, 20, 15, 10, 5, 12, 17},                                      //path7                      
                                    {11, 6, 1, 8, 3, 4, 9, 2, 7, 14, 21, 22, 17, 24, 19, 18, 23, 16, 15, 10, 5, 12, 13, 20},                           //path8
                                    {17, 22, 27, 20, 25, 24, 19, 26, 21, 14, 7, 2, 9, 4, 3, 8, 1, 6, 11, 16, 15, 10, 5, 12, 13, 18, 23},               //path9
                                    {21, 14, 7, 2, 9, 4, 3, 8, 1, 6, 11, 16, 15, 10, 5, 12, 17, 22, 29, 24, 25, 30, 23, 28, 27, 20, 13, 18, 19, 26} }; //path10
// const vector<int> path8 = {11, 6, 1, 8, 3, 4, 9, 2, 7, 14, 21, 22, 17, 24, 19, 18, 23, 16, 15, 10, 5, 12, 13, 20};
// const vector<int> path9 = {17, 22, 27, 20, 25, 24, 19, 26, 21, 14, 7, 2, 9, 4, 3, 8, 1, 6, 11, 16, 15, 10, 5, 12, 13, 18, 23};
// const vector<int> path10 = {21, 14, 7, 2, 9, 4, 3, 8, 1, 6, 11, 16, 15, 10, 5, 12, 17, 22, 29, 24, 25, 30, 23, 28, 27, 20, 13, 18, 19, 26};


int n;
string board[MXN+5];

vector<int> create_path( int k ){
    vector<int> path = paths[ (k-7)%4 ];
    while( path.size()<3*k ){
        int number = path.size();
        for(auto p: path4 ){
            path.push_back( p+number );
        }
    }
    return path;
}

void print( vector<int> v ){
    for( auto p: v ) 
        cout<<p<<' ';
    cout<<'\n';
} 

bool blocked[3*MXN +5];
int get_field_number( int i, int j ){
    int number = 3*i;
    if( j==0 ) return number +1;
    if( j==1 ) return number +2;
    return number +3;
}

pair<int,int> get_position( int nr ){
    int i = nr/3, j = (nr-1)%3;
    return {i,j};
}

void mark_blocked_fields( ){
    for( int i=0; i<n; i++ ){
        for( int j=0; j<board[i].size(); j++ ){
            if( board[i][j]=='X' ) blocked[get_field_number(i,j)] = true;
        }
    }
}

int dp[3*MXN+5][2];
int solve( vector<int> path ){
    // TO TEST ...

    dp[ path[0] ][0] = 0;
    if( !blocked[path[0]] ) dp[ path[0] ][1] = 1;
    for( int i=1; i<path.size(); i++ ){
        dp[ path[i] ][0] = max( dp[ path[i-1] ][0], dp[ path[i-1] ][1] );
        if( blocked[path[i]] ) dp[ path[i] ][1] = 0;
        else{
            dp[ path[i] ][1] = dp[ path[i-1] ][0] +1;
        }
    }
    return max( dp[path[path.size()-1]][0], dp[path[path.size()-1]][1] );
}

char solution[MXN+5][3];
void find_solution( vector<int> path, int result ){

    for( int i=0; i<n; i++ )
        for( int j=0; j<3; j++ )
            solution[i][j] = board[i][j];
    

    int beg = path[0];
    reverse(path.begin(),path.end());

    int i = 0;
    int actual_field = path[i];
    while( actual_field!=beg ){
        if( dp[actual_field][1]==result ){
            pair<int,int> pos = get_position(actual_field);
            solution[pos.first][pos.second] = 'S';
            result--;
        }
        actual_field = path[++i];
    }
}

int main( ){
    cin>>n;
    for( int i=0; i<n; i++ ) cin>>board[i];

    vector<int> path = create_path(n);
    mark_blocked_fields();

    print(path);

    int result = solve(path);
    find_solution(path,result);


    cout<<result<<'\n';
    for( int i=0; i<n; i++ ){
        for( int j=0; j<3; j++ )
            cout<<solution[i][j];
        cout<<'\n';
    }
}