# PKI-2FA — RSA + TOTP Two-Factor Authentication Microservice

**Project:** PKI-Based 2FA Microservice (Dockerized)  
**Author:** Shalini Jalla  
**Repository:** `pki-2fa`  
**Port:** `8080` (HTTP)

---

## Project Summary

This repository implements a secure, containerized microservice that demonstrates enterprise-grade security practices for two-factor authentication using:

- RSA-4096 (OAEP-SHA256) for encrypted seed transport
- RSA-PSS (SHA-256) for commit signatures
- TOTP (SHA-1, 30s period, 6 digits) for 2FA generation/verification
- Cron job to log TOTP codes every minute
- Docker multi-stage build and `docker-compose` for easy deployment
- Persistent volumes for `/data` (seed) and `/cron` (cron logs)

The project satisfies the assignment requirements: decrypting an instructor-provided encrypted seed, generating/verifying TOTP codes from the decrypted seed, cron logging, and providing cryptographic proof of work.

---
