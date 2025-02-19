// -*- C++ -*-
#if !defined(massRegionHists_H)
#define massRegionHists_H

#include <iostream>
#include <TH1F.h>
#include "PhysicsTools/FWLite/interface/TFileService.h"
#include "ZZ4b/nTupleAnalysis/interface/eventData.h"
#include "ZZ4b/nTupleAnalysis/interface/eventView.h"
#include "ZZ4b/nTupleAnalysis/interface/viewHists.h"

namespace nTupleAnalysis {

  class massRegionHists {
  public:
    TFileDirectory dir;
    bool blind;
    bool debug;

    viewHists* inclusive;

    viewHists* ZHSR;
    viewHists* ZHCR;
    viewHists* ZHSB;

    viewHists* ZH;
    viewHists* ZH_SvB_high;
    viewHists* ZH_SvB_low;

    viewHists* ZZSR;
    viewHists* ZZCR;
    viewHists* ZZSB;
    viewHists* ZZ;

    viewHists* SR;
    viewHists* CR;
    viewHists* SB;
    viewHists* SCSR;

    massRegionHists(std::string, fwlite::TFileService&, bool isMC = false, bool _blind = true, bool _debug = false);
    void Fill(eventData*, std::unique_ptr<eventView>&);
    ~massRegionHists(); 

  };

}
#endif // massRegionHists_H
