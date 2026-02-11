---
name: robot-framework-analyzer
description: Analyze Robot Framework test suites for coverage gaps, duplicate tests, selector stability, and generate missing test recommendations with Zephyr Scale integration
license: MIT
compatibility: opencode
metadata:
  audience: developers
  workflow: testing
---

## What I Do

Analyze Robot Framework test suites to identify coverage gaps, detect duplicate or redundant tests, validate selector stability, and generate recommendations for missing tests. Integrates with your Swagger API specification to map frontend tests to backend coverage, and exports results to Zephyr Scale for test management.

**Perfect for:**
- Robot Framework + Browser/Playwright library users
- C# Umbraco/React full-stack applications
- Teams using JIRA + Zephyr Scale for test management
- Keyword-driven testing approaches

---

## Input Requirements

### 1. Robot Framework Tests (Required)

**Directory Structure:**
```
test_scenarios/
├── login_tests.robot
├── checkout_flow.robot
├── user_management/
│   ├── create_user.robot
│   └── delete_user.robot
├── resources/
│   ├── common.resource
│   ├── login_page.resource
│   └── checkout_page.resource
└── libraries/
    ├── CustomKeywords.py
    └── ApiHelpers.py
```

**Test Files:**
- `.robot` files containing test cases
- `.resource` files with keywords and variables
- `.py` library files

### 2. Swagger/OpenAPI Specification (Required for Coverage)

**Backend API Documentation:**
```yaml
openapi: 3.0.0
info:
  title: Umbraco API
  version: 1.0.0
paths:
  /api/users:
    get:
      summary: List users
    post:
      summary: Create user
  /api/users/{id}:
    get:
      summary: Get user
    put:
      summary: Update user
    delete:
      summary: Delete user
```

**Location:** `swagger.json` or `swagger.yaml` in project root

### 3. Application Source Code (Optional but Recommended)

**For Coverage Analysis:**
- C# Controllers (`.cs` files)
- React Components (`.tsx`, `.jsx` files)
- API endpoints

**Location:** Source code directory

### 4. Zephyr Scale Configuration (Optional)

**For Test Export:**
- JIRA project key
- Zephyr Scale API token
- Base URL

---

## Analysis Components

### 1. Coverage Gap Analysis (Priority A)

Identifies untested backend endpoints and frontend flows:

```markdown
## Coverage Gap Report

### Backend API Coverage

| Endpoint | Method | Tested | Coverage % | Missing Scenarios |
|----------|--------|--------|------------|-------------------|
| /api/users | GET | ✅ Yes | 80% | Pagination, filtering |
| /api/users | POST | ✅ Yes | 100% | - |
| /api/users/{id} | GET | ⚠️ Partial | 50% | Invalid ID handling |
| /api/users/{id} | DELETE | ❌ No | 0% | All scenarios |

### Frontend Flow Coverage

| User Flow | Steps Covered | Missing Steps | Priority |
|-----------|---------------|---------------|----------|
| User Login | 3/4 | 2FA, password reset | High |
| Checkout | 5/8 | Payment failure, guest checkout | Critical |
| Profile Update | 2/6 | Avatar upload, validation | Medium |

### Overall Coverage
- **Backend API:** 67% (24/36 endpoints)
- **Frontend Flows:** 58% (31/53 steps)
- **Critical Paths:** 45% (9/20 scenarios)
```

**Mapping Logic:**
```
Swagger Endpoint → Robot Test Case → Coverage Score
/api/users POST → Create New User → ✅ Covered
/api/users/{id} DELETE → (no test) → ❌ Gap
```

---

### 2. Duplicate/Redundant Test Detection (Priority B)

Finds tests with overlapping functionality:

```markdown
## Duplicate Test Analysis

### 🔴 Exact Duplicates (2 found)

**Duplicate Group #1:**
- File: `test_scenarios/login_tests.robot:45`
  - Test: "Valid User Login"
  - Keywords: Open Browser, Input Text, Click Button, Wait
  
- File: `test_scenarios/auth/login.robot:23`
  - Test: "User Can Login Successfully"
  - Keywords: Open Browser, Input Text, Click Button, Wait
  
**Similarity:** 95%
**Recommendation:** Merge into single test in `login_tests.robot`, delete duplicate

### 🟡 Near Duplicates (5 found)

**Similar Tests:**
- "Create User With Valid Data" (create_user.robot:15)
- "Create New User Successfully" (user_management.robot:42)
  
**Difference:** Only test data varies
**Recommendation:** Use Test Template with data-driven approach

### 🟢 Redundant Steps (8 found)

**Example:**
- 12 tests manually navigate to login page
- **Recommendation:** Use Suite Setup or custom keyword `Login As User`
```

**Detection Algorithm:**
- AST (Abstract Syntax Tree) comparison
- Keyword sequence similarity (Levenshtein distance)
- Variable normalization
- Step count comparison

---

### 3. Selector Stability Validation (Priority C)

Validates CSS/XPath selectors for maintainability:

```markdown
## Selector Stability Report

### 🔴 Critical Issues (3 found)

**File:** `resources/login_page.resource`
```
Click Button    xpath=//div[3]/div[2]/button[1]
```
**Issue:** Brittle XPath with indices
**Risk:** Breaks on any DOM structure change
**Fix:** Use data-testid or semantic selectors
```
Click Button    css=[data-testid="login-button"]
```

### 🟠 Warnings (7 found)

**File:** `resources/checkout_page.resource`
```
Input Text    css=.form-control:nth-child(2)    ${email}
```
**Issue:** CSS nth-child selector
**Risk:** Breaks if form fields reordered
**Fix:** Add unique identifiers
```
Input Text    css=[data-testid="email-input"]    ${email}
```

### 🟢 Recommendations (12 found)

**Best Practice:** Add data-testid attributes
```html
<!-- Before -->
<button class="btn primary">Submit</button>

<!-- After -->
<button class="btn primary" data-testid="submit-order-btn">Submit</button>
```

### Selector Health Score: 73/100
- Stable selectors: 45
- Brittle selectors: 10
- Missing data-testid: 28 elements
```

**Stability Rules:**
- ✅ **Stable:** `data-testid`, `id`, semantic attributes
- ⚠️ **Fragile:** `nth-child`, `nth-of-type`, positional XPath
- ❌ **Brittle:** Dynamic classes, deep nesting, indices

---

### 4. Missing Test Recommendations (Priority D)

Generates specific test cases for uncovered scenarios:

```markdown
## Missing Test Recommendations

### Critical Priority (Must Test)

**1. API Error Handling**
```robot
Test API Returns 404 For Invalid User
    [Documentation]    Verify API returns 404 when user ID doesn't exist
    [Tags]    api    error-handling    critical
    Create Session    api    ${BASE_URL}
    ${response}=    GET On Session    api    /api/users/99999    expected_status=404
    Should Be Equal As Strings    ${response.status_code}    404
```
**Reason:** No error handling tests found for GET /api/users/{id}
**File:** `test_scenarios/api/error_handling.robot`

**2. Payment Failure Flow**
```robot
Test Checkout With Declined Card
    [Documentation]    Verify declined card shows error message
    [Tags]    checkout    payment    critical
    Given User Is On Checkout Page
    When User Enters Declined Card Details
    And User Clicks Place Order
    Then Error Message Should Be Visible    Payment declined
```
**Reason:** Only success path tested, no failure scenarios
**File:** `test_scenarios/checkout/payment_failure.robot`

### High Priority (Should Test)

**3. Session Timeout**
```robot
Test User Redirected To Login After Session Timeout
    [Documentation]    Verify user is redirected when session expires
    [Tags]    session    security    high
    Given User Is Logged In
    When Session Expires
    And User Navigates To Profile Page
    Then User Should Be Redirected To Login Page
```

### Medium Priority (Nice to Have)

**4. Form Validation**
- Email format validation
- Password strength requirements
- Required field validation

**5. Accessibility**
- Keyboard navigation tests
- Screen reader compatibility
- ARIA label verification
```

**Recommendation Logic:**
```
Uncovered Endpoint × Risk Factor × Usage Frequency = Priority

Example:
/api/users/{id} DELETE (uncovered)
× Risk: High (destructive operation)
× Usage: Medium (admin function)
= Priority: Critical
```

---

## Output Formats

### 1. Markdown Report (Human-Readable)

**File:** `robot-analysis-report.md`

Complete analysis with:
- Executive summary
- Coverage gaps by priority
- Duplicate test details
- Selector issues with fixes
- Missing test recommendations (ready to copy)

### 2. JSON Data (Machine-Readable)

**File:** `robot-analysis-results.json`

```json
{
  "analysis_metadata": {
    "timestamp": "2026-02-09T10:30:00Z",
    "robot_files_analyzed": 24,
    "test_cases_found": 156,
    "keywords_found": 89
  },
  "coverage": {
    "backend_api": {
      "total_endpoints": 36,
      "tested_endpoints": 24,
      "coverage_percentage": 67,
      "gaps": [
        {
          "endpoint": "/api/users/{id}",
          "method": "DELETE",
          "priority": "critical",
          "reason": "Destructive operation, no tests found"
        }
      ]
    },
    "frontend_flows": {
      "total_steps": 53,
      "covered_steps": 31,
      "coverage_percentage": 58
    }
  },
  "duplicates": [
    {
      "type": "exact",
      "similarity": 0.95,
      "tests": [
        {
          "file": "test_scenarios/login_tests.robot",
          "line": 45,
          "name": "Valid User Login"
        },
        {
          "file": "test_scenarios/auth/login.robot",
          "line": 23,
          "name": "User Can Login Successfully"
        }
      ],
      "recommendation": "Merge tests, keep in login_tests.robot"
    }
  ],
  "selectors": {
    "score": 73,
    "critical_issues": 3,
    "warnings": 7,
    "stable_count": 45,
    "brittle_count": 10
  },
  "recommendations": [
    {
      "priority": "critical",
      "category": "api",
      "title": "Test API Returns 404 For Invalid User",
      "code": "...",
      "file": "test_scenarios/api/error_handling.robot"
    }
  ]
}
```

### 3. Zephyr Scale Import Format

**File:** `zephyr-import.json`

```json
{
  "tests": [
    {
      "name": "Create User With Valid Data",
      "objective": "Verify user can be created with valid information",
      "precondition": "User is authenticated as admin",
      "steps": [
        {
          "index": 1,
          "description": "Navigate to user creation page",
          "expectedResult": "User creation form is displayed"
        },
        {
          "index": 2,
          "description": "Fill in user details",
          "expectedResult": "Form accepts all input"
        }
      ],
      "priority": "High",
      "status": "Draft",
      "folder": "/User Management",
      "labels": ["robot-framework", "ui", "regression"]
    }
  ]
}
```

---

## Integration with Other Skills

### Workflow Integration

```
robot-framework-analyzer
         ↓
    [Analyzes existing tests]
         ↓
    +-> test-coverage-merger (future skill)
    |       ↓
    |   [Combines with C# coverage]
    |       ↓
    +-> architecture-analyzer
            ↓
        [Identifies critical paths]
            ↓
        +-> performance-test
                ↓
            [Generates k6 scripts for critical paths]
```

### Zephyr Scale Integration

1. **Export Analysis Results**
   ```bash
   # Generate Zephyr import file
   python robot_analyzer.py --export-zephyr
   ```

2. **Import to Zephyr Scale**
   - Use Zephyr Scale API or UI import
   - Maps Robot tests to test cases
   - Maintains traceability

3. **Sync Status**
   - Updates test case status
   - Links to JIRA issues
   - Tracks coverage over time

---

## Usage Examples

### Example 1: Full Analysis

**Command:**
```bash
# Analyze with all features
python robot_analyzer.py \
  --test-dir test_scenarios \
  --swagger swagger.json \
  --source-dir src/ \
  --output-format both
```

**Input Files:**
- `test_scenarios/*.robot` (test cases)
- `test_scenarios/resources/*.resource` (keywords)
- `swagger.json` (API spec)
- `src/` (source code)

**Output:**
- `robot-analysis-report.md`
- `robot-analysis-results.json`

---

### Example 2: Coverage-Only Analysis

**Command:**
```bash
# Quick coverage check
python robot_analyzer.py \
  --test-dir test_scenarios \
  --swagger swagger.json \
  --mode coverage-only \
  --min-coverage 80
```

**Output:**
- Lists endpoints below 80% coverage
- Exit code 1 if coverage < threshold (for CI/CD)

---

### Example 3: Duplicate Detection

**Command:**
```bash
# Find duplicates only
python robot_analyzer.py \
  --test-dir test_scenarios \
  --mode duplicates \
  --similarity-threshold 0.85
```

**Output:**
- Groups of similar tests
- Similarity scores
- Merge recommendations

---

### Example 4: Zephyr Export

**Command:**
```bash
# Export to Zephyr Scale
python robot_analyzer.py \
  --test-dir test_scenarios \
  --export-zephyr \
  --zephyr-project PROJ \
  --output zephyr-import.json
```

**Upload:**
```bash
# Upload to Zephyr Scale via API
curl -X POST \
  -H "Authorization: Bearer $ZEPHYR_TOKEN" \
  -H "Content-Type: application/json" \
  -d @zephyr-import.json \
  "https://api.zephyrscale.smartbear.com/v2/testcases"
```

---

### Example 5: CI/CD Integration

**GitHub Actions:**
```yaml
- name: Analyze Robot Framework Tests
  run: |
    python robot_analyzer.py \
      --test-dir test_scenarios \
      --swagger swagger.json \
      --output-format both \
      --fail-below 70
  
- name: Upload Analysis Report
  uses: actions/upload-artifact@v4
  with:
    name: robot-analysis
    path: |
      robot-analysis-report.md
      robot-analysis-results.json
```

---

## When to Use

### ✅ Use This Skill When:

- **Before releases:** Verify test coverage meets requirements
- **Sprint planning:** Identify missing test scenarios
- **Code reviews:** Check if new features have tests
- **Refactoring:** Detect duplicate tests before consolidation
- **CI/CD gates:** Enforce minimum coverage thresholds
- **Zephyr migration:** Export existing Robot tests to Zephyr Scale

### ❌ Don't Use When:

- Tests are not in Robot Framework format (use language-specific tools)
- You only need basic test execution (use `robot` command)
- No API specification available (coverage analysis will be limited)

---

## Best Practices

### Test Organization

✅ **Recommended Structure:**
```
test_scenarios/
├── login/
│   ├── valid_login.robot
│   ├── invalid_login.robot
│   └── _resources/
│       └── login_keywords.resource
├── checkout/
├── api/
└── _common/
    ├── setup.resource
    └── teardown.resource
```

### Selector Strategy

✅ **Use Stable Selectors:**
```robot
# Good - data-testid
Click Button    css=[data-testid="submit-btn"]

# Good - semantic + text
Click Button    xpath=//button[contains(text(), "Submit")]

# Bad - brittle XPath
Click Button    xpath=//div[3]/div[2]/button[1]
```

### Keyword Design

✅ **Reusable Keywords:**
```robot
*** Keywords ***
Login As User
    [Arguments]    ${username}    ${password}
    Input Text    css=[data-testid="username"]    ${username}
    Input Text    css=[data-testid="password"]    ${password}
    Click Button    css=[data-testid="login-btn"]
    Wait Until Page Contains    Welcome
```

---

## Troubleshooting

### Issue: "No tests found"

**Cause:** Wrong directory or file pattern
**Solution:**
```bash
# Verify directory structure
ls -la test_scenarios/

# Check file extensions
find test_scenarios -name "*.robot" -o -name "*.resource"
```

### Issue: "Swagger parsing failed"

**Cause:** Invalid OpenAPI spec
**Solution:**
```bash
# Validate swagger
swagger-codegen validate -i swagger.json

# Or use online validator
https://editor.swagger.io/
```

### Issue: "Coverage shows 0% for all endpoints"

**Cause:** No mapping between tests and API endpoints
**Solution:**
- Add API call keywords to Robot tests
- Use descriptive keyword names matching endpoint paths
- Add comments linking tests to endpoints

---

## Output Files

Generated artifacts:
- `robot-analysis-report.md` - Human-readable analysis
- `robot-analysis-results.json` - Machine-readable data
- `zephyr-import.json` - Zephyr Scale import format
- `selector-fixes.md` - Recommended selector improvements
- `missing-tests/` - Directory with generated test stubs

---

## Integration Checklist

Before running analysis, ensure:

- [ ] Robot Framework tests are in `test_scenarios/` directory
- [ ] Swagger/OpenAPI spec is up to date
- [ ] All test dependencies are installed
- [ ] Python libraries are importable
- [ ] Zephyr Scale credentials are configured (if exporting)

---

## Notes

### Performance

- Analysis time: ~30 seconds for 100 test cases
- Memory usage: ~200MB for large test suites
- Parallel processing: Supported for file parsing

### Limitations

- Dynamic keyword generation: May not detect all keywords
- Complex variable substitution: Some variables may not resolve
- Custom Robot Framework libraries: Requires Python parsing

### Future Enhancements

- [ ] Visual test coverage heatmap
- [ ] AI-powered test generation
- [ ] Automatic selector refactoring
- [ ] Real-time analysis during test execution
- [ ] Integration with test execution reports

---

## See Also

- [architecture-analyzer](architecture-analyzer) - Analyze system architecture
- [performance-test](performance-test) - Generate k6 performance tests
- [test-coverage-merger](test-coverage-merger) - Merge coverage from multiple languages (future)
- [zephyr-test-exporter](zephyr-test-exporter) - Export to Zephyr Scale (future)

---

**Version:** 1.0.0  
**Author:** OpenCode SDET Tools  
**License:** MIT
