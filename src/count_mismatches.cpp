#include <bits/stdc++.h>
using namespace std;

void add_count(string seq, vector<map<char, int>> &count) {
	if (seq.empty()) {
		return;
	}
	
	if (count.empty()) {
		count.resize(seq.size());	
	}
	
	assert(seq.size() == count.size());
	for (int i = 0; i < seq.size(); i++) {
		count[i][seq[i]]++;
	}
}

int main(int argc, char **argv) {
	ifstream in_file(argv[1]);
	if (!in_file.is_open()) {
		return {};
	}
	cout << argv[1] << '\n';
	
	vector<map<char, int>> count;
	string line;
	string seq;
	int num_seqs = 0;
	while (getline(in_file, line)) {
		if (line.empty() or line[0] != '>') {
			seq.append(line);
			continue;
		}
		
		num_seqs++;
		if (num_seqs % 1000 == 0) {
			cout << "Seq: " << num_seqs << ' ' << seq.size() << endl;
		}
		add_count(seq, count);
		seq = "";
	}
	num_seqs++;
	cout << "Seq: " << num_seqs << ' ' << seq.size() << endl;
	add_count(seq, count);
	in_file.close();
	
	map<string, vector<long long>> res;
	for (int i = 0; i < count.size(); i++) {
		for (pair<char, int> p : count[i]) {
			for (pair<char, int> q : count[i]) {
				if (p.first == q.first) {
					continue;
				}
				
				string s = string(1, p.first) + q.first;
				if (!res.count(s)) {
					res[s] = vector<long long>(count.size(), 0);
				}
				
				res[s][i] = ((long long) p.second) * q.second;
			}
		}
	}
	
	ofstream out_file(argv[2]);
	out_file << "Col";
	for (pair<string, vector<long long>> p : res) {
		out_file << ',' << p.first;
	}
	out_file << ",Total\n";
	for (int i = 0; i < count.size(); i++) {
		if (i % 100 == 99) {
			cout << "Col: " << i + 1 << endl;
		}
		out_file << i + 1;
		long long x = 0;
		for (pair<string, vector<long long>> p : res) {
			out_file << ',' << p.second[i];
			x += p.second[i];
		}
		out_file << ',' << x << '\n';
	}
	out_file.close();
}
