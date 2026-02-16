# operational Analysis & Strategy Report
**VoltRide Optimization Project**

**Author:**  
Priyobrata Chatterjee  
Student at KIIT UNIVERSITY  
Roll NO.: 23052904

---

## 1. Introduction

The goal of this analysis was to understand why VoltRide—a well-resourced EV ride-hailing platform—is failing to complete nearly 30% of its ride requests. 

Initial reports suggested a cancellation rate of around 18-20%, attributing the problem to "range anxiety" and insufficient charging infrastructure. However, a deeper dive into the raw data revealed a different story. The actual cancellation rate is **29.6%**, and the primary drivers of failure are not physical constraints, but rather a misalignment between dispatch logic, driver incentives, and charging behavior.

This report details the audit of the data, the correction of baseline metrics, and the development of a recovery strategy based on behavioral insights.

---

## 2. Data Quality Audit

### The "Ghost Cancellation" Discovery
My first step was to validate the baseline metrics. I discovered a significant discrepancy between the previously reported cancellations (449) and the raw dataset.

- **Total Rides:** 2,500
- **Actual Cancellations:** 739
- **True Cancellation Rate:** 29.6%

Previous analyses had filtered out cancellations where the specific reason or attribution was missing, effectively ignoring 290 failed rides. This **40% data loss** created an overly optimistic view of the system's health. All subsequent analysis in this report uses the corrected, comprehensive baseline.

---

## 3. Analysis of Failure Modes

### 3.1 The "Kill Zone" (Battery <20%)
The data shows a catastrophic failure rate for vehicles dispatched with low battery.
- **Cancellation Rate:** 87.5% for vehicles with <20% battery.
- **Baseline:** ~25% for other groups.

**Insight:** The system is essentially functioning as a "dead car dispatcher." Assigning a ride to a vehicle with 15% battery is setting the driver up to fail. They likely accept the ride, realize they can't make it, and cancel. This is an algorithmic value failure, not a driver behavior issue.

### 3.2 The "Goldilocks" Zone (30-60% Battery)
Contrary to the "range anxiety" hypothesis, drivers with mid-level battery charge are actually the **most reliable** segment of the fleet.
- **Cancellation Rate:** ~23-25% (Lowest in the fleet).

These drivers appear to be in a "compliant middle" state: they have enough charge to work confidently but aren't fully topped up, suggesting they are focused on earning rather than positioning for charging.

### 3.3 The "Rich Car" Problem (>80% Battery)
Surprisingly, drivers with high battery charge (>80%) have a **higher cancellation rate (27.8%)** than those in the middle band.

**Hypothesis:** Cherry-Picking.
Drivers who are fully charged likely feel less pressure to accept every ride. They may be selectively cancelling short or low-value trips to wait for longer, more profitable fares. This "wealth effect" creates inefficiency at the top end of the fleet.

### 3.4 The Charging Paradox
We analyzed the impact of proximity to charging stations. Counter-intuitively, rides originating near charging stations have a slightly **higher** cancellation rate (+1.0%) than those far away.

**Implication:**
This debunks the idea that we simply need "more chargers." The problem isn't spatial; it's temporal. Drivers are congregating near chargers or trying to access them during peak hours, creating friction and unavailability precisely when demand is high.

---

## 4. Strategic Recommendations

Based on these findings, I propose a three-tiered intervention strategy.

### Tier 1: Immediate Wins (The "Stop Doing Stupid Things" Phase)
**Timeline:** Week 1  
**Cost:** $0

1. **Implement a 25% Battery Dispatch Floor:** Hard-code the dispatch logic to never assign a ride to a vehicle with less than 25% battery. This stops the "dead car dispatch" loop immediately.
2. **Fix Reporting Logic:** Permanent adoption of the full dataset for reporting to ensure we aren't blinding ourselves to 40% of our failures.

### Tier 2: Algorithmic Optimization
**Timeline:** Weeks 2-8  
**Cost:** Low (Engineering time)

1. **Prioritize the "Compliant Middle":** Adjust the dispatch weighting to favor drivers in the 30-60% battery band for standard rides. They are statistically most likely to complete the job.
2. **"Cherry-Picker" Controls:** For drivers with >80% battery, enforce stricter acceptance rules for short rides to prevent high-value asset underutilization.

### Tier 3: Behavioral Incentives
**Timeline:** Months 2-4  
**Cost:** Moderate (Incentive budget)

1. **Off-Peak Charging Bonuses:** The data shows a massive supply crunch in the morning (7-10 AM) because drivers aren't charging overnight. We need to flip the incentives: pay 3x credits for charging between 11 PM and 5 AM.
2. **Peak-Prep Protocol:** Require a minimum battery level (e.g., 60%) to log in during the morning rush, pushing the "work" of charging to the night before.

---

## 5. Conclusion

VoltRide's challenges are solvable. The high cancellation rate is not a result of market forces or weather (which we found has minimal impact), but of internal logic flaws. By aligning our dispatch algorithms with the physical reality of EV range and the economic reality of driver behavior, we can achieve our sub-15% cancellation target without capital-intensive infrastructure expansion.

**Priyobrata Chatterjee**

