---
name: performance-test
description: Generate k6 performance test scripts with load patterns and extrapolation
license: MIT
compatibility: opencode
metadata:
  audience: developers
  workflow: performance-testing
---

## What I Do

Generate production-ready k6 test scripts with appropriate load patterns, thresholds, and extrapolation logic. Create portable scripts that run anywhere: local machines, CI/CD pipelines, or cloud instances.

## Input Requirements

### 1. Architecture Profile (Required)
From `architecture-analyzer` skill or provided manually:
```yaml
architecture:
  components: [...]
  extrapolation:
    factors: { combined: 6.8 }
  targets:
    production: { avg_rps: 1000 }
    qa_equivalent: { avg_rps: 147 }
```

### 2. Test Objectives
- **Baseline:** Establish baseline performance
- **Capacity:** Find breaking point
- **Spike:** Handle traffic bursts
- **Stress:** Push beyond limits
- **Soak:** Detect memory leaks (12+ hours)
- **All:** Comprehensive test suite

### 3. Target Environment
- **QA:** Generate load for QA environment (calculated from production target)
- **Production:** Generate load for production (use with caution!)
- **Staging:** Generate load for staging (similar to production)

### 4. API Details
- **Base URL:** API endpoint (or use env var)
- **Authentication:** Token, API key, or OAuth
- **Endpoints:** Which endpoints to test
- **Payload:** Request body structure

## Load Patterns

### 1. Constant Load (Baseline)
```javascript
{
  executor: 'constant-vus',
  vus: 30,              // Fixed virtual users
  duration: '5m',        // 5 minutes
}
```
**Use for:** Establishing baseline, measuring steady-state performance

### 2. Ramping VUs (Capacity Finding)
```javascript
{
  executor: 'ramping-vus',
  startVUs: 0,
  stages: [
    { duration: '2m', target: 50 },   // Ramp up
    { duration: '5m', target: 50 },   // Sustain
    { duration: '2m', target: 100 },  // Increase
    { duration: '5m', target: 100 },  // Sustain
    { duration: '2m', target: 0 },    // Ramp down
  ],
}
```
**Use for:** Finding capacity limits, observing graceful degradation

### 3. Ramping Arrival Rate (Realistic Load)
```javascript
{
  executor: 'ramping-arrival-rate',
  startRate: 50,           // Requests per timeUnit
  timeUnit: '1s',
  preAllocatedVUs: 50,
  maxVUs: 200,
  stages: [
    { duration: '2m', target: 50 },
    { duration: '5m', target: 100 },
    { duration: '2m', target: 200 },
  ],
}
```
**Use for:** Simulating real RPS targets, stress testing

### 4. Spike Test
```javascript
{
  executor: 'ramping-arrival-rate',
  startRate: 50,
  timeUnit: '1s',
  preAllocatedVUs: 50,
  maxVUs: 300,
  stages: [
    { duration: '2m', target: 50 },    // Normal
    { duration: '30s', target: 250 },  // Sudden spike (5x)
    { duration: '2m', target: 50 },    // Return to normal
  ],
}
```
**Use for:** Black Friday scenarios, burst traffic handling

### 5. Stress Test
```javascript
{
  executor: 'ramping-arrival-rate',
  startRate: 50,
  timeUnit: '1s',
  preAllocatedVUs: 100,
  maxVUs: 500,
  stages: [
    { duration: '5m', target: 100 },   // Warm up
    { duration: '5m', target: 200 },   // Increase
    { duration: '5m', target: 300 },   // Push beyond capacity
    { duration: '5m', target: 400 },   // Break point
  ],
}
```
**Use for:** Finding breaking point, identifying first failure

### 6. Soak Test (Stability)
```javascript
{
  executor: 'constant-arrival-rate',
  rate: 100,              // 100 RPS
  timeUnit: '1s',
  duration: '12h',        // 12 hours
  preAllocatedVUs: 150,
}
```
**Use for:** Memory leaks, connection leaks, long-term stability

## Threshold Configuration

### Default Thresholds (Adjust per domain)

```javascript
thresholds: {
  // Response time (API endpoints)
  'http_req_duration': [
    'p(95)<500',      // 95th percentile under 500ms
    'p(99)<1000',     // 99th percentile under 1s
    'p(99.9)<2000',   // 99.9th percentile under 2s
  ],
  
  // Success rate (99.9% success = 0.1% error rate)
  'http_req_failed': ['rate<0.001'],
  
  // Minimum throughput (adjust per environment)
  'http_reqs': ['rate>100'],  // 100 RPS minimum
  
  // Custom metrics
  'errors': ['rate<0.001'],
  'api_response_time': ['p(95)<400'],
}
```

### SLO-Based Thresholds

```javascript
// 99.9% uptime = 43 minutes downtime per month
// Error budget: 0.1% of requests can fail
thresholds: {
  'http_req_failed': [
    'rate<0.001',                    // Error budget
    { threshold: 'rate<0.005', abortOnFail: true }, // Critical: abort if >0.5%
  ],
  'http_req_duration': [
    'p(99)<1000',                    // SLO target
    { threshold: 'p(99)<2000', abortOnFail: true }, // Critical: abort if p99>2s
  ],
}
```

## QA Load Calculation

Calculate appropriate QA load based on production targets:

```javascript
// Given:
// - Production target: 2,000 RPS
// - Extrapolation factor: 6.8x
// - Target CPU: 60%

// Step 1: Base QA target
const qaTargetRPS = 2000 / 6.8;  // = 294 RPS

// Step 2: Adjust for test type
const baseline = qaTargetRPS * 0.5;   // 50% for baseline: 147 RPS
const normal = qaTargetRPS;            // 100% for normal: 294 RPS
const stress = qaTargetRPS * 1.5;     // 150% for stress: 441 RPS
const spike = qaTargetRPS * 3;        // 300% for spike: 882 RPS

// Step 3: Calculate VUs needed
// Rule of thumb: VUs = target_RPS * avg_response_time_seconds
// Example: 294 RPS with 0.5s response = 147 VUs
const estimatedVUs = Math.ceil(normal * 0.5);  // 147 VUs
```

## Script Structure

### Complete k6 Script Template

```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate, Trend, Counter } from 'k6/metrics';

// ============================================================================
// CONFIGURATION
// ============================================================================

const CONFIG = {
  baseUrl: __ENV.API_BASE_URL || 'https://api-qa.example.com',
  authToken: __ENV.API_TOKEN || '',
  environment: __ENV.ENVIRONMENT || 'qa',
};

// ============================================================================
// EXTRAPOLATION METADATA (Embedded for reference)
// ============================================================================

export const metadata = {
  generated_by: 'k6-tester agent',
  generated_at: '2026-01-16',
  environment: 'qa',
  
  resources: {
    qa: { cpu: 1, ram_mb: 512, replicas: 1 },
    production: { cpu: 4, ram_mb: 2048, replicas: 2 },
  },
  
  extrapolation: {
    factor: 6.8,
    formula: '(4/1) * (2/1) * 0.85 * 0.90',
    reality_adjustment: 1.25,
  },
  
  targets: {
    production_rps: 2000,
    qa_equivalent_rps: 294,
  },
  
  notes: [
    'QA has ~15% cold start penalty vs production 2%',
    'QA network latency to RDS: 5ms, production: 1ms',
    'Production estimate: 294 RPS * 6.8 * 1.25 = ~2,500 RPS capacity',
  ],
};

// ============================================================================
// CUSTOM METRICS
// ============================================================================

const errorRate = new Rate('errors');
const apiDuration = new Trend('api_response_time');
const throughput = new Counter('requests_total');

// ============================================================================
// TEST SCENARIOS
// ============================================================================

export const options = {
  scenarios: {
    // Scenario 1: Baseline (Constant Load)
    baseline: {
      executor: 'constant-arrival-rate',
      rate: 147,              // 50% of QA target (294 RPS)
      timeUnit: '1s',
      duration: '5m',
      preAllocatedVUs: 100,
      maxVUs: 200,
      exec: 'testAPI',
      startTime: '0s',
      tags: { scenario: 'baseline' },
    },
    
    // Scenario 2: Ramp-up (Find Capacity)
    ramp_up: {
      executor: 'ramping-arrival-rate',
      startRate: 100,
      timeUnit: '1s',
      preAllocatedVUs: 150,
      maxVUs: 400,
      stages: [
        { duration: '2m', target: 200 },
        { duration: '5m', target: 200 },
        { duration: '2m', target: 294 },  // QA target
        { duration: '5m', target: 294 },
        { duration: '2m', target: 441 },  // 150% stress
        { duration: '3m', target: 441 },
        { duration: '2m', target: 0 },
      ],
      exec: 'testAPI',
      startTime: '6m',
      tags: { scenario: 'ramp_up' },
    },
    
    // Scenario 3: Spike (Burst Handling)
    spike: {
      executor: 'ramping-arrival-rate',
      startRate: 147,
      timeUnit: '1s',
      preAllocatedVUs: 200,
      maxVUs: 600,
      stages: [
        { duration: '2m', target: 147 },   // Normal load
        { duration: '30s', target: 882 },  // 3x spike
        { duration: '2m', target: 147 },   // Back to normal
      ],
      exec: 'testAPI',
      startTime: '28m',
      tags: { scenario: 'spike' },
    },
    
    // Scenario 4: Stress (Push Limits) - Commented out by default
    // stress: {
    //   executor: 'ramping-arrival-rate',
    //   startRate: 294,
    //   timeUnit: '1s',
    //   preAllocatedVUs: 300,
    //   maxVUs: 800,
    //   stages: [
    //     { duration: '5m', target: 294 },
    //     { duration: '5m', target: 441 },
    //     { duration: '5m', target: 588 },  // 200% of target
    //   ],
    //   exec: 'testAPI',
    //   startTime: '34m',
    //   tags: { scenario: 'stress' },
    // },
    
    // Scenario 5: Soak (12-hour stability) - Run separately
    // soak: {
    //   executor: 'constant-arrival-rate',
    //   rate: 176,  // 60% of QA target for stability
    //   timeUnit: '1s',
    //   duration: '12h',
    //   preAllocatedVUs: 200,
    //   exec: 'testAPI',
    //   tags: { scenario: 'soak' },
    // },
  },
  
  // ============================================================================
  // THRESHOLDS (Performance SLOs)
  // ============================================================================
  
  thresholds: {
    // Response time targets
    'http_req_duration': [
      'p(95)<500',
      'p(99)<1000',
      'p(99.9)<2000',
    ],
    
    // Success rate (99.9% = 0.1% error rate)
    'http_req_failed': ['rate<0.001'],
    
    // Minimum throughput
    'http_reqs': ['rate>100'],
    
    // Custom metrics
    'errors': ['rate<0.001'],
    'api_response_time': ['p(95)<400'],
    
    // Per-scenario thresholds
    'http_req_duration{scenario:baseline}': ['p(95)<450'],
    'http_req_duration{scenario:spike}': ['p(95)<800'],  // Allow higher latency during spike
  },
  
  // Output options
  summaryTrendStats: ['avg', 'min', 'med', 'max', 'p(90)', 'p(95)', 'p(99)', 'p(99.9)'],
};

// ============================================================================
// TEST FUNCTIONS
// ============================================================================

export function testAPI() {
  const url = `${CONFIG.baseUrl}/api/orders`;
  
  const payload = JSON.stringify({
    customer_id: `test_${__VU}_${Date.now()}`,
    items: [
      { sku: 'ITEM-001', quantity: 2, price: 29.99 },
      { sku: 'ITEM-002', quantity: 1, price: 49.99 },
    ],
    total: 109.97,
  });
  
  const params = {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${CONFIG.authToken}`,
    },
    tags: { name: 'CreateOrder' },
  };
  
  const response = http.post(url, payload, params);
  
  // Validate response
  const success = check(response, {
    'status is 201': (r) => r.status === 201,
    'has order_id': (r) => {
      try {
        return r.json('order_id') !== undefined;
      } catch {
        return false;
      }
    },
    'response time < 500ms': (r) => r.timings.duration < 500,
  });
  
  // Record metrics
  errorRate.add(!success);
  apiDuration.add(response.timings.duration);
  throughput.add(1);
  
  // Think time (simulate realistic user behavior)
  sleep(1);
}

// ============================================================================
// LIFECYCLE HOOKS
// ============================================================================

export function setup() {
  console.log(`
╔════════════════════════════════════════════════════════════════════════════╗
║                       K6 PERFORMANCE TEST                                  ║
╟────────────────────────────────────────────────────────────────────────────╢
║ Environment:     ${CONFIG.environment.toUpperCase().padEnd(58)} ║
║ Target:          ${CONFIG.baseUrl.padEnd(58)} ║
║ Test Duration:   ~34 minutes (baseline + ramp + spike)                    ║
╟────────────────────────────────────────────────────────────────────────────╢
║ SCENARIOS:                                                                 ║
║ • Baseline:      147 RPS for 5 minutes                                    ║
║ • Ramp-up:       100 → 294 → 441 RPS (21 minutes)                         ║
║ • Spike:         147 → 882 → 147 RPS (4.5 minutes)                        ║
╟────────────────────────────────────────────────────────────────────────────╢
║ PRODUCTION EXTRAPOLATION:                                                  ║
║ • QA Capacity:   ~294 RPS (measured)                                      ║
║ • Prod Estimate: ~2,500 RPS (294 × 6.8 × 1.25)                           ║
║ • Confidence:    75% (needs validation)                                   ║
╚════════════════════════════════════════════════════════════════════════════╝
  `);
  
  // Verify connectivity
  const testResponse = http.get(`${CONFIG.baseUrl}/health`);
  if (testResponse.status !== 200) {
    throw new Error(`Health check failed: ${testResponse.status}`);
  }
  console.log('✓ Health check passed');
}

export function teardown(data) {
  console.log(`
╔════════════════════════════════════════════════════════════════════════════╗
║                         TEST COMPLETED                                     ║
╟────────────────────────────────────────────────────────────────────────────╢
║ Next Steps:                                                                ║
║ 1. Review summary above                                                    ║
║ 2. Analyze results: /perf analyze-results results.json                    ║
║ 3. Check CloudWatch metrics during test window                            ║
║ 4. Compare against thresholds                                             ║
╚════════════════════════════════════════════════════════════════════════════╝
  `);
}

// ============================================================================
// USAGE INSTRUCTIONS
// ============================================================================

/*

## Running the Test

### Basic (with defaults):
```bash
k6 run performance-test.js
```

### With configuration:
```bash
API_BASE_URL=https://api-qa.example.com \
API_TOKEN=your-token-here \
ENVIRONMENT=qa \
k6 run performance-test.js --out json=results.json
```

### With custom scenarios:
```bash
# Run only baseline scenario
k6 run performance-test.js --scenarios baseline

# Run baseline + ramp-up
k6 run performance-test.js --scenarios baseline,ramp_up
```

### In Docker (portable):
```bash
docker run --rm -i \
  -e API_BASE_URL=${API_URL} \
  -e API_TOKEN=${TOKEN} \
  grafana/k6 run - <performance-test.js --out json=results.json
```

### In CI/CD:
```yaml
# GitHub Actions example
- name: Run k6 Performance Test
  run: |
    k6 run performance-test.js \
      --out json=results.json \
      --summary-export=summary.json
      
- name: Upload Results
  uses: actions/upload-artifact@v3
  with:
    name: k6-results
    path: |
      results.json
      summary.json
```

## CloudWatch Monitoring (During Test)

### EKS Pods
```bash
# Monitor CPU
aws cloudwatch get-metric-statistics \
  --namespace AWS/EKS \
  --metric-name pod_cpu_utilization \
  --dimensions Name=ClusterName,Value=your-cluster \
  --start-time $(date -u -d '30 minutes ago' +%Y-%m-%dT%H:%M:%S) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
  --period 60 \
  --statistics Average
```

### SQS Queue
```bash
# Monitor queue depth
aws sqs get-queue-attributes \
  --queue-url https://sqs.us-east-1.amazonaws.com/123456789/orders \
  --attribute-names ApproximateNumberOfMessagesVisible
```

### Lambda Functions
```bash
# Monitor invocations
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Invocations \
  --dimensions Name=FunctionName,Value=order-processor \
  --start-time $(date -u -d '30 minutes ago' +%Y-%m-%dT%H:%M:%S) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
  --period 60 \
  --statistics Sum
```

### RDS PostgreSQL
```bash
# Monitor database connections
aws cloudwatch get-metric-statistics \
  --namespace AWS/RDS \
  --metric-name DatabaseConnections \
  --dimensions Name=DBInstanceIdentifier,Value=your-db \
  --start-time $(date -u -d '30 minutes ago' +%Y-%m-%dT%H:%M:%S) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
  --period 60 \
  --statistics Maximum
```

## Analyzing Results

After the test completes:

```bash
# Use OpenCode k6-tester agent
/perf analyze-results results.json

# Or manually with jq
cat results.json | jq '{
  throughput: .metrics.http_reqs.values.rate,
  p95_latency: .metrics.http_req_duration.values["p(95)"],
  p99_latency: .metrics.http_req_duration.values["p(99)"],
  error_rate: .metrics.http_req_failed.values.rate
}'
```

## Soak Test (Run Separately)

For 12-hour stability testing:

```bash
# Uncomment the 'soak' scenario in the script, then:
k6 run performance-test.js --scenarios soak --out json=soak-results.json

# Monitor memory growth:
watch -n 60 'kubectl top pods -l app=order-api'
```

## Troubleshooting

### Test fails immediately:
- Check health endpoint: `curl https://api-qa.example.com/health`
- Verify authentication token
- Check network connectivity

### High error rate:
- Reduce load (lower target RPS)
- Check application logs
- Verify database connections available

### Test too slow:
- Increase `preAllocatedVUs` and `maxVUs`
- Reduce `sleep()` duration

### Results not saved:
- Ensure write permissions for output file
- Use `--out json=results.json` flag
- Check disk space

*/
```

## Script Generation Modes

### Mode 1: API-Only (Isolated Testing)
- Test API endpoints without downstream dependencies
- Measure pure API performance
- Mock downstream services if needed

### Mode 2: End-to-End (Full Flow)
- Test complete workflow: API → SQS → Lambda → DB
- Include checks for async processing
- Provide CloudWatch validation steps

### Mode 3: Mixed (Recommended)
- Separate scenarios for isolated and E2E
- Compare performance characteristics
- Identify where delays occur

## Best Practices

### Script Quality
- ✅ Portable (env vars, no hardcoded values)
- ✅ Documented (inline comments, usage instructions)
- ✅ Modular (separate test functions)
- ✅ Realistic (think time, varied payloads)
- ✅ Observable (custom metrics, tags)

### Load Patterns
- ✅ Start with baseline before stress
- ✅ Gradual ramp-up (don't shock the system)
- ✅ Include ramp-down (observe recovery)
- ✅ Realistic think time (users don't spam)

### Thresholds
- ✅ Based on SLOs, not arbitrary
- ✅ Multiple percentiles (p95, p99, p99.9)
- ✅ Error budget aligned with uptime target
- ✅ Per-scenario adjustments (spike allows higher latency)

### Output
- ✅ JSON for programmatic analysis
- ✅ Summary for human review
- ✅ Tags for filtering
- ✅ Custom metrics for domain-specific tracking

## Integration with Other Skills

1. **architecture-analyzer** → Provides profile, calculates QA targets
2. **performance-test** (this skill) → Generates k6 script
3. **analyze-k6-results** → Parses output, extrapolates to production

## When to Use

- ✅ After architecture analysis
- ✅ Before production deployment
- ✅ When capacity planning
- ✅ After infrastructure changes
- ✅ Regular performance regression testing

## Output Files

Generated artifacts:
- `performance-test.js` - Runnable k6 script
- `README.md` - Usage instructions
- `cloudwatch-queries.sh` - Monitoring commands
- `config.example.env` - Environment variable template
