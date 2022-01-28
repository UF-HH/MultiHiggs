#ifndef TIMER_H
#define TIMER_H

/*
** class  : Timer
** author : L. Cadamuro (UF)
** date   : 02/12/2020
** brief  : class to time the repeated execution time of functions in a loop
** note   : the timer assumes that all operations are sequential, and registers the delta time from the previous one
**        : an average or cumulated runtime is then printed
**        : new steps in the stopwatch are automatically detected when a ".click(name)" instruction is given
**        : if name is seen for the first time, the name is appended to the list of steps
**        : if name was already seen, the timer is updated
**        : the lap is restarted by calling "start_lap" and stopped with "end_lap"
**
**        : NOTE: since we expect few steps to be timed [O(10)], the code relies on maps to index the steps
*/

#include <iostream>
#include <chrono>
#include <string>
#include <vector>
#include <unordered_map>

class Timer
{
public:

  typedef std::chrono::time_point<std::chrono::high_resolution_clock> abstime_t;
  typedef std::chrono::microseconds deltat_t;

  Timer()  {curr_idx_ = -1;}
  ~Timer() {}
  void start_lap();
  void click(std::string name);
  void print_summary();
    
private:
  void insert_step(std::string name);
  std::unordered_map<std::string, int> m_idx_; // maps a string to the position of a vector for at at(idx) access

  std::vector<std::string> steps_;
  // std::vector<abstime_t> step_time_;
  std::vector<deltat_t> step_dt_;
  std::vector<int> step_calls_;
                
  abstime_t curr_start_t_;
  int curr_idx_;

  const int debug_lvl = 0; // 0 : none. 1: low verbosity. 2 : all events
};


#endif
