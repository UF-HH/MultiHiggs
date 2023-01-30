#include "Combinatorics.h"

using namespace std;

vector<int> remaining(const vector<int> a_, const vector<int> b)
{
  vector<int> a = a_;
  if (b.size() == 0)
    return a;
    
  a.erase(std::remove_if(a.begin(), a.end(), [b](int value)
                         { return (std::find(b.begin(), b.end(), value) != b.end()); }),
          a.end());
  return a;
}

vector<vector<int>> combinations(const vector<int> items, int k)
{
  vector<bool> mask(items.size());
  std::fill(mask.begin(), mask.begin() + k, true);

  vector<vector<int>> combs;
  do
  {
    vector<int> comb;
    for (unsigned int i = 0; i < mask.size(); ++i)
    {
      if (mask[i])
      {
        comb.push_back(items[i]);
      }
    }
    combs.push_back(comb);
  } while (std::prev_permutation(mask.begin(), mask.end()));

  return combs;
}

vector<vector<int>> combinations(int items_, int k)
{
  vector<int> items(items_);
  for (int i = 0; i < items_; i++)
  {
    items[i] = i;
  }

  return combinations(items, k);
}

vector<vector<vector<int>>> combinations(const vector<int> items, deque<int> ks)
{
  vector<vector<vector<int>>> f_groups;

  int k = ks.front();
  ks.pop_front();

  auto combs = combinations(items, k);

  if (ks.size() == 0)
  {
    for (auto comb : combs)
      f_groups.push_back({comb});
  }

  else
  {
    for (auto comb : combs)
    {
      auto remain = remaining(items, comb);
      auto o_groups = combinations(remain, ks);

      for (auto o_group : o_groups)
      {
        vector<vector<int>> group = {comb};

        if (group[0][0] > o_group[0][0] && group[0].size() == o_group[0].size())
          continue;

        group.insert(group.end(), o_group.begin(), o_group.end());
        f_groups.push_back(group);
      }
    }
  }

  return f_groups;
}

vector<vector<vector<int>>> combinations(int items_, deque<int> ks)
{
  vector<int> items(items_);
  for (int i = 0; i < items_; i++)
  {
    items[i] = i;
  }

  return combinations(items, ks);
}

vector<vector<vector<int>>> combinations(const vector<int> items, vector<int> ks_)
{
  std::deque<int> ks;
  std::move(ks_.begin(), ks_.end(), std::back_inserter(ks));
  return combinations(items, ks);
}

vector<vector<vector<int>>> combinations(int items_, vector<int> ks)
{
  vector<int> items(items_);
  for (int i = 0; i < items_; i++)
  {
    items[i] = i;
  }

  return combinations(items, ks);
}