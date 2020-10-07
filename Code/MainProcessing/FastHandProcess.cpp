#include <iostream>
#include <set>
#include <array>
#include <vector>
#include <cmath>
#include <string>
#include <algorithm>
#include <sys/resource.h>
#include <cstring>
#include<fstream>

using namespace std;

#define DWORD int32_t

// The handranks lookup table- loaded from HANDRANKS.DAT.
int HR[32487834];

set<int> allCards;


void initiateAllCards(){
    for(int i = 1; i <53; i++)
        allCards.insert(i);
}
int initiateHR(){
    memset(HR, 0, sizeof(HR));
    FILE *fin = fopen("/Volumes/GoogleDrive/My Drive/Research2020/MyPoker/HandRanking/HandRanks.dat", "rb");
    if (!fin)
        return -1;
    fread(HR, sizeof(HR), 1, fin);    // get the HandRank Array
    fclose(fin);
    return 1;
}

template <typename Iterator>
inline bool next_combination(const Iterator first, Iterator k, const Iterator last)
{
   if ((first == last) || (first == k) || (last == k)) return false;
   Iterator itr1 = first;
   Iterator itr2 = last;
   ++itr1;
   if (last == itr1) return false;
   itr1 = last; --itr1; itr1 = k; --itr2;
   while (first != itr1)
   {
      if (*--itr1 < *itr2)
      {
         Iterator j = k;
         while (!(*itr1 < *j)) ++j;
         std::iter_swap(itr1,j);
         ++itr1;
         ++j;
         itr2 = k;
         std::rotate(itr1,j,last);
         while (last != j)
         {
            ++j;
            ++itr2;
         }
         std::rotate(k,itr2,last);
         return true;
      }
   }
   std::rotate(first,k,last);
   return false;
}





double EHS7(int* cards)
{
    set<int> s1;
    for(int i=0; i < 7; i++) s1.insert(cards[i]);
    
    set<int> intersect;
    set_difference(allCards.begin(),allCards.end(),s1.begin(),s1.end(),std::inserter(intersect,intersect.begin()));
        
    const size_t n = 45;
    const size_t k = 2;
    array<int, n> arr;
    int i=0;
    for(int x: intersect) arr[i++] = x;
    
    int* temp = cards;
    int inputScore = HR[53 + *temp++];
    for(int i=0; i < 6; i++)
        inputScore = HR[inputScore + *temp++];
    
    double w=0,l=0,t=0;
    temp = cards; temp++; temp++;
    int tempScore = HR[53 + *temp++];
    for(int i=0; i < 4; i++)
        tempScore = HR[tempScore + *temp++];

    do
    {
        int s = HR[HR[tempScore + arr[0]] + arr[1]];
        if(s>inputScore) l++;
        else if(s==inputScore) t++;
        else w++;
    }
    while(next_combination(arr.begin(),arr.begin() + k,arr.end()));
    
    return (w + 0.5*t)/(w+t+l);
}

double EHS6(int* cards)
{
    set<int> s1;
    for(int i=0; i < 6; i++) s1.insert(cards[i]);
    
    set<int> intersect;
    set_difference(allCards.begin(),allCards.end(),s1.begin(),s1.end(),std::inserter(intersect,intersect.begin()));
    
    int size = int(intersect.size());
    int arr[size];
    
    int i=0;
    for(int x: intersect) arr[i++] = x;
    
    int cards7[7] = {cards[0],cards[1],cards[2],cards[3],cards[4],cards[5],-1};
    double totalEquity = 0;
    for(int x: arr)
    {
        cards7[6] = x;
        totalEquity += EHS7(cards7);
    }
    
    return totalEquity/size;
}

double EHS5(int* cards)
{
    set<int> s1;
    for(int i=0; i < 5; i++) s1.insert(cards[i]);
    
    set<int> intersect;
    set_difference(allCards.begin(),allCards.end(),s1.begin(),s1.end(),std::inserter(intersect,intersect.begin()));
        
    const size_t n = 47;
    const size_t k = 2;
    array<int, n> arr;
    int i=0;
    for(int x: intersect) arr[i++] = x;

    double totalEquity = 0;
    int cards7[7] = {cards[0],cards[1],cards[2],cards[3],cards[4],-1,-1};
    do
    {
        cards7[5]=arr[0]; cards7[6]=arr[1];
        totalEquity += EHS7(cards7);
    }
    while(next_combination(arr.begin(),arr.begin() + k,arr.end()));
    
    return totalEquity/(n*(n-1)/2);
}
double EHS2(int* cards)
{
    set<int> s1;
    for(int i=0; i < 2; i++) s1.insert(cards[i]);
    
    set<int> intersect;
    set_difference(allCards.begin(),allCards.end(),s1.begin(),s1.end(),std::inserter(intersect,intersect.begin()));
    
    const size_t n = 50;
    const size_t k = 5;
    array<int, n> arr;
    int i=0;
    for(int x: intersect) arr[i++] = x;

    double totalEquity = 0;
    int count =0;
    int cards7[7] = {cards[0],cards[1],-1,-1,-1,-1,-1};
    do
    {
        cards7[2]=arr[0]; cards7[3]=arr[1]; cards7[4]=arr[2];
        cards7[5]=arr[3]; cards7[6]=arr[4];
        totalEquity += EHS7(cards7);
        if(++count%10000==0) printf("%d\n",count);
    }
    while(next_combination(arr.begin(),arr.begin() + k,arr.end()));
    
    return totalEquity/2118760;
}


int* histo(int* cards, int* histo, int a, int b)
{
    int* h = histo;
    set<int> s1;
    for(int i=0; i < a; i++) s1.insert(cards[i]);
    
    set<int> intersect;
    set_difference(allCards.begin(),allCards.end(),s1.begin(),s1.end(),std::inserter(intersect,intersect.begin()));
    
    size_t k = b-a;
    vector<int> arr;
    for(int x: intersect) arr.push_back(x);
        
    vector<int> c;
    for(int i=0; i < a; i++) c.push_back(cards[i]);
    for(int i=a; i < b; i++) c.push_back(-1);
    
    do
    {
        for(int i = a; i < b; i++) c[i] = arr[i-a];

        double v;
        if(b==5) v = EHS5(&c[0]);
        else if(b==6) v = EHS6(&c[0]);
        else v = EHS7(&c[0]);
        
        int val = int(floor(v * 100));
        if(val==100) val=99;
        h[val]++;
    }
    while(next_combination(arr.begin(),arr.begin() + k,arr.end()));
    
    return histo;
}


int main(int argc, char* argv[])
{
    initiateAllCards();
    if(initiateHR()==-1) return -1;
    
    int x[] = {1,2,3,4,5,6,7};//{23,14,51,10,11,40,18};
    printf("%f\n",EHS7(x));
    //string x = "hello"+string(argv[0])+string(argv[1]);
    //printf("%s",x.c_str());
    /*
    ifstream myReadFile;
    myReadFile.open("/Users/alexpaskov/Downloads/sixI2H.txt");
    string line;
    int numCards = 6, id;
    int count = 0;
    if (myReadFile.is_open())
    {
        while (!myReadFile.eof())
        {
            myReadFile >> line;
            int idx = 0;
            for(char x: line)
            {
                if(x==':')
                    break;
                idx++;
            }
            idx++;
            id = atoi(line.substr(0,idx-1).c_str());
            if(count>55190500) printf("%d,",id);
            for(int i = 0; i < numCards; i++)
            {
                if(count>55190500) printf("%d,",atoi(line.substr(idx+i*2,2).c_str()));
            }
            if(count++>55190500) printf("\n");
        
        }
    }
    myReadFile.close();
    return 0;
    *//*
    int cards[] = { 1, 40};//, 17, 29, 35 , 23};//17, 29, 35, 23};//, 50};
    printf("before\n");
    double x = EHS2(cards);
    printf("after\n");

    
    initiateAllCards();
    if(initiateHR()==-1) return -1;
    //int cards[] = { 1, 40, 17, 29, 35, 23};//, 50};
    int hist[100] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                      0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
    //5c9d-3d5d7d
    int cards[] = {52,51};//48,44,40,36};//, 13, 10, 6, 14};//, 22};
    histo(cards,hist,2,5);
    //printf("%f\n",EHS5(cards));
    for(int x: hist)
        printf("%d ",x);
    printf("\n");

    
    "2c": 1,
    "2d": 2,
    "2h": 3,
    "2s": 4,
    "3c": 5,
    "3d": 6,
    4c 9
    5c 13
    6c 17
    7c 21
    8c 25
    9c 29
    10c 33
    jc 37
    qc 41
    kc 45
    "kh": 47,
    "ks": 48,
    "ac": 49,
    "ad": 50,
    "ah": 51,
    "as": 52*/
}
