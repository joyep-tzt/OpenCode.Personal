---
description: Quick performance testing workflow with k6-tester agent
---

# /perf - Performance Testing Command

Quick access to k6 performance testing workflows using the k6-tester agent and associated skills.

## Subcommands

### `/perf analyze`
Analyze system architecture and create test strategy

**Usage:**
```
/perf analyze
/perf analyze architecture.yaml
/perf analyze "Describe your architecture here"
```

**What it does:**
- Invokes `architecture-analyzer` skill
- Parses architecture from files, code, or description
- Identifies components and dependencies
- Predicts bottlenecks
- Generates test strategy recommendations
- Outputs architecture profile (YAML)

**Example:**
```
User: /perf analyze

Agent: I'll analyze your architecture. Please provide:
1. Architecture description, YAML file, or infrastructure code
2. Environment specifications (QA vs Production resources)
3. Performance targets (expected RPS, latency SLOs)

[Agent analyzes and generates architecture profile]
```

---

### `/perf create`
Generate k6 test script with appropriate load patterns

**Usage:**
```
/perf create
/perf create --type api-only
/perf create --type e2e
/perf create --pattern baseline,ramp,spike
/perf create --target-rps 2000
```

**Options:**
- `--type`: Test type (`api-only`, `e2e`, `all`) - Default: `all`
- `--pattern`: Load patterns (`constant`, `ramp`, `spike`, `stress`, `soak`, `all`) - Default: `all`
- `--target-rps`: Production target RPS - Default: Ask user
- `--environment`: Target environment (`qa`, `staging`, `prod`) - Default: `qa`

**What it does:**
- Invokes `performance-test` skill
- Uses architecture profile (from `/perf analyze` or asks for details)
- Generates portable k6 script (.js file)
- Creates configuration guide
- Provides CloudWatch monitoring instructions

**Example:**
```
User: /perf create --target-rps 2000

Agent: Creating k6 test script for 2,000 RPS production target...

Based on your architecture (4 vCPU, 2GB, 2 pods in prod vs 1 vCPU, 512MB, 1 pod in QA):
- Extrapolation factor: 6.8x
- QA target: 294 RPS
- Stress test: 441 RPS

Generated files:
- performance-test.js (k6 script)
- README.md (usage instructions)
- cloudwatch-queries.sh (monitoring commands)

Run with: k6 run performance-test.js --out json=results.json
```

---

### `/perf run`
Execute k6 test (interactive workflow)

**Usage:**
```
/perf run
/perf run performance-test.js
```

**What it does:**
- Checks if k6 is installed
- Prompts for configuration (API URL, auth token, etc.)
- Executes test with `!k6 run ...`
- Saves results to JSON
- Automatically triggers analysis when complete

**Example:**
```
User: /perf run

Agent: I'll run the performance test. First, let me verify your environment:

✓ k6 installed (version 0.48.0)
✓ Test script found: performance-test.js
✓ API accessible: https://api-qa.example.com/health

Configuration:
- API_BASE_URL: https://api-qa.example.com
- Environment: qa
- Output: results.json

!k6 run performance-test.js --out json=results.json

[Test runs for 34 minutes]

Test completed! Analyzing results...
[Triggers /perf analyze-results results.json]
```

---

### `/perf analyze-results`
Analyze k6 test results with extrapolation and cost modeling

**Usage:**
```
/perf analyze-results results.json
/perf analyze-results results.json --arch architecture.yaml
/perf analyze-results [paste k6 summary text]
```

**Options:**
- `--arch`: Architecture profile file - Default: Auto-detect or ask
- `--cloudwatch`: Include CloudWatch metrics - Default: false
- `--format`: Output format (`markdown`, `json`, `both`) - Default: `both`

**What it does:**
- Invokes `analyze-k6-results` skill
- Parses k6 output (JSON or text)
- Checks threshold compliance
- Extrapolates to production capacity
- Identifies bottlenecks
- Performs cost analysis
- Provides prioritized recommendations

**Example:**
```
User: /perf analyze-results results.json

Agent: Analyzing performance test results...

## Executive Summary
✅ System can handle production targets
⚠️ Database connection pooling (RDS Proxy) needed

**QA Results:**
- Achieved: 250 RPS
- p95 latency: 456ms
- Error rate: 0.05%

**Production Estimate:**
- Capacity: 1,471 RPS (95% confidence)
- p95 latency: 365ms
- First bottleneck: Database connections at 4,022 RPS

**Cost for 3,000 RPS:** $1,205/month (with optimizations)

[Full analysis report generated]

Generated files:
- analysis-report.md
- metrics.json
```

---

### `/perf estimate`
Cost estimation for scaling scenarios

**Usage:**
```
/perf estimate --target-rps 5000
/perf estimate --target-rps 5000 --current-results results.json
/perf estimate --scale 3x
```

**Options:**
- `--target-rps`: Target requests per second
- `--scale`: Scaling factor (e.g., `2x`, `3x`, `5x`)
- `--current-results`: Use actual test results - Default: Ask for current performance
- `--optimize`: Include cost optimizations - Default: true

**What it does:**
- Calculates resource requirements for target load
- Estimates AWS costs (EKS, RDS, Lambda, SQS, SNS)
- Identifies bottlenecks at target scale
- Suggests optimizations (batching, spot instances, etc.)
- Provides multiple scenarios (cheap/balanced/premium)

**Example:**
```
User: /perf estimate --target-rps 5000

Agent: Estimating costs for 5,000 RPS target...

**Current Performance:** 250 RPS @ $526/month
**Target:** 5,000 RPS (20x increase)

**Required Resources:**
- EKS: 8 pods (32 vCPU) - $1,152/month
- RDS: db.r5.2xlarge - $900/month
- Lambda: 150M invocations - $205/month
- SQS: 150M requests - $60/month
- SNS: 150M notifications - $75/month

**Total: $2,653/month** (baseline)

**With Optimizations:**
- SQS batching: -$238/month
- Spot instances (50%): -$403/month
- RDS Proxy: -$320/month (vs instance upgrade)

**Optimized Total: $1,692/month** (36% savings)

**Bottlenecks:**
🔴 Database connections: Need RDS Proxy or larger instance
🟡 Lambda concurrency: Request increase to 20,000

[Full cost analysis generated]
```

---

### `/perf compare`
Compare multiple test runs

**Usage:**
```
/perf compare baseline.json latest.json
/perf compare --baseline baseline.json --current latest.json
```

**What it does:**
- Compares metrics across test runs
- Identifies performance regression or improvement
- Highlights threshold violations
- Shows trend analysis

**Example:**
```
User: /perf compare baseline.json latest.json

Agent: Comparing test results...

## Performance Comparison

| Metric | Baseline | Latest | Change |
|--------|----------|--------|--------|
| Throughput | 250 RPS | 280 RPS | +12% ✅ |
| p95 Latency | 456ms | 420ms | -8% ✅ |
| Error Rate | 0.05% | 0.03% | -40% ✅ |

**Analysis:**
✅ Performance improved across all metrics
✅ Recent optimizations are working
✅ No threshold violations

**Recommendations:**
- Monitor sustained performance over 24-48 hours
- Consider increasing target load
```

---

### `/perf monitor`
Generate CloudWatch monitoring setup

**Usage:**
```
/perf monitor
/perf monitor --arch architecture.yaml
/perf monitor --format dashboard
```

**Options:**
- `--format`: Output format (`cli`, `dashboard`, `terraform`) - Default: `cli`
- `--arch`: Architecture profile - Default: Auto-detect

**What it does:**
- Generates CloudWatch query commands
- Creates dashboard JSON (for import)
- Provides Terraform configuration
- Sets up alarms for critical metrics

**Example:**
```
User: /perf monitor

Agent: Generating CloudWatch monitoring setup...

## CLI Commands

### EKS Pods
aws cloudwatch get-metric-statistics \
  --namespace AWS/EKS \
  --metric-name pod_cpu_utilization \
  --dimensions Name=ClusterName,Value=your-cluster \
  ...

### SQS Queue
aws sqs get-queue-attributes \
  --queue-url https://sqs.us-east-1.amazonaws.com/...
  ...

[Full monitoring guide generated]
```

---

## Workflow Examples

### Complete Workflow (First Time)

```
1. User: /perf analyze
   → Generates architecture profile

2. User: /perf create --target-rps 2000
   → Generates k6 test script

3. User: Manually runs: k6 run performance-test.js --out json=results.json

4. User: /perf analyze-results results.json
   → Full analysis with extrapolation and cost modeling

5. User: /perf estimate --target-rps 5000
   → Cost estimation for future scaling
```

### Quick Workflow (Existing Setup)

```
1. User: /perf run
   → Runs test automatically

2. Agent: Auto-analyzes results when complete
   → Provides summary and recommendations
```

### Cost Planning Workflow

```
1. User: /perf analyze-results results.json

2. User: /perf estimate --scale 3x
   → Calculates costs for 3x current load

3. User: /perf estimate --scale 3x --optimize
   → Includes cost optimizations
```

## Integration with k6-tester Agent

All `/perf` commands invoke the `@k6-tester` agent with appropriate context:

```
User: /perf analyze
↓
Command invokes: @k6-tester "Use architecture-analyzer skill to analyze the system"
↓
Agent uses skill and generates output
```

## Prerequisites

- **k6 installed:** Required for `/perf run`
- **AWS CLI:** Optional, for CloudWatch monitoring
- **Architecture profile:** Generated by `/perf analyze` or provided manually

## Tips

1. **Always start with `/perf analyze`** - Understanding architecture is critical
2. **Run soak tests separately** - 12-hour tests need dedicated time
3. **Monitor CloudWatch during tests** - Validates extrapolation assumptions
4. **Iterate on targets** - Start conservative, increase gradually
5. **Keep results** - Compare over time to track performance trends

## Command Aliases

```
/perf analyze     → /perf-analyze
/perf create      → /perf-create
/perf run         → /perf-run
/perf results     → /perf analyze-results
/perf cost        → /perf estimate
```

## Error Handling

If k6 is not installed:
```
Agent: k6 is not installed. Install with:

# macOS
brew install k6

# Linux
sudo gpg -k
sudo gpg --no-default-keyring --keyring /usr/share/keyrings/k6-archive-keyring.gpg --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys C5AD17C747E3415A3642D57D77C6C491D6AC1D69
echo "deb [signed-by=/usr/share/keyrings/k6-archive-keyring.gpg] https://dl.k6.io/deb stable main" | sudo tee /etc/apt/sources.list.d/k6.list
sudo apt-get update
sudo apt-get install k6

# Docker
docker pull grafana/k6
```

## Best Practices

- ✅ Run tests during low-traffic periods (QA environments)
- ✅ Save all results for historical comparison
- ✅ Document architecture changes that affect performance
- ✅ Validate extrapolations with shadow traffic
- ✅ Implement recommendations in priority order (Critical first)
