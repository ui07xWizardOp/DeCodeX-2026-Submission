# Audit Summary & Key Findings
**DeCodeX 2026 Submission**

**Prepared By:**  
Priyobrata Chatterjee  
Student at KIIT UNIVERSITY  
Roll NO.: 23052904

---

## Executive Summary

This audit represents a complete re-analysis of the VoltRide operational dataset. My objective was to move beyond surface-level metrics and identify the structural reasons why 30% of rides are failing.

What I found was a system fighting itself. VoltRide has adequate resources—cars, drivers, and chargers—but uses dispatch logic that sets them up to fail. By correcting a significant data quality error (missing 40% of cancellations) and debunking the "range anxiety" myth, I have outlined a strategy to reduce cancellations by nearly 50% without buying a single new charger.

---

## core findings

### 1. The "Ghost Cancellation" Error (Data Quality)
The most critical discovery happened before the analysis even began. Previous automated reports flagged ~450 cancellations. A manual audit of the raw data revealed 739 actual cancellations.

**The Reality:**
- **29.6% Cancellation Rate** (not the previously reported 18%)
- **40% Data Loss** in prior reporting due to attribution filtering errors.

We cannot fix what we cannot measure. This report uses the corrected, fully validated baseline.

### 2. The "Kill Zone" (Operational Failure)
The single biggest source of failure is the dispatch algorithm itself.
- **Fact:** 87.5% of rides dispatched to cars with <20% battery are cancelled.
- **Implication:** The system is assigning trips to vehicles that physically cannot complete them.
- **Fix:** A hard block on dispatching any vehicle below 25% battery. This single change saves 60-80 rides per month immediately.

### 3. The "Goldilocks" Driver
Conventional wisdom suggests drivers get "range anxiety" as their battery drops. The data proves the opposite.
- **<30% Battery:** High cancellation (fear of running out).
- **>80% Battery:** High cancellation (selective/cherry-picking).
- **30-60% Battery:** **The Risk Trough.** These drivers are the most reliable.

**Insight:** We should prioritize dispatching to this "compliant middle" group. They are hungry enough to work but charged enough to finish the job.

### 4. The Charging Paradox
One of the most counter-intuitive findings is that **proximity to charging stations actually increases cancellation rates** (+1.0%).

This suggests the problem isn't *where* the chargers are, but *when* drivers use them. Drivers are ignoring overnight charging to chase evening surge pricing, leading to a massive supply crunch (and cancellation spike) during the morning rush. Adding more chargers won't fix this; fixing the incentives will.

---

## Consolidated Recommendations

My strategy focuses on high-leverage, low-cost interventions first.

### Phase 1: Immediate Correction (Week 1)
**Action:** Implement a 25% Battery Dispatch Floor.
- **Cost:** $0
- **Impact:** Reduces cancellations by 8-10%.
- **Rationale:** Stops the system from dispatching "dead" cars.

### Phase 2: Algorithmic Optimization (Weeks 2-8)
**Action:** Prioritize the "Goldilocks" drivers (30-60% battery) for standard trips.
- **Cost:** Low (Development time).
- **Impact:** Improves completion rate by another 3-5%.
- **Rationale:** Allocates work to the most reliable driver segment.

### Phase 3: Behavioral Economics (Months 2-4)
**Action:** Launch "Off-Peak Charging" incentives (3x credits for overnight/mid-day charging).
- **Cost:** ~$20k/month (marketing/credits).
- **Impact:** Solves the morning supply crisis.
- **Rationale:** Shifts charging behavior away from peak demand hours.

---

## Financial Impact

Implementing this plan is projected to recover approximately **$112,500 in annual revenue**.

- **ROI (Year 1):** 150-250%
- **Payback Period:** <6 months

Most importantly, the first 10% improvement costs absolutely nothing.

---

## Conclusion

VoltRide's operational crisis isn't about a lack of infrastructure; it's about a lack of logic. By aligning dispatch algorithms with physical realities and driver psychology, we can cut cancellations in half.

This analysis is ready for immediate review and implementation.

**Priyobrata Chatterjee**  
*KIIT University*
