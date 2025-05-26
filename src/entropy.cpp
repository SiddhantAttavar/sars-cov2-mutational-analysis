#include <bits/stdc++.h>
using namespace std;

const double percentile = 0.9;

int main(int argc, char **argv) {
	ifstream in_file(argv[1]);
	if (!in_file.is_open()) {
		return {};
	}

	string alpha = "ATCG-";

	string line;
	vector<vector<int>> f;
	int c = 0;
	string seq;
	while (getline(in_file, line)) {
		if (line[0] != '>') {
			seq.append(line);
			continue;
		}

		if (seq.empty()) {
			continue;
		}

		c++;
		if (c % 1000 == 0) {
			cout << "Seq: " << c << endl;
		}

		if (f.empty()) {
			f.resize(seq.size(), vector<int>(alpha.size()));
		}

		for (int i = 0; i < seq.size(); i++) {
			if (seq[i] == '-') {
				continue;
			}
			int j = alpha.find(seq[i]);
			if (j == -1) {
				continue;
			}
			f[i][j]++;
		}

		seq = "";
	}
	in_file.close();

	double eps = 1e-6;
	vector<double> v(f.size(), 0);
	for (int i = 0; i < f.size(); i++) {
		for (int j : f[i]) {
			double y = (j * 1.0) / c;
			v[i] -= y * log2(min(1.0, y + eps));
		}
	}
	
	ofstream out_file(argv[2]);
	out_file << "Col";
	for (char c : alpha) {
		out_file << ',' << c;
	}
	out_file << ",Entropy";
	out_file << '\n';
	for (int i = 0; i < f.size(); i++) {
		out_file << i + 1;
		for (int j : f[i]) {
			out_file << ',' << j;
		}
		out_file << ',' << v[i];
		out_file << '\n';
	}
	out_file.close();
	return 0;

	cout << "debug" << endl;
}
