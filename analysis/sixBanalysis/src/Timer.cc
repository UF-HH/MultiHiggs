#include "Timer.h"
#include <iomanip>

void Timer::start_lap()
{
  if (debug_lvl >= 2) std::cout << "[DEBUG] Timer : start_lap" << std::endl;

  // restart the timer
  curr_idx_ = -1;
  curr_start_t_ = std::chrono::high_resolution_clock::now();
}

// void Timer::end_lap()
// {
//     if (debug_lvl >= 2) std::cout << "[DEBUG] Timer : end_lap" << std::endl;

//     // update the statistics up to the last step seen
//     for (int idx = 0; idx <= curr_idx_; ++idx)
//     {
//         if (debug_lvl >= 2) std::cout << "[DEBUG] Timer : end_lap : checking idx " << idx << std::endl;

//         deltat_t dt;
//         if (idx == 0){
//             dt = std::chrono::duration_cast<deltat_t>(step_time_.at(0) - curr_start_t_);
//         }
//         else{
//             dt = std::chrono::duration_cast<deltat_t>(step_time_.at(idx) - step_time_.at(idx-1));
//         }
//         step_dt_.at(idx) += dt;
//         if (debug_lvl >= 2) std::cout << "[DEBUG] Timer : end_lap : checked idx " << idx << " dt was " << dt.count() << std::endl;
//     }
// }

void Timer::click(std::string name)
{
  if (debug_lvl >= 2) std::cout << "[DEBUG] Timer : click : clicking for step " << name << std::endl;

  // check if this is a new key
  auto it = m_idx_.find(name);
  int idx;
  if (it == m_idx_.end()){
    insert_step(name);
    idx = steps_.size()-1; // by construction this is the last item in the list
  }
  else
    idx = it->second;

  if (debug_lvl >= 2) std::cout << "[DEBUG] Timer : click : clicking for step " << name << " : idx is " << idx << std::endl;

  step_calls_.at(idx) += 1;
  abstime_t now = std::chrono::high_resolution_clock::now();
  // step_time_.at(idx) = std::chrono::high_resolution_clock::now();
  deltat_t dt = std::chrono::duration_cast<deltat_t>(now - curr_start_t_);
  step_dt_.at(idx) += dt;
  curr_start_t_ = now;
  curr_idx_ = idx; // last index seen
}

void Timer::insert_step(std::string name)
{
  if (debug_lvl >= 1) std::cout << "[DEBUG] Timer : inserted new field : " << name << std::endl;

  steps_.push_back(name);
  m_idx_[name] = steps_.size()-1;
  // step_time_.resize(steps_.size());
  step_calls_.resize(steps_.size());
  step_calls_.back() = 0;
  step_dt_.resize(steps_.size());
  step_dt_.back() = deltat_t(0);

  if (debug_lvl >= 1) std::cout << "[DEBUG] Timer : inserted new field : done for " << name
				<< " field sizes are now "
				<< steps_.size() << " "
			// << step_time_.size() << " "
				<< step_calls_.size() << " "
				<< step_dt_.size() << " "
				<< std::endl;

}

void Timer::print_summary()
{
  double tot_s = 0;
  for (unsigned int idx = 0; idx < steps_.size(); ++idx)
    tot_s += step_dt_.at(idx).count() / 1000000.;

  std::streamsize ss = std::cout.precision(); // default stream precision
  for (unsigned int idx = 0; idx < steps_.size(); ++idx)
    {
      // std::cout << std::setw(35) << std::left <<
      std::cout << "-- " << steps_.at(idx) << std::endl;
      // std::cout << "   ... average [us]          : " << 1.*step_dt_.at(idx).count()/step_calls_.at(idx) << std::endl;
      std::cout << "   ... time/10000 events [s] : " << 0.01*step_dt_.at(idx).count()/step_calls_.at(idx) << std::endl;
      std::cout << "   ... total time spent  [s] : " << step_dt_.at(idx).count()/1000000. << std::endl;
      std::cout << std::fixed << std::setprecision(1);
      std::cout << "   ... frac. time spent      : " << 100. * ((step_dt_.at(idx).count() / 1000000.) / tot_s) << " %" << std::endl;
      std::cout << std::fixed << std::setprecision(ss);
      std::cout << "   ... calls :               : " << step_calls_.at(idx) << std::endl;
    }
  std::cout << std::endl;
  std::cout << "-- -- TOTAL ELAPSED TIME [s] : " << tot_s << std::endl;
}
