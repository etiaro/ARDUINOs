#include <vector>
#include <fstream>
#include <iostream>
#include <algorithm>
#include <cmath>
#include <queue>

using namespace std;

void loadPts(string fileName, vector<vector<pair<float, float>>> &pts){
  ifstream rf(fileName, ios::out | ios::binary);
  if(!rf) {
    cout << "Cannot open file!" << endl;
  }
  int len;
  for(int i = 0; i < 4; i++){
    rf.read((char *) &len, sizeof(len));
    pts[i].resize(len);
    for(int j = 0; j < len; j++){
      rf.read((char *) &pts[i][j].first, sizeof(float));
      rf.read((char *) &pts[i][j].second, sizeof(float));
    }
  }
  rf.close();
}

void saveLns(string fileName, vector<vector<pair<float, float>>> &lns){
  ofstream wf(fileName, ios::out | ios::binary);
  if(!wf) {
    cout << "Cannot open file!" << endl;
  }
  int len;
  for(int i = 0; i < 4; i++){
    len = lns[i].size();
    wf.write((char *) &len, sizeof(len));
    for(int j = 0; j < len; j++){
      wf.write((char *) &lns[i][j].first, sizeof(float));
      wf.write((char *) &lns[i][j].second, sizeof(float));
    }
  }
  wf.close();
}

float dist(pair<float,float> &p1, pair<float,float> &p2){
  return sqrt((p1.first-p2.first)*(p1.first-p2.first)+(p1.second-p2.second)*(p1.second-p2.second));
}
struct Con {
  int a, b;
  float dist;
};
bool operator<(const Con &c1, const Con &c2){
  if(c1.dist == c2.dist){
    if(c1.a == c2.a) return c1.b < c2.b;
    return c1.a < c2.a;
  }
  return c1.dist < c2.dist;
}

int find(int v, vector<int> &fu){
  if(fu[v] == v) return v;
  fu[v] = find(fu[v], fu);
  return fu[v];
}

int main(int arg, char** argsv){
  if (arg < 2){
    cout << "GIVE FILENAME!";
    return 0;
  }
  string fileName = argsv[1];
  vector<vector<pair<float, float>>> pts(4);
  loadPts(fileName, pts);

  vector<vector<pair<float, float>>> lns(4);
  for(int i = 0; i < 4; i++){
    if(pts[i].size()>0){
      vector<Con> cons(pts[i].size()*(pts[i].size()-1)/2);
      int x = 0;
      for(int a = 0; a < pts[i].size(); a++)
        for(int b = a+1; b < pts[i].size(); b++)
          cons[x++] = {a, b, dist(pts[i][a], pts[i][b])};
      sort(cons.begin(), cons.end());
      cout << "...";
      vector<vector<int>> g(pts[i].size());
      vector<int> fu(pts[i].size());
      for(int j = 0; j < pts[i].size(); j++) fu[j] = j;
      int tmp = 0;
      for(auto act : cons)
        if(g[act.a].size() < 2 && g[act.b].size() < 2 && find(act.a, fu) != find(act.b, fu)) {
          g[act.a].push_back(act.b);
          g[act.b].push_back(act.a);
          fu[find(act.a, fu)] = find(act.b, fu);
          tmp++;
        }
      int beg = 0;
      for(int j = 0; j < pts[i].size(); j++)
        if(g[j].size() < 2){
          beg = j;
          break;
        }
      queue<int> q;q.push(beg);
      vector<bool> was(pts[i].size(), false);
      while(!q.empty()){
        int act = q.front(); q.pop();
        was[act] = true;
        lns[i].push_back(pts[i][act]);
        for(auto v : g[act]) if(!was[v]) q.push(v);
      }
      cout << "done "<< i <<endl;;
    }
  }

  saveLns(fileName+".ln", lns);
}