# K6 Performance Testing Examples

This directory contains example k6 test scripts, architecture profiles, and analysis reports demonstrating the k6-tester agent capabilities.

## Contents

- **architecture-qa-vs-prod.yaml** - Sample architecture profile showing QA and Production environments
- **api-only-test.js** - Simple API endpoint testing (isolated)
- **e2e-test.js** - End-to-end testing with async flow validation
- **analysis-report-example.md** - Sample extrapolation and cost analysis report

## Quick Start

### 1. Analyze Your Architecture

```bash
# In OpenCode
/perf analyze

# Or provide architecture description
@k6-tester "Analyze this architecture: API on EKS (4 CPU, 2GB, 2 pods prod / 1 CPU, 512MB, 1 pod QA) 
→ SQS → Lambda → RDS PostgreSQL. Target 2,000 RPS in production."
```

### 2. Generate Test Script

```bash
/perf create --target-rps 2000

# Or with specific patterns
/perf create --pattern baseline,ramp,spike
```

### 3. Run Test

```bash
# Set environment variables
export API_BASE_URL="https://api-qa.example.com"
export API_TOKEN="your-token-here"
export ENVIRONMENT="qa"

# Run test with JSON output
k6 run api-only-test.js --out json=results.json

# Or use Docker (portable)
docker run --rm -i \
  -e API_BASE_URL=$API_BASE_URL \
  -e API_TOKEN=$API_TOKEN \
  grafana/k6 run - <api-only-test.js --out json=results.json
```

### 4. Analyze Results

```bash
# In OpenCode
/perf analyze-results results.json

# Agent will provide:
# - QA test results summary
# - Production capacity extrapolation
# - Bottleneck analysis
# - Cost modeling for scaling scenarios
# - Prioritized recommendations
```

## Architecture Profile Example

The `architecture-qa-vs-prod.yaml` demonstrates:

- Component definitions (API, SQS, Lambda, RDS)
- Resource specifications (QA vs Production)
- Dependency mapping
- Performance characteristics
- Extrapolation formulas
- Cost modeling data

**Usage:**
```bash
# Generate test from architecture profile
/perf create --arch architecture-qa-vs-prod.yaml

# Analyze results with profile
/perf analyze-results results.json --arch architecture-qa-vs-prod.yaml
```

## Test Scripts

### api-only-test.js

Isolated API endpoint testing:
- Tests API without downstream dependencies
- Multiple load patterns: baseline, ramp-up, spike
- Appropriate thresholds (p95, p99, error rate)
- Extrapolation metadata embedded
- ~30 minute test duration

**Scenarios:**
1. Baseline: 50% of QA target for 5 minutes
2. Ramp-up: Gradually increase to 150% of target
3. Spike: 3x burst for 30 seconds

**Run:**
```bash
k6 run api-only-test.js --out json=results.json
```

### e2e-test.js

End-to-end workflow testing:
- Tests full flow: API → SQS → Lambda → DB
- Includes CloudWatch monitoring instructions
- Validates async processing
- Longer think time (realistic user behavior)
- ~45 minute test duration

**Validation Steps:**
1. k6 tests API endpoints
2. Manually check SQS queue depth (should return to ~0)
3. Verify Lambda invocations match API requests
4. Check DB write metrics in CloudWatch

**Run:**
```bash
k6 run e2e-test.js --out json=results.json

# Monitor during test
./cloudwatch-monitor.sh  # Generated with test script
```

## Analysis Report Example

The `analysis-report-example.md` shows a complete analysis including:

### Executive Summary
- Test results overview
- Production capacity estimate
- Confidence level
- Critical recommendations

### Detailed Analysis
- Threshold compliance
- Bottleneck identification (DB connections, Lambda concurrency, etc.)
- Extrapolation methodology with formulas
- Reality adjustments (cold starts, network latency)

### Cost Modeling
- Current infrastructure costs
- Scaling scenarios (2x, 3x, 5x load)
- Optimization opportunities
- Cost per RPS analysis

### Recommendations
- Prioritized action items (Critical → Medium → Low)
- Implementation timelines
- Cost-benefit analysis

## Extrapolation Methodology

All examples use the multi-factor scaling formula:

```
Production Capacity = QA Capacity × CPU Factor × Replica Factor × Efficiency × Reality Factor

Where:
- CPU Factor = (Prod CPU / QA CPU) × 0.85 (15% multi-core overhead)
- Replica Factor = (Prod Replicas / QA Replicas) × 0.90 (10% LB overhead)
- Efficiency = Target CPU% / Observed CPU%
- Reality Factor = 1.25 (cold starts, network improvements)

Example:
QA: 250 RPS @ 78% CPU (1 vCPU, 1 pod)
Prod: ? RPS @ 60% CPU (4 vCPU, 2 pods)

Calculation:
- CPU: (4/1) × 0.85 = 3.4x
- Replicas: (2/1) × 0.90 = 1.8x
- Efficiency: 60/78 = 0.77x
- Base: 250 × 3.4 × 1.8 × 0.77 = 1,177 RPS
- Reality: 1,177 × 1.25 = 1,471 RPS

Confidence: 75%
```

## Load Pattern Reference

### Constant Load (Baseline)
```javascript
{
  executor: 'constant-arrival-rate',
  rate: 147,  // 50% of QA target
  timeUnit: '1s',
  duration: '5m',
}
```
**Purpose:** Establish baseline performance

### Ramping VUs (Capacity)
```javascript
{
  executor: 'ramping-vus',
  stages: [
    { duration: '2m', target: 50 },
    { duration: '5m', target: 50 },
    { duration: '2m', target: 100 },
    { duration: '5m', target: 100 },
  ],
}
```
**Purpose:** Find capacity limits

### Spike Test (Bursts)
```javascript
{
  executor: 'ramping-arrival-rate',
  stages: [
    { duration: '2m', target: 147 },   // Normal
    { duration: '30s', target: 882 },  // 6x spike
    { duration: '2m', target: 147 },   // Return
  ],
}
```
**Purpose:** Handle traffic bursts (Black Friday)

### Stress Test (Breaking Point)
```javascript
{
  executor: 'ramping-arrival-rate',
  stages: [
    { duration: '5m', target: 294 },   // Target load
    { duration: '5m', target: 441 },   // 150%
    { duration: '5m', target: 588 },   // 200%
  ],
}
```
**Purpose:** Find breaking point

### Soak Test (Stability)
```javascript
{
  executor: 'constant-arrival-rate',
  rate: 176,  // 60% of target
  duration: '12h',
}
```
**Purpose:** Detect memory leaks

## Threshold Reference

### API Endpoints (Default)
```javascript
thresholds: {
  'http_req_duration': ['p(95)<500', 'p(99)<1000'],
  'http_req_failed': ['rate<0.001'],  // 99.9% success
  'http_reqs': ['rate>100'],
}
```

### Read-Heavy Endpoints
```javascript
thresholds: {
  'http_req_duration': ['p(95)<200', 'p(99)<500'],
  'http_req_failed': ['rate<0.0001'],  // 99.99% success
}
```

### Write-Heavy Endpoints
```javascript
thresholds: {
  'http_req_duration': ['p(95)<800', 'p(99)<1500'],
  'http_req_failed': ['rate<0.002'],  // 99.8% success
}
```

## CloudWatch Monitoring

### Key Metrics to Watch

**EKS Pods:**
```bash
# CPU Utilization (target: <80%)
aws cloudwatch get-metric-statistics \
  --namespace AWS/EKS \
  --metric-name pod_cpu_utilization \
  --dimensions Name=ClusterName,Value=your-cluster
```

**SQS Queue:**
```bash
# Queue depth (should return to ~0 after test)
aws sqs get-queue-attributes \
  --queue-url https://sqs.us-east-1.amazonaws.com/123456789/orders \
  --attribute-names ApproximateNumberOfMessagesVisible
```

**Lambda:**
```bash
# Invocations (should match API requests)
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Invocations \
  --dimensions Name=FunctionName,Value=order-processor
```

**RDS:**
```bash
# Database connections (critical!)
aws cloudwatch get-metric-statistics \
  --namespace AWS/RDS \
  --metric-name DatabaseConnections \
  --dimensions Name=DBInstanceIdentifier,Value=your-db
```

## Cost Estimation Reference

### AWS Pricing (Approximate, US-East-1)

| Service | Unit | Price |
|---------|------|-------|
| **EKS (compute)** | vCPU/hour | $0.05 |
| **RDS db.t3.large** | hour | $0.166 |
| **RDS db.r5.xlarge** | hour | $0.625 |
| **RDS Proxy** | hour | $0.015 |
| **Lambda** | GB-second | $0.0000166667 |
| **SQS Standard** | million requests | $0.40 (after 1M free) |
| **SNS** | million notifications | $0.50 (after 1M free) |

### Example: 1,000 RPS Sustained

```
EKS: 8 vCPU × $0.05 × 720h = $288/month
RDS: $0.166 × 720h = $120/month
Lambda: 26M invocations × 5s × 1GB × $0.0000166667 = $36/month
SQS: 26M requests × $0.40/million = $10/month
SNS: 26M notifications × $0.50/million = $13/month

Total: ~$467/month
```

## Troubleshooting

### Test Fails Immediately
```bash
# Check health endpoint
curl https://api-qa.example.com/health

# Verify authentication
curl -H "Authorization: Bearer $API_TOKEN" https://api-qa.example.com/health
```

### High Error Rate
- Reduce load (lower RPS target)
- Check application logs
- Verify database connection pool not exhausted
- Check for rate limiting

### Results Not Matching Thresholds
- Increase test duration (warm up period)
- Check for external factors (other tests running)
- Verify QA environment is properly sized
- Review CloudWatch for resource constraints

### Extrapolation Seems Off
- Validate architecture profile accuracy
- Check reality adjustments (cold starts, network)
- Compare with historical production data
- Run shadow traffic test for validation

## Best Practices

1. **Always analyze architecture first** - Use `/perf analyze` before testing
2. **Start with baseline** - Don't jump straight to stress testing
3. **Monitor CloudWatch during tests** - Validates assumptions
4. **Save all results** - Compare over time
5. **Run soak tests separately** - 12-hour tests need dedicated time
6. **Validate extrapolations** - Use shadow traffic when possible
7. **Implement critical recommendations** - RDS Proxy, concurrency limits
8. **Document assumptions** - Reality factors should be explained
9. **Test regularly** - Catch performance regressions early
10. **Gradual production rollout** - 10% → 50% → 100%

## Related Resources

- k6 Documentation: https://k6.io/docs/
- AWS CloudWatch Metrics: https://docs.aws.amazon.com/cloudwatch/
- Performance Testing Best Practices: https://k6.io/docs/testing-guides/
- k6-tester Agent: `.opencode/agent/k6-tester.md`
- Skills:
  - architecture-analyzer: `.opencode/skill/architecture-analyzer/SKILL.md`
  - performance-test: `.opencode/skill/performance-test/SKILL.md`
  - analyze-k6-results: `.opencode/skill/analyze-k6-results/SKILL.md`

## Getting Help

```bash
# In OpenCode
@k6-tester "I need help with [your question]"

# Or use /perf commands
/perf analyze     # Architecture analysis
/perf create      # Generate test script
/perf results     # Analyze results
/perf estimate    # Cost estimation
```

## Contributing

When adding new examples:
1. Include architecture profile
2. Document load patterns used
3. Provide expected results
4. Include cost analysis
5. Add troubleshooting tips
6. Reference confidence levels

## License

MIT License - Same as OpenCode.Personal repository
