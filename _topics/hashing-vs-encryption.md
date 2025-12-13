---
title: Hashing vs Encryption — Quick Comparison
category: Security
tags:
  - hashing
  - encryption
  - cryptography
summary: A concise quick-tick comparing hashing and encryption for security use-cases.
---

## Hashing

- Hashing is a one-way function that produces a fixed-size digest from arbitrary input.
- Common algorithms: SHA-256, SHA-3, BLAKE2, MD5 (deprecated).
- Use-cases: password verification (with salt), data integrity checks, content-addressing (e.g., git), deduplication.
- Properties:
  - Deterministic: same input → same digest.
  - Irreversible: you cannot recover original data from the hash.
  - Collision-resistant: hard to find two different inputs with same hash.

## Encryption

- Encryption is a reversible process to protect confidentiality; encrypted data can be decrypted if you have the key.
- Common algorithms: AES (symmetric), RSA & Elliptic-Curve (asymmetric).
- Use-cases: protecting data at rest, data in transit (TLS), encrypted backups.
- Properties:
  - Reversible with the key.
  - Requires secure key management.
  - Can provide confidentiality and (with MACs) integrity.

## When to use what

- Use hashing when you only need to verify data or store a digest (e.g., passwords, checksums).
- Use encryption when you need to keep the original data secret but retrievable for authorized parties.

## Practical tips

- For passwords, use a slow hashing algorithm with salt (bcrypt, scrypt, Argon2) rather than raw SHA-*.
- Always verify the authenticity/integrity of encrypted data (e.g. use authenticated encryption modes like AES-GCM).
- Properly manage keys and rotate them as needed when using encryption.

## Short Summary

Hashing is for irreversible verification and identification; encryption is for reversible confidentiality using keys.