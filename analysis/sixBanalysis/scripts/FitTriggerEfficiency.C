#include "Riostream.h"
#include "TFile.h"
#include "TGraphAsymmErrors.h"
#include "TGraphErrors.h"
#include "TGraph.h"
#include "TF1.h"
#include "TF1Convolution.h"
#include "TCanvas.h"
#include "TMath.h"
#include "TFitResultPtr.h"
#include "TFitResult.h"
#include "TStyle.h"
#include "TString.h"
#include "TAxis.h"
#include "TVirtualFitter.h"
#include "TSpline.h"
#include "TLegend.h"

ofstream outputFile("fitCurves.h", ios::out);
std::string crystalBallFunction = "ROOT::Math::crystalball_cdf(x, [5], [4], [1], [0])*([3]-[2]) + [2]";
std::string crystalBallAndErrorFunction = "ROOT::Math::crystalball_cdf(x, [5], [4], [1], [0]) * (0.5*(1 + TMath::Erf( (x-[0])/[6]) ) ) *([3]-[2]) + [2]";

void doFit(TFile &outputRootFile, TVirtualPad *theCanvas, TFile &theInputFile, std::string&& plotName, std::string fitFunction, std::vector<double> initialParameters , double xMin, double xMax, bool drawPlot = true, std::string appendToFunctionName = "", bool forceToOne = false)
{
  std::cout << "--- Fitting plot " << plotName << std::endl;
  TGraphAsymmErrors* theTriggerEfficiency = (TGraphAsymmErrors*)theInputFile.Get(plotName.data());
  theCanvas->cd();
  
  std::string fullFunctionName = plotName + appendToFunctionName;
  
  
  TF1 *theFunction  = new TF1("cdf",fitFunction.data(), xMin, xMax);
  
  if (fitFunction.find("crystalball_cdf") != string::npos)
    {
      TF1 *theSCurveFunction = new TF1("fitFunction", "0.5*(1 + TMath::Erf( (x[0]-[0])/[1]) ) * ([3]-[2]) + [2]", xMin, xMax);
      theSCurveFunction->SetParameters(initialParameters.data());
      theFunction->SetParameters(initialParameters.data());
      theSCurveFunction->SetParLimits(2,0,1);
      theSCurveFunction->SetParLimits(3,0,1);
      theTriggerEfficiency->Fit(theSCurveFunction, "Q0RE");
      
      theFunction->SetParameter(0, theSCurveFunction->GetParameter(0));
      theFunction->SetParameter(1, theSCurveFunction->GetParameter(1));
      theFunction->SetParameter(2, theSCurveFunction->GetParameter(2));
      theFunction->SetParameter(3, theSCurveFunction->GetParameter(3));
      theFunction->SetParameter(4, 3.);
      theFunction->SetParameter(5, 3.);
      theFunction->SetParLimits(2,0,1);
      theFunction->SetParLimits(3,0,1);
      theFunction->SetParLimits(4,1.001,10);
      theFunction->SetParLimits(5,0.001,10.);
      if(fitFunction.find("Erf") != string::npos) theFunction->SetParLimits(6,10.,100.);
      theTriggerEfficiency->Fit(theFunction, "Q0RE");
      
      theFunction->FixParameter(0, theFunction->GetParameter(0));
      theFunction->FixParameter(1, theFunction->GetParameter(1));
      theFunction->FixParameter(2, theFunction->GetParameter(2));
      theFunction->FixParameter(3, theFunction->GetParameter(3));
      theTriggerEfficiency->Fit(theFunction, "Q0R");
      
      theFunction->ReleaseParameter(0);
      theFunction->ReleaseParameter(1);
      theFunction->FixParameter(4, theFunction->GetParameter(4));
      theFunction->FixParameter(5, theFunction->GetParameter(5));
      theTriggerEfficiency->Fit(theFunction, "Q0R");
      
      theFunction->ReleaseParameter(4);
      theFunction->ReleaseParameter(5);
      theFunction->SetParLimits(4,1.001,10);
      theFunction->SetParLimits(5,0.001,10.);
      theTriggerEfficiency->Fit(theFunction, "Q0R");
      
      
      theFunction->ReleaseParameter(2);
      theFunction->ReleaseParameter(3);
      theFunction->SetParLimits(2,0,1);
      theFunction->SetParLimits(3,0,1);
      theFunction->SetParLimits(4,1.01,10);
      if(forceToOne) theFunction->FixParameter(3,1.);
    }
  
  theFunction->SetLineColor(kBlack);
  theFunction->SetLineWidth(1);
  TSpline3 *theSpline=nullptr;
  
  if(fitFunction.find("pol") != string::npos)
    {
      theTriggerEfficiency->Fit(theFunction, "0ERQW");
      theTriggerEfficiency->Fit(theFunction, "0ERQW");
      uint16_t numberOfPoints = theTriggerEfficiency->GetN();
      std::vector<double> pointX(numberOfPoints);
      std::vector<double> pointY(numberOfPoints);
      std::vector<double> pointErrorUp(numberOfPoints);
      std::vector<double> pointErrorDown(numberOfPoints);
      for(uint16_t point=0; point<numberOfPoints; ++point)
        {
	  double pointXvalue, pointYvalue;
	  theTriggerEfficiency->GetPoint(point, pointXvalue, pointYvalue);
	  pointX[point] = pointXvalue; 
	  pointY[point] = pointYvalue; 
	  pointErrorUp  [point] = pointYvalue + theTriggerEfficiency->GetErrorYhigh(point);
	  pointErrorDown[point] = pointYvalue - theTriggerEfficiency->GetErrorYlow (point);
        }
      TGraph* theErrorGraphUp = new TGraph(numberOfPoints, pointX.data(), pointErrorUp.data());
      theErrorGraphUp->SetNameTitle((std::string(theTriggerEfficiency->GetName()) + "Up").data(),(std::string(theTriggerEfficiency->GetTitle()) + " Up").data());
      
      TGraph* theErrorGraphDown = new TGraph(numberOfPoints, pointX.data(), pointErrorDown.data());
      theErrorGraphDown->SetNameTitle((std::string(theTriggerEfficiency->GetName()) + "Down").data(),(std::string(theTriggerEfficiency->GetTitle()) + " Down").data());
      
      outputRootFile.WriteObject(theErrorGraphUp  , (fullFunctionName + "Up"  ).data());
      outputRootFile.WriteObject(theErrorGraphDown, (fullFunctionName + "Down").data());
      
      theSpline = new TSpline3("Cubic Spline", pointX.data(), pointY.data(), numberOfPoints);
    }
  TFitResultPtr fitResults = theTriggerEfficiency->Fit(theFunction, "S0ER");
  if(drawPlot) theTriggerEfficiency->Draw("ap");
  theTriggerEfficiency->GetYaxis()->SetTitleOffset(1.);
  theTriggerEfficiency->GetYaxis()->SetRangeUser(0., 1.3);
  theTriggerEfficiency->SetLineColor(kBlack);
  theTriggerEfficiency->SetMarkerColor(kBlack);
  
  //Create a TGraphErrors to hold the confidence intervals
  int nPoints = 1000;
  TGraphErrors *grint = new TGraphErrors(nPoints+1);
  grint->SetTitle("Fitted line with .68 conf. band");
  float histMin = theTriggerEfficiency->GetX()[0] - theTriggerEfficiency->GetErrorXlow(0);
  float histMax = theTriggerEfficiency->GetX()[theTriggerEfficiency->GetN()-1] + theTriggerEfficiency->GetErrorXlow(theTriggerEfficiency->GetN()-1);
  for (int i=0; i<=nPoints; i++)
    {
      double xValue = histMin + (histMax-histMin)/(double(nPoints)) * double(i);
      double yValue = theFunction->Eval(xValue);
      double yError = 0.;
      fitResults->GetConfidenceIntervals(1, 1, 1, &xValue, &yError, 0.68, true);
      grint->SetPoint(i, xValue, yValue);
      grint->SetPointError(i, (histMax-histMin)/(float(nPoints))/2., yError);
    }
  
  std::string pairObjectName = fullFunctionName + "Pair";
  std::string fitResultName = fullFunctionName + "_FitResult";
  
  outputRootFile.WriteObject(theTriggerEfficiency, fullFunctionName.data());
  outputRootFile.WriteObject(fitResults.Get(), fitResultName.data());
  
  outputFile << "    std::pair<TF1*, KFitResult*> f" << pairObjectName <<" = createPair(" << std::endl;
  outputFile << "        ((TGraphAsymmErrors*)triggerFitFile.Get(\"" << fullFunctionName << "\"))->GetFunction(\""<< theFunction->GetName() << "\")," << std::endl;
  outputFile << "        (KFitResult*)triggerFitFile.Get(\"" << fitResultName << "\")"<< std::endl;
  outputFile << "    );" << std::endl;
  outputFile << std::endl;
  
  
  grint->SetFillColor(kRed);
  grint->SetFillStyle(3001);
  grint->Draw("E3 same");
  theFunction->Draw("same");
  auto theLegend = new TLegend(0.20,0.78,0.88,0.88);
  theLegend->SetNColumns(3);
  theTriggerEfficiency->SetMarkerStyle(20);
  theTriggerEfficiency->SetMarkerSize(0.3);
  theLegend->AddEntry(theTriggerEfficiency, "eff data", "ep");
  theLegend->AddEntry(theFunction, "Fit funct", "l");
  theLegend->AddEntry(grint, "68% CL band", "f");
  theLegend->Draw("same");
  return;
}

void doAllFit2018(std::string inputFileName)
{
  gROOT->SetBatch(true);
  gStyle->SetOptFit();
  gStyle->SetStatY(0.5);
  TFile theInputFile(inputFileName.data());
  std::vector<double> initialParameters;
  
  std::string outputFileName = "TriggerEfficiency_Fit_2018_wMatching.root";
  TFile outputRootFile(outputFileName.data(), "RECREATE");
  
  outputFile << "#include \"TFile.h\""                                  << std::endl;
  outputFile << "#include \"TF1.h\""                                    << std::endl;
  outputFile << "#include \"TFitResult.h\""                             << std::endl;
  outputFile << "#include \"TGraphAsymmErrors.h\""                           << std::endl;
  outputFile << "#include \"Math/WrappedMultiTF1.h\""                   << std::endl;
  outputFile                                                            << std::endl;
  outputFile << "namespace TriggerFitCurves2018\n{"                     << std::endl;
  outputFile << "    TFile triggerFitFile(\""<< outputFileName <<"\");" << std::endl;
  outputFile << "    class KFitResult : public TFitResult"                                                                                                        << std::endl;
  outputFile << "    {"                                                                                                                                           << std::endl;
  outputFile << "    public:"                                                                                                                                     << std::endl;
  outputFile << "        using TFitResult::TFitResult;"                                                                                                           << std::endl;
  outputFile << "        KFitResult* ResetModelFunction(TF1* func){"                                                                                              << std::endl;
  outputFile << "            this->SetModelFunction(std::shared_ptr<IModelFunction>(dynamic_cast<IModelFunction*>(ROOT::Math::WrappedMultiTF1(*func).Clone())));" << std::endl;
  outputFile << "            return this;"                                                                                                                        << std::endl;
  outputFile << "        }"                                                                                                                                       << std::endl;
  outputFile << "    };"                                                                                                                                          << std::endl;
  outputFile << "    std::pair<TF1*,KFitResult*> createPair(TF1* theFunction, KFitResult* theFitResult )" << std::endl;
  outputFile << "    {"                                                                                   << std::endl;
  outputFile << "        theFitResult->ResetModelFunction(theFunction);"                                  << std::endl;
  outputFile << "        return {theFunction, theFitResult};"                                             << std::endl;
  outputFile << "    }"                                                                                   << std::endl;
  outputFile << std::endl;

  //====================================
  // Fit trigger curves for Data
  //====================================
  TCanvas *theCanvasSingleMuonRatio1 = new TCanvas("SingleMuon_2018_1", "SingleMuon_2018_1", 1400, 800);
  theCanvasSingleMuonRatio1->DivideSquare(6,0.005,0.005);
  
  initialParameters = {299, 94, 0.0, 1.0};
  doFit(outputRootFile, theCanvasSingleMuonRatio1->cd(1),theInputFile, "SingleMuon__Efficiency_L1filterHT", crystalBallAndErrorFunction, initialParameters, 160., 1500.);
  
  initialParameters = { 25., 17., 0.11, 0.99, 1.01, 2.85, 10. };
  doFit(outputRootFile, theCanvasSingleMuonRatio1->cd(2),theInputFile, "SingleMuon__Efficiency_QuadCentralJet30", crystalBallAndErrorFunction, initialParameters,  25., 300.);
  
  initialParameters = { 336.3, 66.3, 0.0, 0.99, 1.01, 1.4, 45. };
  doFit(outputRootFile, theCanvasSingleMuonRatio1->cd(3),theInputFile, "SingleMuon__Efficiency_CaloQuadJet30HT320", crystalBallAndErrorFunction, initialParameters, 200.,1200.);
  
  initialParameters = { 0.0, 5.8, 0.0, 1.0};
  doFit(outputRootFile, theCanvasSingleMuonRatio1->cd(4),theInputFile, "SingleMuon__Efficiency_BTagCaloDeepCSVp17Double", "pol5", initialParameters, 0.0, 1.0);
  
  initialParameters = { 29, 11.5, 0.0, 1.00, 1.0, 0.12, 10.0};
  doFit(outputRootFile, theCanvasSingleMuonRatio1->cd(5),theInputFile, "SingleMuon__Efficiency_PFCentralJetLooseIDQuad30", crystalBallFunction, initialParameters, 25., 250.);
  
  initialParameters = { 84, 10.97, 0.0, 1.0, 1.0, 4.23, 3.0};
  doFit(outputRootFile, theCanvasSingleMuonRatio1->cd(6),theInputFile, "SingleMuon__Efficiency_1PFCentralJetLooseID75", crystalBallFunction, initialParameters, 40., 500.);
  
  theCanvasSingleMuonRatio1->SaveAs((std::string(inputFileName.substr(0,inputFileName.length()-5) + "_" + theCanvasSingleMuonRatio1->GetName()) + "_Fit" + ".png").data());
  outputRootFile.WriteObject(theCanvasSingleMuonRatio1, theCanvasSingleMuonRatio1->GetName());
  delete theCanvasSingleMuonRatio1;
    
  TCanvas *theCanvasSingleMuonRatio2 = new TCanvas("SingleMuon_2018_2", "SingleMuon_2018_2", 1400, 800);
  theCanvasSingleMuonRatio2->DivideSquare(6,0.005,0.005);
  
  initialParameters = {66.87, 2.4, 0.05, 1.0, 1.0, 2.4, 14};
  doFit(outputRootFile, theCanvasSingleMuonRatio2->cd(1),theInputFile, "SingleMuon__Efficiency_2PFCentralJetLooseID60", crystalBallAndErrorFunction, initialParameters,  30., 300.);
  
  initialParameters = {39.54, 8.7, 0.0, 1.0, 9.81, 7.492, 21.};
  doFit(outputRootFile, theCanvasSingleMuonRatio2->cd(2),theInputFile, "SingleMuon__Efficiency_3PFCentralJetLooseID45", crystalBallAndErrorFunction, initialParameters, 25., 300.);
  
  initialParameters = {46, 8.41, 0.15, 1.0, 1.0, 8.6, 8.253};
  doFit(outputRootFile, theCanvasSingleMuonRatio2->cd(3),theInputFile, "SingleMuon__Efficiency_4PFCentralJetLooseID40", crystalBallFunction, initialParameters, 25., 200.);
  
  initialParameters = { 340., 73.7, 0.81, 1., 1., 2.3, 50.4 };
  doFit(outputRootFile, theCanvasSingleMuonRatio2->cd(4),theInputFile, "SingleMuon__Efficiency_PFCentralJetsLooseIDQuad30HT330", crystalBallFunction, initialParameters, 300., 1500.);
  
  
  initialParameters = {0.482, 0.3657, 0.489, 1.0, 1.01, 3.022};
  doFit(outputRootFile, theCanvasSingleMuonRatio2->cd(5),theInputFile, "SingleMuon__Efficiency_BTagPFDeepCSV4p5Triple", crystalBallFunction, initialParameters, 0.0, 1.0);
  
  theCanvasSingleMuonRatio2->SaveAs((std::string(inputFileName.substr(0,inputFileName.length()-5) + "_" + theCanvasSingleMuonRatio2->GetName()) + "_Fit" + ".png").data());
  outputRootFile.WriteObject(theCanvasSingleMuonRatio2, theCanvasSingleMuonRatio2->GetName());
  delete theCanvasSingleMuonRatio2;
  
  //====================================
  // Fit trigger curves for TT sample
  //====================================
  
  TCanvas *theCanvasTTbarRatio1 = new TCanvas("TTbar_2018_1", "TTbar_2018_1", 1400, 800);
  theCanvasTTbarRatio1->DivideSquare(6,0.005,0.005);
  
  initialParameters = { 240.731,  77.3069,  0.018671,  0.981187 };
  doFit(outputRootFile, theCanvasTTbarRatio1->cd(1),theInputFile, "TTbar__Efficiency_L1filterHT", crystalBallAndErrorFunction, initialParameters, 160.,1500.);
  
  initialParameters = { 35, 21, 0.0, 1.0};
  doFit(outputRootFile, theCanvasTTbarRatio1->cd(2),theInputFile, "TTbar__Efficiency_QuadCentralJet30", crystalBallAndErrorFunction, initialParameters, 25., 250.);
  
  initialParameters = { 312, 312, 0.0, 1.0, 1.0, 0.3, 61};
  doFit(outputRootFile, theCanvasTTbarRatio1->cd(3),theInputFile, "TTbar__Efficiency_CaloQuadJet30HT320", crystalBallAndErrorFunction, initialParameters, 200.,1200.);
  
  initialParameters = { 0.0, 0.7, 0.0, 1.0};
  doFit(outputRootFile, theCanvasTTbarRatio1->cd(4),theInputFile, "TTbar__Efficiency_BTagCaloDeepCSVp17Double", "pol5", initialParameters, 0.1, 1.0);
  
  initialParameters = { 29, 11.5, 0.0, 1.00, 1.3, 0.12, 9.8};
  doFit(outputRootFile, theCanvasTTbarRatio1->cd(5),theInputFile, "TTbar__Efficiency_PFCentralJetLooseIDQuad30", crystalBallFunction, initialParameters,  25., 250.);
  

  initialParameters = { 84, 13.12, 0.06, 0.99, 1.0, 3.9, 3.2};
  doFit(outputRootFile, theCanvasTTbarRatio1->cd(6),theInputFile, "TTbar__Efficiency_1PFCentralJetLooseID75", crystalBallFunction, initialParameters,  40., 500.);
  
  theCanvasTTbarRatio1->SaveAs((std::string(inputFileName.substr(0,inputFileName.length()-5) + "_" + theCanvasTTbarRatio1->GetName()) + "_Fit" + ".png").data());
  outputRootFile.WriteObject(theCanvasTTbarRatio1, theCanvasTTbarRatio1->GetName());
  delete theCanvasTTbarRatio1;
  
  TCanvas *theCanvasTTbarRatio2 = new TCanvas("TTbar_2018_2", "TTbar_2018_2", 1400, 800);
  theCanvasTTbarRatio2->DivideSquare(6,0.005,0.005);
  
  initialParameters = { 64., 32.0, 0.07, 1.0, 1.01, 0.49, 12.36};
  doFit(outputRootFile, theCanvasTTbarRatio2->cd(1),theInputFile, "TTbar__Efficiency_2PFCentralJetLooseID60", crystalBallAndErrorFunction, initialParameters, 25., 300.);

  initialParameters = {39.54, 8.7, 0.0, 1.0, 9.81, 7.492, 21.};
  doFit(outputRootFile, theCanvasTTbarRatio2->cd(2),theInputFile, "TTbar__Efficiency_3PFCentralJetLooseID45", crystalBallAndErrorFunction, initialParameters, 25., 300.);

  initialParameters = {40, 11.42, 0.15, 1.0, 1.0, 8.6, 10.0};
  doFit(outputRootFile, theCanvasTTbarRatio2->cd(3),theInputFile, "TTbar__Efficiency_4PFCentralJetLooseID40", crystalBallAndErrorFunction, initialParameters, 25., 200.);
  
  initialParameters = { 340., 73.7, 0.81, 1., 1., 2.3, 50.4 };
  doFit(outputRootFile, theCanvasTTbarRatio2->cd(4),theInputFile, "TTbar__Efficiency_PFCentralJetsLooseIDQuad30HT330", crystalBallAndErrorFunction, initialParameters, 300., 1500.);
  
  initialParameters = { 0.45,  0.765024,  1.21809e-09,  1.05882 };
  doFit(outputRootFile, theCanvasTTbarRatio2->cd(5),theInputFile, "TTbar__Efficiency_BTagPFDeepCSV4p5Triple", "pol5", initialParameters, 0.0, 1.0);
  
  theCanvasTTbarRatio2->SaveAs((std::string(inputFileName.substr(0,inputFileName.length()-5) + "_" + theCanvasTTbarRatio2->GetName()) + "_Fit" + ".png").data());
  outputRootFile.WriteObject(theCanvasTTbarRatio2, theCanvasTTbarRatio2->GetName());
  delete theCanvasTTbarRatio2;
  
  outputFile << std::endl;
  outputFile << "};" << std::endl;
  outputRootFile.Close();
  gROOT->SetBatch(false);
}

void FitTriggerEfficiency()
{
  doAllFit2018("TriggerEfficiency_BeforeFit_2018_wMatching.root");
}
