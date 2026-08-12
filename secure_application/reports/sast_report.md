# SAST Security Analysis Report

## 1. Project Details

| Item | Details |
|---|---|
| Group Number | 14 |
| Application | Library Management System |
| Language | Python |
| SAST Tool | Semgrep |
| Application Type | Console-based |

---

## 2. Vulnerabilities Tested

The application was intentionally developed with three vulnerabilities:

1. SQL Injection
2. Improper Input Validation
3. Missing Authentication

---

## 3. Before Fixing Vulnerabilities

The vulnerable application was scanned using Semgrep.

Command:

```bash
semgrep scan --config secure_application/sast/custom_rules.yml secure_application/src/library_vulnerable.py

