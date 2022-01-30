#include <vector>
#include <fstream>
#include <iostream>
#include <algorithm>
#include <cmath>

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

float dist(pair<float,float> p1, pair<float,float> p2){
  return sqrt((p1.first-p2.first)*(p1.first-p2.first)+(p1.second-p2.second)*(p1.second-p2.second));
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
      lns[i].push_back(pts[i].back());
      pts[i].pop_back();
      while(!pts[i].empty()){
        float minDist = dist(pts[i][0], lns[i].back());
        int minJ = 0;
        for(int j = 1; j < pts[i].size(); j++)
          if (dist(pts[i][j], lns[i].back()) < minDist){
            minDist = dist(pts[i][j], lns[i].back());
            minJ = j;
          }
        lns[i].push_back(pts[i][minJ]);
        pts[i].erase(pts[i].begin()+ minJ);
      }
      cout << i<<" done\n";
    }
  }

  saveLns(fileName+".ln", lns);
}