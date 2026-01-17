---
name: security-audit
description: Security vulnerability scanning and best practices check
license: MIT
compatibility: opencode
metadata:
  audience: developers
  workflow: security
---

## What I Do
Perform comprehensive security audit of code changes, identifying vulnerabilities and security best practices violations.

## Security Checks

### Input Validation
- All user input validated
- SQL injection prevention (parameterized queries)
- XSS prevention (proper escaping)
- Command injection prevention
- Path traversal prevention

### Authentication & Authorization
- Authentication required for sensitive endpoints
- Authorization checks before data access
- Session management secure
- Password requirements enforced
- Multi-factor authentication considered

### Data Protection
- Sensitive data encrypted
- No hardcoded secrets
- Secure password storage (hashing + salt)
- PII handled properly
- HTTPS enforced

### Dependencies
- No known vulnerable packages
- Dependencies up to date
- License compliance
- Supply chain security

### Configuration
- Security headers configured
- CORS properly configured
- Rate limiting in place
- Error messages don't leak info
- Debug mode disabled in production

### API Security
- API keys rotated regularly
- API rate limiting
- Request validation
- Response sanitization
- Proper HTTP methods

## Severity Classification

### 🔴 Critical (Fix Immediately)
- SQL injection
- Remote code execution
- Authentication bypass
- Exposed secrets
- Data leaks

### 🟠 High (Fix Before Release)
- XSS vulnerabilities
- Broken authentication
- Sensitive data exposure
- Insecure dependencies
- Missing authorization

### 🟡 Medium (Fix Soon)
- Missing rate limiting
- Weak crypto
- Insufficient logging
- Missing security headers
- Insecure configs

### 🟢 Low (Best Practice)
- Code complexity
- Missing documentation
- Outdated dependencies
- Code duplication

## Output Format

```markdown
## Security Audit Results

### 🔴 Critical Issues (X found)

**SQL Injection Vulnerability**
- **File:** src/api/users.ts:45
- **Code:** \`SELECT * FROM users WHERE id = ${userId}\`
- **Risk:** Database compromise, data theft
- **Fix:** Use parameterized query:
  ```typescript
  const query = 'SELECT * FROM users WHERE id = ?';
  await db.query(query, [userId]);
  ```

**Hardcoded API Key**
- **File:** src/config/api.ts:12
- **Code:** \`const API_KEY = "sk-1234-secret"\`
- **Risk:** Credential exposure
- **Fix:** Use environment variable:
  ```typescript
  const API_KEY = process.env.API_KEY;
  ```

### 🟠 High Issues (X found)

**Missing Authentication**
- **File:** src/routes/admin.ts:23
- **Risk:** Unauthorized access to admin functions
- **Fix:** Add authentication middleware

### 🟡 Medium Issues (X found)

**Weak Password Requirements**
- **File:** src/auth/password.ts:34
- **Risk:** Weak passwords allowed
- **Fix:** Enforce: min 12 chars, uppercase, lowercase, numbers, symbols

### 🟢 Low Issues (X found)

**Missing Security Headers**
- **File:** src/server.ts:10
- **Fix:** Add helmet.js for security headers

## Recommendations

1. Implement input validation library
2. Add automated security scanning to CI/CD
3. Enable dependency vulnerability scanning
4. Regular security training for team
5. Consider bug bounty program
```

## When to Use

- Before every PR merge
- Before production deployment
- After dependency updates
- Regular audits (monthly)
- When handling sensitive data
