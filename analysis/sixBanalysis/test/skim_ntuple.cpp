// skim_ntuple.exe --input input/PrivateMC_2018/NMSSM_XYH_YToHH_6b_MX_600_MY_400.txt --cfg config/skim_ntuple_2018.cfg  --output prova.root --is-signal

#include <iostream>
#include <string>
#include <iomanip>
#include <any>

#include <boost/program_options.hpp>
namespace po = boost::program_options;

#include "CfgParser.h"
#include "NanoAODTree.h"

#include "SkimUtils.h"
namespace su = SkimUtils;

#include "OutputTree.h"
#include "jsonLumiFilter.h"

#include "SixB_functions.h"

#include "TFile.h"
#include "TROOT.h"

using namespace std;

std::vector<std::string> split_by_delimiter(std::string input, std::string delimiter)
{
    std::vector<std::string> tokens;
    if(input == "")
        return tokens;

    size_t pos = 0;
    while ((pos = input.find(delimiter)) != std::string::npos)
    {
        tokens.push_back(input.substr(0, pos));
        input.erase(0, pos + delimiter.length());
    }
    tokens.push_back(input); // last part splitted

    return tokens;
}

int main(int argc, char** argv)
{
    cout << "[INFO] ... starting program" << endl;

    ////////////////////////////////////////////////////////////////////////
    // Declare command line options
    ////////////////////////////////////////////////////////////////////////
    
    po::options_description desc("Skim options");
    desc.add_options()
        ("help", "produce help message")
        // required
        ("cfg"   , po::value<string>()->required(), "skim config")
        ("input" , po::value<string>()->required(), "input file list")
        ("output", po::value<string>()->required(), "output file LFN")
        // optional
        // ("xs"        , po::value<float>(), "cross section [pb]")
        ("maxEvts"   , po::value<int>()->default_value(-1), "max number of events to process")
        ("puWeight"  , po::value<string>()->default_value(""), "PU weight file name")
        ("seed"      , po::value<int>()->default_value(12345), "seed to be used in systematic uncertainties such as JEC, JER, etc")
        // ("kl-rew-list"  , po::value<std::vector<float>>()->multitoken()->default_value(std::vector<float>(0), "-"), "list of klambda values for reweight")
        // ("kl-rew"    , po::value<float>(),  "klambda value for reweighting")
        // ("kl-map"    , po::value<string>()->default_value(""), "klambda input map for reweighting")
        // ("kl-histo"  , po::value<string>()->default_value("hhGenLevelDistr"), "klambda histogram name for reweighting")
        ("jes-shift-syst", po::value<string>()->default_value("nominal"), "Name of the JES (scale) source uncertainty to be shifted. Usage as <name>:<up/down>. Pass -nominal- to not shift the jets")
        ("jer-shift-syst", po::value<string>()->default_value("nominal"), "Name of the JER (resolution) source uncertainty to be shifted. Usage as <jer/bjer>:<up/down>. Pass -nominal- to not shift the jets")
        // pairing variables
        // ("bbbbChoice"    , po::value<string>()->default_value("BothClosestToDiagonal"), "bbbb pairing choice")
        // ("mh1mh2"        , po::value<float>()->default_value(1.05), "Ratio Xo/Yo or 1/slope of the diagonal") 
        // ("option"        , po::value<int>()->default_value(0), "Option: 0=Nominal, 1=Alternative 1, 2=Alternative 2") 
        // flags
        ("is-data",       po::value<bool>()->zero_tokens()->implicit_value(true)->default_value(false), "mark as a data sample (default is false)")
        ("is-signal",     po::value<bool>()->zero_tokens()->implicit_value(true)->default_value(false), "mark as a HH signal sample (default is false)")
        //
        ("save-p4",       po::value<bool>()->zero_tokens()->implicit_value(true)->default_value(false), "save the tlorentzvectors in the output")
    ;

    po::variables_map opts;
    try {
        po::store(parse_command_line(argc, argv, desc, po::command_line_style::unix_style ^ po::command_line_style::allow_short), opts);
        if (opts.count("help")) {
            cout << desc << "\n";
            return 1;
        }
        po::notify(opts);
    }    
    catch (po::error& e) {
        cerr << "** [ERROR] " << e.what() << endl;
        return 1;
    }

    ////////////////////////////////////////////////////////////////////////
    // Read config and other cmd line options for skims
    ////////////////////////////////////////////////////////////////////////

    const bool is_data = opts["is-data"].as<bool>();
    cout << "[INFO] ... is a data sample? " << std::boolalpha << is_data << std::noboolalpha << endl;

    const bool is_signal = (is_data ? false : opts["is-signal"].as<bool>());
    cout << "[INFO] ... is a signal sample? " << std::boolalpha << is_signal << std::noboolalpha << endl;

    CfgParser config;
    if (!config.init(opts["cfg"].as<string>())){
        cerr << "** [ERROR] no config file was provuded" << endl;
        return 1;
    }
    cout << "[INFO] ... using config file " << opts["cfg"].as<string>() << endl;

    ////////////////////////////////////////////////////////////////////////
    // Prepare event loop
    ////////////////////////////////////////////////////////////////////////

    cout << "[INFO] ... opening file list : " << opts["input"].as<string>().c_str() << endl;
    if ( access( opts["input"].as<string>().c_str(), F_OK ) == -1 ){
        cerr << "** [ERROR] The input file list does not exist, aborting" << endl;
        return 1;        
    }

    // Joining all the NANOAD input file in a TChain in order to be used like an unique three
    TChain ch("Events");
    int nfiles = su::appendFromFileList(&ch, opts["input"].as<string>());
    
    if (nfiles == 0){
        cerr << "** [ERROR] The input file list contains no files, aborting" << endl;
        return 1;
    }
    cout << "[INFO] ... file list contains " << nfiles << " files" << endl;

    cout << "[INFO] ... creating tree reader" << endl;

    // The TChain is passed to the NanoAODTree_SetBranchImpl to parse all the branches
    NanoAODTree nat (&ch);

    ////////////////////////////////////////////////////////////////////////
    // Trigger information
    ////////////////////////////////////////////////////////////////////////

    cout << "[INFO] ... loading " << config.readStringListOpt("triggers::makeORof").size() << " triggers" << endl;

    const bool apply_trigger =  config.readBoolOpt("triggers::applyTrigger");
    cout << "[INFO] ... is the OR decision of these triggers applied? " << std::boolalpha << apply_trigger << std::noboolalpha << endl;

    std::vector<std::string> triggerAndNameVector;
    if(apply_trigger) triggerAndNameVector = config.readStringListOpt("triggers::makeORof");
    std::vector<std::string> triggerVector;
    // <triggerName , < objectBit, minNumber> >
    std::map<std::string, std::map< std::pair<int,int>, int > > triggerObjectAndMinNumberMap;

    cout << "[INFO] ... listing the triggers applied" << endl;
    for (auto & trigger : triggerAndNameVector)
    {
        if(trigger == "")
            continue;
        
        std::vector<std::string> triggerTokens = split_by_delimiter(trigger, ":");
        if (triggerTokens.size() != 2)
            throw std::runtime_error("** skim_ntuple : could not parse trigger entry " + trigger + " , aborting");

        triggerVector.push_back(triggerTokens[1]);
        cout << "   - " << triggerTokens[0] << "  ==> " << triggerTokens[1] << endl;

        // if(!config.hasOpt( Form("triggers::%s_ObjectRequirements",triggerTokens[0].data()) ))
        // {
        //     cout<<Form("triggers::%s_ObjectRequirements",triggerTokens[0].data())<<std::endl;
        //     cout<<"Trigger "<< triggerTokens[1] <<" does not have ObjectRequirements are not defined";
        //     continue;
        // }

        // triggerObjectAndMinNumberMap[triggerTokens[1]] = std::map< std::pair<int,int>, int>();   

        // std::vector<std::string> triggerObjectMatchingVector = config.readStringListOpt(Form("triggers::%s_ObjectRequirements",triggerTokens[0].data()));

        // for (auto & triggerObject : triggerObjectMatchingVector)
        // {

        //     std::vector<std::string> triggerObjectTokens;
        //     while ((pos = triggerObject.find(delimiter)) != std::string::npos)
        //     {
        //         triggerObjectTokens.push_back(triggerObject.substr(0, pos));
        //         triggerObject.erase(0, pos + delimiter.length());
        //     }
        //     triggerObjectTokens.push_back(triggerObject); // last part splitted
        //     if (triggerObjectTokens.size() != 3)
        //     {
        //         throw std::runtime_error("** skim_ntuple : could not parse trigger entry " + triggerObject + " , aborting");
        //     }

        //     triggerObjectAndMinNumberMap[triggerTokens[1]][std::pair<int,int>(atoi(triggerObjectTokens[0].data()),atoi(triggerObjectTokens[1].data()))] = atoi(triggerObjectTokens[2].data());
        // }
    }

    nat.triggerReader().setTriggers(triggerVector);

    ////////////////////////////////////////////////////////////////////////
    // Prepare the output
    ////////////////////////////////////////////////////////////////////////
 
    string outputFileName = opts["output"].as<string>();
    cout << "[INFO] ... saving output to file : " << outputFileName << endl;
    TFile outputFile(outputFileName.c_str(), "recreate");
    OutputTree ot(
        opts["save-p4"].as<bool>()
    );
  
    jsonLumiFilter jlf;
    if (is_data)
        jlf.loadJSON(config.readStringOpt("data::lumimask")); // just read the info for data, so if I just skim MC I'm not forced to parse a JSON

    ////////////////////////////////////////////////////////////////////////
    // Execute event loop
    ////////////////////////////////////////////////////////////////////////

    int maxEvts = opts["maxEvts"].as<int>();
    if (maxEvts >= 0)
        cout << "[INFO] ... running on : " << maxEvts << " events" << endl;

    SixB_functions sbf;

    for (int iEv = 0; true; ++iEv)
    {
        if (maxEvts >= 0 && iEv >= maxEvts)
            break;

        if (!nat.Next()) break;
        if (iEv % 10000 == 0) cout << "... processing event " << iEv << endl;

        if (is_data && !jlf.isValid(*nat.run, *nat.luminosityBlock)){
            continue; // not a valid lumi
        }

        EventInfo ei;

        sbf.copy_event_info(nat, ei);

        if (is_signal){
            sbf.select_gen_particles   (nat, ei);
            sbf.match_genbs_to_genjets (nat, ei);
        }

        std::vector<Jet> all_jets    = sbf.get_all_jets     (nat);
        // FIXME: here smear and resolution of jets when required
        std::vector<Jet> presel_jets = sbf.preselect_jets   (nat, all_jets);
        std::vector<Jet> sixb_jets   = sbf.select_sixb_jets (nat, presel_jets);
        if (sixb_jets.size() < 6)
            continue;
        sbf.pair_jets(nat, ei, sixb_jets);

        su::fill_output_tree(ot, nat, ei);
    }

    outputFile.cd();
    ot.write();
}