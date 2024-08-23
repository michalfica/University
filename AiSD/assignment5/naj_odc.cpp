#include <bits/stdc++.h>
using namespace std;

#define MX_N 200000
typedef long long LL;
const LL INF=1e18;

struct point{
    int x, y, nr;
    void read( ){ cin>>x>>y; }
    point make_point ( int _x, int _y )
    {
        point p;
        p.x=_x;
        p.y=_y;
        return p;
    }
    point operator -( point a ){ return make_point( x-a.x, y-a.y ); }
    point operator +( point a ){ return make_point( x+a.x, y+a.y ); }
};

LL leng( point a, point b )
{
    LL ans;
    a=a-b;
    // ans=sqrt( (LL)a.x*a.x + (LL)a.y*a.y );
    ans=(LL)a.x*a.x + (LL)a.y*a.y ;
    return ans;
}

bool comp1( point a, point b )
{
    if( a.x==b.x ) return a.y>b.y;
    return a.x<b.x;
}

bool comp2( point a, point b )
{
    if( a.y==b.y ) return a.x<b.x;
    return a.y>b.y;
}

int n;
point tab1[MX_N+5];//points sorted by x
vector<point> vec;//points in range 2d
LL result;

LL smallest_dist( int l, int r )
{
    if( r-l+1==1 ) return INF;
    if( r-l+1==2 ) return leng( tab1[l], tab1[r] );

    int mid=(l+r)/2;
    LL d, d1, d2;

    d1=smallest_dist( l, mid );
    d2=smallest_dist( mid+1, r );
    d=min( d1, d2 );

    for( int i=l; i<=r; i++ )
    {
        if( abs(tab1[i].x-tab1[mid].x)<=d ) vec.push_back( tab1[i] );
    }

    sort( vec.begin(), vec.end(), comp2 );

    int size1=vec.size();
    for( int i=0; i<size1; i++ )
    {
        for( int j=1; j<min(7,size1-i); j++ )
        {
            LL dist=leng( vec[i], vec[j+i] );
            if( dist<d ) d=dist;
        }
    }
    vec.clear();
    return d;
}

int A[MX_N+5];
int main( )
{
    ios_base::sync_with_stdio(0);
    cin.tie(0);

    cin>>n;
    for( int i=0; i<n; i++ ) cin>>A[i];

    int sum = 0;
    for( int i=0; i<n; i++ ){
        sum += A[i];

        tab1[i].x = i;
        tab1[i].y = sum;
    }


    sort( tab1, tab1+n, comp1 );

    result=smallest_dist( 0, n-1 );
    cout<<result<<'\n';
    // cout<<fixed<<setprecision(5)<<result<<"\n";
}
