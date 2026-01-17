---
name: architecture-analyzer
description: Parse and understand system architecture for performance testing
license: MIT
compatibility: opencode
metadata:
  audience: developers
  workflow: performance-testing
---

## What I Do

Analyze system architecture to create performance testing strategies. Parse architecture descriptions, identify components, map dependencies, and predict bottlenecks before testing begins.

## Input Formats

### Natural Language
```
"We have an API on EKS that sends messages to SQS, which triggers Lambda 
functions that write to PostgreSQL. Production has 4 CPUs and 2GB RAM with 
2 pods. QA has 1 CPU and 512MB RAM."
```

### YAML Architecture Files
```yaml
components:
  - name: api-gateway
    type: http-api
    platform: eks
    resources:
      prod: { cpu: 4, ram: 2048, replicas: 2 }
      qa: { cpu: 1, ram: 512, replicas: 1 }
```

### Infrastructure as Code
- Terraform configurations
- Kubernetes manifests
- CloudFormation templates
- Docker Compose files

### Code Analysis
- Parse application code for dependencies
- Identify database connections
- Find external service integrations

## Architecture Components

### Identify and Document

**1. Entry Points**
- HTTP APIs (REST, GraphQL)
- WebSocket connections
- Message consumers
- Scheduled jobs

**2. Compute Resources**
- Platform: EKS, ECS, Lambda, EC2
- Resources: CPU, RAM, disk
- Scaling: Fixed, HPA, auto-scaling groups
- Configuration: Replicas, concurrency limits

**3. Async Components**
- Queues: SQS Standard, SQS FIFO
- Topics: SNS, EventBridge
- Streams: Kinesis
- Characteristics: Throughput limits, message size, retention

**4. Data Stores**
- Databases: RDS PostgreSQL, DynamoDB, Aurora
- Caches: Redis, Memcached
- Object storage: S3
- Configuration: Instance type, connections, IOPS

**5. Dependencies**
- External APIs
- Third-party services
- Internal microservices

## Output: Architecture Profile

Generate structured architecture profile:

```yaml
architecture:
  name: "System Name"
  description: "Brief description"
  
  components:
    - id: component-id
      name: "Friendly name"
      type: http-api | sqs-standard | aws-lambda | postgresql | etc
      platform: eks | ecs | lambda | rds
      
      endpoints: # For APIs
        - method: POST
          path: /api/resource
          avg_response_ms: 350
          p95_response_ms: 500
      
      environments:
        production:
          cpu: 4
          ram_mb: 2048
          replicas: 2
          hpa:
            enabled: true
            min_replicas: 2
            max_replicas: 10
            target_cpu_percent: 70
        
        qa:
          cpu: 1
          ram_mb: 512
          replicas: 1
          hpa:
            enabled: false
      
      dependencies:
        - component-id-2
        - component-id-3
      
      performance_characteristics:
        cold_start_ms: 200
        max_concurrent_requests: 1000
        connection_pool_size: 50
      
      bottlenecks:
        - type: connections
          limit: 100
          risk: "May exhaust database connection pool"
          recommendation: "Use RDS Proxy for connection pooling"

extrapolation:
  method: "Multi-factor scaling with efficiency adjustments"
  factors:
    cpu_scaling:
      formula: "(prod_cpu / qa_cpu) * efficiency"
      efficiency: 0.85
    pod_scaling:
      formula: "(prod_replicas / qa_replicas) * lb_efficiency"
      lb_efficiency: 0.90
    combined:
      calculated: 6.8  # Example for 4 CPU, 2 replicas
  
  adjustments:
    cold_start_penalty:
      qa_impact: 15%
      prod_impact: 2%
      adjustment: "+13% for production"
    network_latency:
      qa_to_rds_ms: 5
      prod_to_rds_ms: 1
      adjustment: "+10% for production"
    combined_reality_factor: 1.25

targets:
  production:
    avg_rps: 1000
    peak_rps: 2000
    p95_latency_ms: 300
    p99_latency_ms: 800
    error_rate: 0.001
    uptime: 99.9%
  
  qa_equivalent:
    avg_rps: 147  # Calculated from extrapolation
    peak_rps: 294
    p95_latency_ms: 450
    error_rate: 0.001
```

## Bottleneck Prediction

### Analysis Checklist

**1. Database Connections**
```
Calculate: expected_connections = RPS × connections_per_request × avg_duration
Compare: expected_connections vs max_connections
Risk: Critical if ratio > 0.8
```

**2. Lambda Concurrency**
```
Calculate: concurrent = RPS × avg_duration_seconds
Compare: concurrent vs limit (default 1000)
Risk: Medium if ratio > 0.7
```

**3. SQS Throughput**
```
Calculate: messages_per_sec = RPS
Compare: messages_per_sec vs 300 (soft limit per queue)
Risk: Low (can burst, add queues)
```

**4. CPU Saturation**
```
Calculate: expected_cpu = (test_rps / test_cpu_percent) × target_rps
Target: 60-70% CPU at normal load
Risk: Medium if > 80%
```

**5. Memory**
```
Calculate: memory_per_request × concurrent_requests
Compare: vs available RAM
Risk: High if > 85% (triggers OOM)
```

**6. Network Bandwidth**
```
Calculate: (avg_request_size + avg_response_size) × RPS
Compare: vs network limits
Risk: Low for most applications
```

### Bottleneck Report Format

```markdown
## Predicted Bottlenecks

### 🔴 Critical: Database Connections
- **Component:** RDS PostgreSQL
- **Current Limit:** 100 connections (db.t3.large)
- **Expected Usage:** 280 connections at 1,500 RPS
- **Risk Level:** Will fail at 535 RPS (36% of target)
- **Impact:** Connection pool exhaustion → HTTP 500 errors
- **Solution:** 
  1. RDS Proxy ($11/month) - Recommended
  2. Connection pooling in app (free, requires code changes)
  3. Upgrade to larger instance ($450/month)

### 🟡 Medium: Lambda Concurrency
- **Component:** Order Processor Lambda
- **Current Limit:** 1,000 concurrent
- **Expected Usage:** 750 concurrent at 1,500 RPS
- **Risk Level:** 75% utilization (acceptable)
- **Solution:** Request limit increase to 3,000 (free, 2-3 days)

### 🟢 Low: SQS Throughput
- **Component:** Orders Queue
- **Soft Limit:** 300 messages/sec per queue
- **Expected Usage:** 1,500 messages/sec
- **Risk Level:** Can burst, rarely bottleneck
- **Solution:** Use 5 queues or implement batching (reduce to 150 msg/sec)
```

## Test Strategy Recommendations

### Phase 1: Baseline (Constant Load)
```
Objective: Establish baseline performance
Duration: 5-10 minutes
Load: 50% of QA target
Metrics: Response time, error rate, resource usage
```

### Phase 2: Ramp-Up
```
Objective: Find capacity limits
Duration: 15-20 minutes
Load: 0 → 100% → 150% of QA target
Metrics: Breaking point, degradation curve
```

### Phase 3: Spike Test
```
Objective: Handle traffic bursts
Duration: 10 minutes
Load: Normal → 3x spike → Normal
Metrics: Recovery time, error spike
```

### Phase 4: Stress Test
```
Objective: Push beyond limits
Duration: 15-20 minutes
Load: 100% → 200% of QA target
Metrics: First component to fail, cascading failures
```

### Phase 5: Soak Test
```
Objective: Detect memory leaks, degradation
Duration: 12-24 hours
Load: 60-70% of QA capacity
Metrics: Memory growth, response time drift, connection leaks
```

## Extrapolation Calculations

### Formula Components

**1. CPU Scaling**
```
Factor = (Prod CPU / QA CPU) × Efficiency
Efficiency = 0.85 (15% overhead for multi-core coordination)

Example: (4 CPU / 1 CPU) × 0.85 = 3.4x
```

**2. Replica/Pod Scaling**
```
Factor = (Prod Replicas / QA Replicas) × LB Efficiency
LB Efficiency = 0.90 (10% load balancer overhead)

Example: (2 pods / 1 pod) × 0.90 = 1.8x
```

**3. Combined Base Scaling**
```
Base Factor = CPU Factor × Replica Factor
Example: 3.4 × 1.8 = 6.12x
```

**4. Target CPU Adjustment**
```
Adjustment = Target CPU% / Observed CPU%
Purpose: Leave headroom for bursts

Example: If QA runs at 78% CPU but want Prod at 60%:
Adjustment = 60 / 78 = 0.77x
```

**5. Reality Factor**
```
Cold Starts: QA 15% → Prod 2% = +13%
Network: QA 5ms → Prod 1ms = +10%
Resources: Shared → Dedicated = +5%
Combined: 1.25x (or adjust based on observations)
```

**6. Final Calculation**
```
Prod Capacity = QA Capacity × Base Factor × CPU Adjustment × Reality Factor

Example:
250 RPS × 6.12 × 0.77 × 1.25 = 1,471 RPS
```

### Confidence Levels

- **90%+:** Validated with production shadow traffic
- **80-89%:** Multiple test runs, consistent results
- **70-79%:** Single test run, reasonable assumptions
- **60-69%:** Limited data, many assumptions
- **<60%:** Highly speculative, needs more testing

## CloudWatch Monitoring Guide

Provide monitoring instructions for test validation:

### EKS Pods
```
Metrics to watch:
- CPUUtilization (target: <80%)
- MemoryUtilization (target: <85%)
- NetworkIn/NetworkOut
- Running pod count (verify HPA)

Alert if:
- CPU > 90% for 5+ minutes
- Memory > 90%
- Pod restart rate increases
```

### SQS Queues
```
Metrics to watch:
- ApproximateNumberOfMessagesVisible (queue depth)
- NumberOfMessagesSent
- NumberOfMessagesReceived
- ApproximateAgeOfOldestMessage

Alert if:
- Queue depth > 1000
- Oldest message > 5 minutes
- Messages sent ≠ API requests (indicates failures)
```

### Lambda Functions
```
Metrics to watch:
- Invocations
- Errors
- Duration (avg, p99)
- ConcurrentExecutions
- Throttles

Alert if:
- Error rate > 0.1%
- Duration p99 > 25 seconds (timeout risk)
- Concurrent > 80% of limit
- Any throttles
```

### RDS PostgreSQL
```
Metrics to watch:
- DatabaseConnections (critical!)
- CPUUtilization
- WriteLatency
- WriteIOPS
- FreeableMemory

Alert if:
- Connections > 80 (for 100 max)
- CPU > 80%
- WriteLatency > 10ms p95
- IOPS approaching provisioned limit
```

## Usage Examples

### Example 1: Parse Natural Language

**Input:**
```
"My order API runs on EKS with 4 CPUs and 2GB RAM in production with 2 pods. 
QA has 1 CPU and 512MB with 1 pod. When an order is created, we send a message 
to SQS which triggers a Lambda to write to PostgreSQL. We need to handle 
2,000 RPS in production."
```

**Output:**
```yaml
architecture:
  name: "Order Management System"
  components:
    - id: api-gateway
      type: http-api
      platform: eks
      endpoints:
        - method: POST
          path: /api/orders
      environments:
        production: { cpu: 4, ram_mb: 2048, replicas: 2 }
        qa: { cpu: 1, ram_mb: 512, replicas: 1 }
      dependencies: [sqs-orders]
    
    - id: sqs-orders
      type: sqs-standard
      dependencies: [lambda-processor]
    
    - id: lambda-processor
      type: aws-lambda
      dependencies: [rds-postgres]
    
    - id: rds-postgres
      type: postgresql
      platform: aws-rds

extrapolation:
  factors:
    combined: 6.8
  
targets:
  production:
    avg_rps: 2000
  qa_equivalent:
    avg_rps: 294  # 2000 / 6.8
```

### Example 2: Analyze Kubernetes Manifests

**Input:** `deployment.yaml`
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: order-api
spec:
  replicas: 2
  template:
    spec:
      containers:
      - name: api
        resources:
          requests:
            cpu: "4"
            memory: "2Gi"
          limits:
            cpu: "4"
            memory: "2Gi"
```

**Output:** Architecture profile with EKS configuration extracted

### Example 3: Predict Bottlenecks

**Input:** Architecture profile + target 3,000 RPS

**Output:**
```markdown
## Bottleneck Analysis for 3,000 RPS Target

### 🔴 Critical: Database Connections
At 3,000 RPS, expect ~570 concurrent database connections.
RDS limit: 100 connections (db.t3.large)
**Will fail at 526 RPS (18% of target)**

Solution: RDS Proxy ($11/month)

### 🟡 Medium: Lambda Concurrency
At 3,000 RPS with 5s avg duration = 15,000 concurrent executions
Default limit: 1,000
**Will throttle above 200 RPS**

Solution: Request limit increase to 20,000 (free)

### Recommendation: Address both before testing
```

## Integration with k6-tester Agent

This skill is designed to work with the k6-tester agent:

1. **Architecture Analysis** → Generates profile
2. **Performance Test Skill** → Uses profile to create k6 scripts
3. **Analyze Results Skill** → Uses profile for extrapolation

The architecture profile is the foundation for all performance testing activities.

## When to Use

- ✅ Before creating k6 test scripts
- ✅ When planning production capacity
- ✅ When investigating performance issues
- ✅ Before scaling infrastructure
- ✅ When onboarding new team members (documentation)

## Best Practices

1. **Always analyze architecture first** - Don't guess, understand
2. **Document assumptions** - Reality factor adjustments should be explained
3. **Update profiles regularly** - Architecture changes over time
4. **Validate predictions** - Test results should confirm bottleneck predictions
5. **Include monitoring** - Architecture analysis should guide what to monitor

## Output Files

Generated files:
- `architecture-profile.yaml` - Structured component map
- `architecture-analysis.md` - Human-readable report
- `test-strategy.md` - Recommended testing approach
- `monitoring-guide.md` - CloudWatch metrics to watch
