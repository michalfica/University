#include <bits/stdc++.h>
using namespace std;

#define LL long long 
#define DEBUG false 
#define cerr if(DEBUG) cout

const int MXN = 1e6;
const LL INF=1e18;

struct point{
    int x, y, nr;
    void read() {cin>>x>>y;}

    point (){
        x = 0, y = 0;
    };

    point make_point( int _x, int _y ){
        point p;
        p.x = _x, p.y = _y;
        return p;
    }
    point operator +( point a ) { return make_point( x+ a.x, y+ a.y ); }
    point operator -( point a ) { return make_point( x -a.x, y -a.y ); }
};

LL leng( point a, point b )
{
    LL ans;
    a=a-b;
    ans=(LL)a.x*a.x + (LL)a.y*a.y;
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
point tab[MXN+5];//points sorted by x
vector<point> vec;//points in range 2d

pair<LL,pair<point,point>> nearest_points( int l, int r ){
    if( l==r )   return { INF, { tab[l], tab[l] } };
    if( r-l==1 ) return { leng(tab[l],tab[r]), { tab[l], tab[r] } };

    int mid = (l+r)/2;
    pair<LL,pair<point,point>> p1 = nearest_points(l, mid);
    pair<LL,pair<point,point>> p2 = nearest_points(mid+1, r);

    LL d1 = p1.first, d2 = p2.first;
    LL d = min(d1,d2);
    pair<point,point> pnts;

    if( d1==d ){
        pnts = p1.second;
    }
    if( d2==d ){
        pnts = p2.second;
    }

    for( int i=l; i<=r; i++ ){
        if( abs(tab[i].x - tab[mid].x) <= d ) vec.push_back(tab[i]);
    }

    sort( vec.begin(), vec.end(), comp2 );
    int size1 = vec.size();

    for( int i=0; i<size1; i++ ){
        for( int j =1; j<min(7, size1-i); j++ ){
            LL dist=leng( vec[i], vec[j+i] );
            if( dist<d ){
                d=dist;
                pnts = {vec[i], vec[i+j]};
            }
        }
    }

    vec.clear();
    return {d,pnts};
}

int main( ){
    ios_base::sync_with_stdio(0);
    cin.tie(0);

    cin>>n;
    for( int i=0; i<n; i++ ){
        tab[i].read();
    }
    
    sort( tab, tab+n, comp1 );
    // cerr<<"posortowane pnkty: \n";
    // for( int i=0; i<n; i++  ){
    //     point p = tab[ i ];
    //     cerr<<"["<<p.x<<','<<p.y<<"] ";
    // }
    // cerr<<'\n';


    pair<LL, pair<point,point>> result=nearest_points( 0, n-1 );
    pair<point,point> pnts = result.second;

    // if( result.first==0 ) cout<<"min dist to "<<result.first<<' '<<"["<<pnts.second.x<<","<<pnts.second.y<<"] ["<<pnts.first.x<<','<<pnts.first.y<<"]"<<'\n';
    // else cout<<result.first<<'\n';

    cout<<pnts.first.x<<' '<<pnts.first.y<<'\n';
    cout<<pnts.second.x<<' '<<pnts.second.y<<'\n';
    
}