#include "ZZ4b/nTupleAnalysis/interface/massRegionHists.h"

using namespace nTupleAnalysis;

massRegionHists::massRegionHists(std::string name, fwlite::TFileService& fs, bool isMC, bool _blind, bool _debug) {
  dir = fs.mkdir(name);
  blind = _blind;
  debug = _debug;

  inclusive = new viewHists(name+"/inclusive", fs, isMC, debug);

  ZHSR      = new viewHists(name+"/ZHSR",      fs, isMC, debug);
  ZHCR      = new viewHists(name+"/ZHCR",      fs, isMC, debug);
  ZHSB      = new viewHists(name+"/ZHSB",      fs, isMC, debug);
  ZH        = new viewHists(name+"/ZH",        fs, isMC, debug);

  ZH_SvB_high = new viewHists(name+"/ZH_SvB_high", fs, isMC, debug);
  ZH_SvB_low  = new viewHists(name+"/ZH_SvB_low",  fs, isMC, debug);

  ZZSR      = new viewHists(name+"/ZZSR",      fs, isMC, debug);
  ZZCR      = new viewHists(name+"/ZZCR",      fs, isMC, debug);
  ZZSB      = new viewHists(name+"/ZZSB",      fs, isMC, debug);
  ZZ        = new viewHists(name+"/ZZ",        fs, isMC, debug);

  SR = new viewHists(name+"/SR", fs, isMC, debug);
  CR = new viewHists(name+"/CR", fs, isMC, debug);
  SB = new viewHists(name+"/SB", fs, isMC, debug);
  SCSR = new viewHists(name+"/SCSR", fs, isMC, debug);

} 

void massRegionHists::Fill(eventData* event, std::unique_ptr<eventView> &view){
  if(blind && (view->ZZSR || view->ZHSR || view->HHSR)) return;
  
  inclusive->Fill(event, view);

  if(view->ZHSR) ZHSR->Fill(event, view);
  if(view->ZHCR) ZHCR->Fill(event, view);
  if(view->ZHSB) ZHSB->Fill(event, view);

  if(view->ZHSB || view->ZHCR || view->ZHSR){
    ZH->Fill(event, view);
    if(event->ZHvB > 0.5)
      ZH_SvB_high->Fill(event, view);
    else
      ZH_SvB_low ->Fill(event, view);
  }

  if(view->ZZSR) ZZSR->Fill(event, view);
  if(view->ZZCR) ZZCR->Fill(event, view);
  if(view->ZZSB) ZZSB->Fill(event, view);
  if(view->ZZSB || view->ZZCR || view->ZZSR){
    ZZ->Fill(event, view);
  }

  if(view->SR) SR->Fill(event, view);
  if(view->CR) CR->Fill(event, view);
  if(view->SB) SB->Fill(event, view);
  if(view->SB || view->CR || view->SR) SCSR->Fill(event, view);

  return;
}

massRegionHists::~massRegionHists(){} 


