---
name: analyze-k6-results
description: Analyze k6 test results with production extrapolation and cost modeling
license: MIT
compatibility: opencode
metadata:
  audience: developers
  workflow: performance-testing
---

## What I Do

Analyze k6 performance test results, extrapolate QA findings to production capacity, identify bottlenecks, and provide cost-performance recommendations with reality checks.

## Input Requirements

### 1. k6 Results (Required)
Accept multiple formats:

**JSON Output:**
```bash
k6 run test.js --out json=results.json
```

**Summary Export:**
```bash
k6 run test.js --summary-export=summary.json
```

**Text Summary:**
```
Copy-paste k6 terminal output
```

### 2. Architecture Profile (Recommended)
From `architecture-analyzer` skill or manual input:
- Component specifications
- Resource ratios (QA vs Prod)
- Extrapolation factors
- Known bottlenecks

### 3. CloudWatch Metrics (Optional but valuable)
- EKS: CPU, Memory utilization
- SQS: Queue depth, message throughput
- Lambda: Invocations, duration, errors
- RDS: Connections, latency, IOPS

## Analysis Components

### 1. Result Parsing

Extract key metrics from k6 output:

```javascript
{
  "metrics": {
    // HTTP Request metrics
    "http_reqs": {
      "count": 15000,
      "rate": 250.0        // RPS achieved
    },
    
    // Response time metrics
    "http_req_duration": {
      "avg": 234.5,
      "min": 87.2,
      "med": 198.4,
      "max": 1523.7,
      "p90": 389.2,
      "p95": 456.3,
      "p99": 789.1,
      "p99.9": 1201.4
    },
    
    // Error metrics
    "http_req_failed": {
      "rate": 0.0005,      // 0.05% error rate
      "count": 8,
      "total": 15000
    },
    
    // Data transfer
    "data_received": {
      "count": 45000000    // 45 MB
    },
    
    // Virtual users
    "vus_max": 100
  },
  
  "root_group": {
    "checks": {
      "passes": 14992,
      "fails": 8
    }
  }
}
```

### 2. Threshold Compliance Check

```markdown
## Threshold Analysis

| Threshold | Target | Actual | Status | Margin |
|-----------|--------|--------|--------|--------|
| p95 < 500ms | 500ms | 456ms | ✅ Pass | 44ms (9%) |
| p99 < 1000ms | 1000ms | 789ms | ✅ Pass | 211ms (21%) |
| Error rate < 0.1% | 0.1% | 0.05% | ✅ Pass | 0.05% (50%) |
| Throughput > 100 RPS | 100 RPS | 250 RPS | ✅ Pass | 150 RPS (150%) |

**Overall:** ✅ All thresholds passed

**Concerns:**
- p99 latency is 79% of threshold (close to limit)
- Consider improving if production needs headroom
```

### 3. Production Extrapolation

Apply multi-factor scaling formula:

```
Step 1: Base Scaling
-------
QA Results: 250 RPS @ 78% CPU
Resources: 1 vCPU, 512MB, 1 pod

Production Resources: 4 vCPU, 2GB, 2 pods
CPU Factor: (4/1) × 0.85 = 3.4x
Replica Factor: (2/1) × 0.90 = 1.8x
Combined: 3.4 × 1.8 = 6.12x

Step 2: CPU Target Adjustment
-------
QA CPU: 78%
Target Prod CPU: 60% (leave 40% headroom)
Adjustment: 60 / 78 = 0.77x

Base Capacity: 250 × 6.12 × 0.77 = 1,177 RPS

Step 3: Reality Adjustments
-------
Cold Starts: QA 15% → Prod 2% = +13%
Network: QA 5ms → Prod 1ms = +10%  
Resources: Shared → Dedicated = +5%
Combined Reality Factor: 1.25x

Final Estimate: 1,177 × 1.25 = 1,471 RPS

Step 4: Latency Extrapolation
-------
QA p95: 456ms
Production p95: 456ms × (1 / 1.25) = 365ms
(Faster due to warm pods, better network)

Confidence: 75%
- Based on linear scaling assumptions
- Needs validation with production traffic
- Database connections may be limiting factor
```

### 4. Bottleneck Identification

#### Database Connection Analysis
```markdown
### 🔴 Critical: Database Connections

**QA Observations:**
- Connections: 48 average, 67 peak
- RPS: 250
- Ratio: 0.19 connections per RPS

**Production Extrapolation:**
- At 1,471 RPS: 0.19 × 1,471 = 280 connections
- RDS Limit (db.t3.large): 100 connections
- **Bottleneck at:** 100 / 0.19 = 526 RPS in QA
- **Production equivalent:** 526 × 6.12 × 1.25 = 4,022 RPS

**Risk Level:** 🔴 Critical
- Current target: 1,471 RPS
- Bottleneck: 4,022 RPS
- Headroom: 2.7x (acceptable but monitor closely)

**If Target Increases to 5,000 RPS:**
- Required connections: 653
- **Will fail - requires solution**

**Solutions:**
1. RDS Proxy (Recommended)
   - Cost: $0.015/hour = $11/month
   - Benefit: 10,000+ connections via pooling
   - Implementation: 1 day
   - Risk: None

2. Application Connection Pooling
   - Cost: Free
   - Benefit: Reduce ratio to ~0.05 per RPS
   - Implementation: 3 days development
   - Risk: Code complexity

3. Upgrade RDS Instance
   - Cost: db.r5.xlarge = $450/month (vs $120 current)
   - Benefit: 500 max_connections
   - Implementation: 2 hours (with downtime)
   - Risk: Expensive

**Recommendation:** Implement RDS Proxy before production
```

#### Lambda Concurrency Analysis
```markdown
### 🟡 Medium: Lambda Concurrency

**QA Observations:**
- Peak concurrent: 45 executions
- RPS: 250
- Avg duration: 5.1 seconds
- Ratio: 0.18 concurrent per RPS

**Production Extrapolation:**
- At 1,471 RPS: 0.18 × 1,471 = 265 concurrent
- Default Limit: 1,000
- Headroom: 735 (73.5%)

**Risk Level:** 🟡 Medium
- Adequate for current target
- May need increase for 3x growth

**Recommendation:**
- Request increase to 3,000 (free, takes 2-3 days)
- Monitor concurrent executions in CloudWatch
```

#### SQS Throughput Analysis
```markdown
### 🟢 Low: SQS Throughput

**QA Observations:**
- Messages: 15,023 (matches API requests ✅)
- Peak rate: 250 messages/sec
- Max queue depth: 147 messages

**Production Extrapolation:**
- At 1,471 RPS: 1,471 messages/sec
- Soft Limit: 300 messages/sec per queue
- **Will exceed at 5x QA load**

**Risk Level:** 🟢 Low
- SQS can burst above soft limits
- Rarely the bottleneck
- Can add multiple queues if needed

**Optimization (Optional):**
- Batch 10 orders per message
- Reduces to 147 messages/sec
- Saves ~$32/month in SQS costs
- Implementation: 2 days
```

### 5. Cost Analysis

#### Current Production Cost (Estimated)

```markdown
## Cost Breakdown

### Infrastructure (EKS)
- Configuration: 2 pods × (4 vCPU, 2GB RAM)
- Total: 8 vCPU, 4GB RAM
- Pricing: $0.05/vCPU/hour
- Calculation: 8 × $0.05 × 720 hours
- **Monthly Cost: $288**

### RDS PostgreSQL
- Instance: db.t3.large (2 vCPU, 8GB RAM)
- Pricing: $0.166/hour
- Calculation: $0.166 × 720 hours
- **Monthly Cost: $120**

### Lambda Functions
- Invocations: 30M/month (1,000 RPS avg × 86,400 sec/day × 30 days)
- Configuration: 1GB RAM, 5 sec avg duration
- GB-seconds: 30M × 5 × 1 = 150M GB-seconds
- Pricing: $0.0000166667/GB-second
- Calculation: 150M × $0.0000166667
- **Monthly Cost: $41**

### SQS Standard
- Requests: 30M/month
- Free tier: 1M requests
- Billable: 29M requests
- Pricing: $0.40 per million
- Calculation: 29 × $0.40
- **Monthly Cost: $12**

### SNS Standard
- Notifications: 30M/month
- Free tier: 1M notifications
- Billable: 29M notifications
- Pricing: $0.50 per million
- Calculation: 29 × $0.50
- **Monthly Cost: $15**

### Data Transfer
- Estimated: $50/month
- (Based on avg request/response size and traffic)

---

**TOTAL CURRENT COST: $526/month**
(At ~1,000 RPS average, 1,471 RPS capacity)
```

#### Scaling Scenarios

```markdown
## Scenario 1: Target 3,000 RPS (2x Current Capacity)

### Required Changes

**EKS Pods:**
- Current: 2 pods (8 vCPU total)
- Required: 5 pods (20 vCPU total)
- Cost: 20 × $0.05 × 720 = **$720/month** (+$432)

**RDS PostgreSQL:**
- Current: db.t3.large (limited connections)
- Required: db.r5.xlarge (4 vCPU, 32GB, 500 connections)
- Cost: $0.625/hour × 720 = **$450/month** (+$330)
- Alternative: Keep db.t3.large + RDS Proxy = $120 + $11 = **$131/month** (-$319 vs upgrade)

**RDS Proxy:** (REQUIRED if keeping db.t3.large)
- Cost: $0.015/hour × 720 = **$11/month** (+$11)

**Lambda:**
- Invocations: 90M/month
- GB-seconds: 450M
- Cost: **$123/month** (+$82)

**SQS:**
- Requests: 90M/month
- Cost: 89 × $0.40 = **$36/month** (+$24)

**SNS:**
- Notifications: 90M/month
- Cost: 89 × $0.50 = **$45/month** (+$30)

**Data Transfer:**
- Estimated: **$150/month** (+$100)

---

**Option A: Upgrade RDS**
- Total: $720 + $450 + $123 + $36 + $45 + $150 = **$1,524/month**
- Increase: +$998 (190% of current)
- Cost per RPS: $0.508

**Option B: RDS Proxy (Recommended)**
- Total: $720 + $131 + $123 + $36 + $45 + $150 = **$1,205/month**
- Increase: +$679 (129% of current)
- Cost per RPS: $0.402
- **Savings: $319/month vs Option A**

---

## Scenario 2: Target 5,000 RPS (3.4x Current Capacity)

### Required Changes

**EKS Pods:**
- Required: 8 pods (32 vCPU total)
- Cost: **$1,152/month**

**RDS PostgreSQL:**
- Required: db.r5.2xlarge (8 vCPU, 64GB, 1000 connections)
- Cost: $1.25/hour × 720 = **$900/month**
- With RDS Proxy: Still beneficial for connection pooling

**RDS Proxy:**
- Cost: **$11/month** (enables better connection management)

**Lambda:**
- Invocations: 150M/month
- Cost: **$205/month**

**SQS:**
- Requests: 150M/month
- With batching (10x): 15M requests
- Cost: 14 × $0.40 = **$6/month** (with optimization)
- Without batching: **$60/month**

**SNS:**
- Notifications: 150M/month
- Cost: **$75/month**

**Data Transfer:**
- Estimated: **$250/month**

---

**Total: $1,152 + $900 + $11 + $205 + $60 + $75 + $250 = $2,653/month**
- With SQS batching: **$2,599/month**
- Increase: +$2,073 (394% of current)
- Cost per RPS: $0.520

**Bottleneck Check:**
- Database: 1000 connections × 5.26 RPS/conn = 5,263 RPS capacity ✅
- Lambda: 3,000 concurrent limit → ~15,000 RPS capacity ✅
- SQS: Multiple queues or batching needed ✅
```

#### Cost Optimization Strategies

```markdown
## Optimization 1: SQS Message Batching

**Change:** Send 10 orders per SQS message instead of 1

**Benefits:**
- Messages: 150M → 15M (-90%)
- Cost savings: $60 → $6 per month (-$54)
- Lambda invocations: 150M → 15M (-90%)
- Lambda cost savings: $205 → $21 (-$184)
- **Total Savings: $238/month**

**Trade-offs:**
- Requires application code changes (2 days dev)
- Batch processing logic needed
- Slightly higher latency per message
- More complex error handling

**Recommendation:** Implement when cost becomes concern (>$1,500/month)

---

## Optimization 2: EKS Spot Instances

**Change:** Use 50% spot, 50% on-demand for EKS nodes

**Benefits:**
- Current: $1,152 on-demand
- With spot: ($1,152 × 0.5 × 0.3) + ($1,152 × 0.5) = $173 + $576 = $749
- **Savings: $403/month** (35%)

**Trade-offs:**
- Spot interruptions (mitigated by 50/50 mix)
- Requires configuration and monitoring
- May impact reliability slightly

**Recommendation:** Use for non-critical workloads or with proper fallback

---

## Optimization 3: Lambda Reserved Concurrency

**Change:** Provision 500 Lambda instances (reserved concurrency)

**Benefits:**
- Eliminates cold starts
- Improves p95 latency by ~15-20%
- More predictable performance
- Cost: Same (pay for what you use)

**Trade-offs:**
- Reserves capacity (can't be used by other functions)
- Requires capacity planning

**Recommendation:** Implement for production consistency

---

## Optimization 4: Aurora Serverless v2 (Alternative to RDS)

**Change:** Migrate from RDS PostgreSQL to Aurora Serverless v2

**Benefits:**
- Auto-scales with load (0.5 - 128 ACUs)
- No manual instance sizing
- Better high availability
- Pay only for capacity used

**At 5,000 RPS:**
- Estimated: 24 ACUs needed
- Cost: 24 × $0.12 × 720 = $2,074/month
- vs db.r5.2xlarge: $900/month
- **Difference: +$1,174/month**

**Trade-offs:**
- More expensive at constant load
- Cost-effective for bursty traffic
- Reduces operational overhead
- Slight latency overhead (milliseconds)

**Recommendation:** Use if traffic is highly variable (10x burst patterns)
```

### 6. Reality Checks & Caveats

```markdown
## Important Considerations

### Test Environment Limitations

| Factor | Impact | Adjustment |
|--------|--------|------------|
| **Cold starts** | QA: 15% vs Prod: 2% | +13% perf in prod |
| **Network latency** | QA: 5ms vs Prod: 1ms | +10% perf in prod |
| **Shared resources** | QA database shared | +5% perf in prod |
| **Test duration** | 34 minutes (too short) | ⚠️ Need 12h soak test |
| **Synthetic load** | Constant RPS pattern | ⚠️ Real users are bursty |
| **Single region** | No multi-region latency | ⚠️ Add +50ms for global |

### Production Reality

**✅ Positive Factors:**
- Warmed pods (HPA pre-scales before load)
- Dedicated RDS instance (no contention)
- Better network (same VPC, AZ affinity)
- Production-grade infrastructure

**⚠️ Risk Factors:**
- Real user behavior is unpredictable
- Peak traffic can be 5-10x average
- Deploy events cause temporary cold starts
- Cascading failures (one component affects others)
- Database migrations during deployment

### Confidence Levels

| Metric | Estimate | Confidence | Reason |
|--------|----------|------------|---------|
| **Throughput** | 1,471 RPS | 75% | Linear scaling assumption |
| **Latency** | 365ms p95 | 80% | Historical data matches |
| **Error rate** | 0.03% | 85% | Consistent across tests |
| **DB bottleneck** | 4,022 RPS | 70% | Need connection profiling |
| **Cost** | $526/month | 90% | Based on AWS pricing |

### Validation Recommendations

1. **Shadow Traffic Testing**
   - Mirror 10% of production traffic to staging
   - Compare actual vs predicted performance
   - Adjust extrapolation factors

2. **12-Hour Soak Test**
   - Run at 60-70% of capacity
   - Monitor for memory leaks
   - Check connection stability
   - Validate no gradual degradation

3. **Gradual Production Rollout**
   - Deploy to 10% of users
   - Monitor for 24 hours
   - Increase to 50%
   - Monitor for 48 hours
   - Full rollout if metrics match predictions

4. **Chaos Engineering**
   - Simulate Lambda failures
   - Test database failover
   - Verify queue backlog handling
   - Measure recovery time
```

## Output Formats

### 1. Markdown Report (Human-Readable)

```markdown
# Performance Test Analysis Report
Date: 2026-01-16
Environment: QA
Test Duration: 34 minutes

## Executive Summary
✅ System can handle production targets with current architecture
⚠️ Database connection pooling (RDS Proxy) is critical

[Full analysis with all sections above]
```

### 2. JSON Data (Machine-Readable)

```json
{
  "test_metadata": {
    "environment": "qa",
    "date": "2026-01-16",
    "duration_minutes": 34
  },
  "qa_results": {
    "throughput_rps": 250,
    "p95_latency_ms": 456,
    "p99_latency_ms": 789,
    "error_rate": 0.0005
  },
  "production_extrapolation": {
    "estimated_rps": 1471,
    "confidence": 0.75,
    "extrapolation_factor": 6.8,
    "reality_adjustment": 1.25,
    "p95_latency_ms": 365,
    "error_rate": 0.0003
  },
  "bottlenecks": [
    {
      "component": "rds-postgres",
      "type": "database_connections",
      "severity": "critical",
      "limit": 100,
      "expected_usage": 280,
      "breaking_point_rps": 4022,
      "solution": "RDS Proxy ($11/month)"
    }
  ],
  "cost_analysis": {
    "current_monthly_usd": 526,
    "scenarios": {
      "3000_rps": { "cost": 1205, "with_optimizations": true },
      "5000_rps": { "cost": 2599, "with_optimizations": true }
    }
  },
  "recommendations": [
    {
      "priority": "critical",
      "title": "Implement RDS Proxy",
      "cost": 11,
      "timeline_days": 1
    }
  ]
}
```

## Best Practices

### Analysis Quality
- ✅ Parse both text and JSON k6 output
- ✅ Cross-reference CloudWatch metrics
- ✅ Apply reality adjustments (don't use raw extrapolation)
- ✅ State confidence levels clearly
- ✅ Provide multiple cost scenarios

### Recommendations
- ✅ Prioritize by severity (Critical → Warning → Info)
- ✅ Include implementation timeline
- ✅ Provide specific solutions with code/config
- ✅ Consider trade-offs (cost vs performance vs complexity)

### Communication
- ✅ Executive summary at top
- ✅ Visual indicators (✅ ⚠️ 🔴 🟡 🟢)
- ✅ Both technical details and business impact
- ✅ Actionable next steps

## Integration with Other Skills

1. **architecture-analyzer** → Provides baseline profile
2. **performance-test** → Generates tests that produce results
3. **analyze-k6-results** (this skill) → Analyzes and extrapolates
4. **Cost estimation** → Used for scaling decisions

## When to Use

- ✅ After k6 test completes
- ✅ Before production deployment
- ✅ When planning capacity increases
- ✅ After infrastructure changes
- ✅ Regular performance reviews

## Output Files

Generated artifacts:
- `analysis-report.md` - Full human-readable report
- `metrics.json` - Structured data for dashboards
- `recommendations.md` - Prioritized action items
- `cost-scenarios.csv` - Spreadsheet for budgeting
