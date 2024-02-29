#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <chrono>
#include <rapidcsv.h>

std::vector<std::vector<std::string>> read_csv_ifstream(const std::string& filename) {
  std::ifstream file(filename);
  std::vector<std::vector<std::string>> data;

  if (!file.is_open()) {
    throw std::runtime_error("Error opening file");
  }

  std::string line;
  while (std::getline(file, line)) {
    std::vector<std::string> row;
    std::stringstream ss(line);
    std::string cell;
    while (std::getline(ss, cell, ',')) {
      row.push_back(cell);
    }
    data.push_back(row);
  }

  file.close();
  return data;
}

std::vector<std::vector<std::string>> read_csv_rapidcsv(const std::string& filename) {
  std::vector<std::vector<std::string>> data;
  rapidcsv::Document doc(filename);

  for (const rapidcsv::Row& row : doc) {
    std::vector<std::string> row_data;
    for (const rapidcsv::Cell& cell : row) {
      row_data.push_back(cell.get<std::string>());
    }
    data.push_back(row_data);
  }

  return data;
}

int main() {
  const std::string filename = "data/btag/2018/reshaping_deepJet_v3.csv";

  // Measure time for std::ifstream
  auto start_time = std::chrono::high_resolution_clock::now();
  std::vector<std::vector<std::string>> data_ifstream = read_csv_ifstream(filename);
  auto end_time = std::chrono::high_resolution_clock::now();
  std::chrono::duration<double, std::nano> elapsed_ifstream = end_time - start_time;

  // Measure time for RapidCSV
  start_time = std::chrono::high_resolution_clock::now();
  std::vector<std::vector<std::string>> data_rapidcsv = read_csv_rapidcsv(filename);
  end_time = std::chrono::high_resolution_clock::now();
  std::chrono::duration<double, std::nano> elapsed_rapidcsv = end_time - start_time;

  // Print data size and execution times
  std::cout << "Data size: " << data_ifstream.size() << "x" << data_ifstream[0].size() << std::endl;
  std::cout << "std::ifstream: " << elapsed_ifstream.count() / 1e9 << " seconds" << std::endl;
  std::cout << "RapidCSV: " << elapsed_rapidcsv.count() / 1e9 << " seconds" << std::endl;

  return 0;
}
