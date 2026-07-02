---
title: glibc vs musl — C Standard Library Comparison
description: - [Overview](#overview)
---

# glibc vs musl — C Standard Library Comparison

> **Last updated:** 2026-06-07
> **glibc:** GNU C Library v2.40+ — https://www.gnu.org/software/libc/
> **musl:** musl libc v1.2.5+ — https://musl.libc.org/
> **License comparison:** LGPL (glibc) vs MIT (musl)

## Table of Contents

- [Overview](#overview)
  - [What is glibc?](#what-is-glibc)
  - [What is musl?](#what-is-musl)
- [Architecture & Design Philosophy](#architecture--design-philosophy)
  - [Key Size Comparison](#key-size-comparison)
- [Performance](#performance)
  - [Strengths of glibc](#strengths-of-glibc)
  - [Strengths of musl](#strengths-of-musl)
  - [Real-World Impact](#real-world-impact)
- [Binary Compatibility](#binary-compatibility)
  - [Symbol Versioning](#symbol-versioning)
  - [Dynamic Library Loading](#dynamic-library-loading)
  - [Lazy Binding](#lazy-binding)
  - [ABI Differences](#abi-differences)
- [Static Linking](#static-linking)
  - [musl Advantages](#musl-advantages)
  - [glibc Static Linking Disadvantages](#glibc-static-linking-disadvantages)
- [Docker & Container Image Size](#docker--container-image-size)
  - [Image Size Comparison](#image-size-comparison)
  - [Why Alpine is Smaller](#why-alpine-is-smaller)
  - [The Docker Trade-off](#the-docker-trade-off)
- [DNS Resolution](#dns-resolution)
  - [glibc DNS](#glibc-dns)
  - [musl DNS](#musl-dns)
  - [Practical Impact for Go/Rust/Python](#practical-impact-for-gorustpython)
- [Threading Model](#threading-model)
  - [Default Thread Stack Size](#default-thread-stack-size)
  - [Thread Cancellation](#thread-cancellation)
  - [Mutex/Condvar Correctness](#mutexcondvar-correctness)
- [Memory Allocation](#memory-allocation)
  - [glibc (ptmalloc2)](#glibc-ptmalloc2)
  - [musl (mallocng)](#musl-mallocng)
  - [Practical Implications](#practical-implications)
- [Locale Handling](#locale-handling)
  - [glibc Locale](#glibc-locale)
  - [musl Locale](#musl-locale)
- [Distro Ecosystem](#distro-ecosystem)
  - [glibc Distributions](#glibc-distributions)
  - [musl Distributions](#musl-distributions)
- [Go & musl](#go--musl)
- [Rust & musl](#rust--musl)
- [Practical Pain Points & Gotchas](#practical-pain-points--gotchas)
  - [DNS Issues](#dns-issues)
  - [Threading Surprises](#threading-surprises)
  - [Locale Surprises](#locale-surprises)
  - [Dynamic Loading](#dynamic-loading)
  - [Build System Issues](#build-system-issues)
  - [iconv Limitations](#iconv-limitations)
- [Standards & Undefined Behavior](#standards--undefined-behavior)
- [When to Choose Which](#when-to-choose-which)
  - [Choose musl when](#choose-musl-when)
  - [Choose glibc when](#choose-glibc-when)
- [Quick Reference Table](#quick-reference-table)
- [Summary](#summary)

---

## Overview

**glibc** (GNU C Library) and **musl** are the two most common C standard library implementations for Linux. Every dynamically-linked Linux program uses one of them — they provide the core APIs for file I/O, networking, threading, memory allocation, string processing, and more.

### What is glibc?

- The **de facto standard** C library on Linux — used by Ubuntu, Debian, Fedora, RHEL, Arch, and almost all desktop/server distributions
- Developed by the GNU Project since 1988
- **Monolithic + modular**: split across multiple shared libraries (`libc.so.6`, `libm.so.6`, `libpthread.so.0`, `librt.so.1`, `libdl.so.2`, plus NSS and iconv modules)
- **Maximizes performance** via hand-tuned assembly (AVX2, SSE4.2), heavy inlining, and complex algorithms
- **Lenient with standards**: prioritizes backward compatibility over strict POSIX/ISO conformance

### What is musl?

- A **lightweight, standards-focused** alternative, used by Alpine Linux and popular in container/embedded environments
- Created by Rich Felker (etalabs) in 2011
- **Single monolithic `libc.so`**: everything in one shared object (~527KB vs glibc's ~7.9MB total)
- **Simplicity-first**: simple, correct algorithms over complex ones. Code is dense but readable.
- **Standards-conformance driven**: strict adherence to ISO C and POSIX. Rejects GNU extensions that conflict with standards.
- **Static linking friendly**: minimal overhead — a static hello world with `printf` is ~13KB vs glibc's ~662KB

---

## Architecture & Design Philosophy

| Aspect | glibc | musl |
|--------|-------|------|
| **Structure** | Multiple shared objects | Single `libc.so` |
| **License** | LGPL (with exceptions) | MIT |
| **Design goal** | Maximum performance + compatibility | Correctness + simplicity + size |
| **Standard conformance** | Lenient (GNU extensions, BSD legacy) | Strict (POSIX, ISO C) |
| **Static linking** | Discouraged, fragile | First-class, tiny binaries |
| **External modules** | NSS, iconv, locale via `.so` | Everything built-in |
| **Maintainers** | GNU Project team | Rich Felker + community |

### Key Size Comparison

| Metric | musl | glibc |
|--------|------|-------|
| Complete `.a` set | 426 KB | 2.0 MB |
| Complete `.so` set | 527 KB | 7.9 MB |
| Static hello (`printf`) | 13 KB | 662 KB |
| Min static program | 1.8 KB | 662 KB |
| Dynamic overhead (min dirty) | 20 KB | 48 KB |
| Static overhead (min dirty) | 8 KB | 28 KB |

*Source: etalabs.net/compare_libcs*

---

## Performance

### Strengths of glibc

- **String/memory operations**: `strlen`, `strchr`, `strstr`, `memcpy` use hand-tuned SIMD (AVX2, SSE4.2) — often **2-5x faster** than musl
- **Malloc**: ptmalloc2 has excellent single-threaded throughput
- **Pthread creation**: ~0.142µs vs musl's ~0.248µs

### Strengths of musl

- **UTF-8 decoding**: significantly faster (~0.073µs vs glibc's ~0.351µs)
- **Process startup**: ~446µs vs glibc's ~864µs dynamic startup
- **Multi-threaded allocation**: better under shared contention (0.050µs vs 0.062µs)
- **Stdio unlocked**: competitive with glibc for I/O operations

### Real-World Impact

For most application code, the performance gap is **negligible**. Bottlenecks are usually in application logic, I/O, database queries, or networking — not libc string/memory functions. The difference matters most in **microbenchmarks** and tight loops calling libc functions millions of times.

---

## Binary Compatibility

### Symbol Versioning

- **glibc**: Full GNU `symver` — binaries compiled against glibc 2.31 may not run on glibc 2.28 (forward compatibility NOT guaranteed). Backward compatibility IS guaranteed (binary from 1998 still runs).
- **musl**: No symbol versioning. ABI is stable within the same major release. Guarantees both backward AND forward compatibility.

### Dynamic Library Loading

- **glibc**: Reference-counted `dlopen`/`dlclose`. Libraries can be unloaded, constructors/destructors run on each load/unload.
- **musl**: `dlclose` is a **no-op**. Libraries stay loaded for process lifetime. Constructors run once, destructors only on process exit.

### Lazy Binding

- **glibc**: Supports lazy binding (PLT resolution deferred until first call). Reduces startup time for large programs but introduces fragility.
- **musl**: No lazy binding. All symbols resolved at load time. More robust — no "unresolved symbol" crashes at arbitrary call points.

### ABI Differences

| Difference | glibc | musl |
|-----------|-------|------|
| **`regoff_t`** (64-bit) | 32-bit (non-conforming) | 64-bit (POSIX conforming) |
| **`setjmp`/`longjmp`** | Saves/restores signal mask | Never saves (POSIX conforming) |
| **Default locale** | C (pseudo-ASCII) | C.UTF-8 |
| **`struct pthread_attr_t`** | Standard layout | Different layout |

**Cross-linking constraint**: You **cannot** mix glibc-linked and musl-linked shared libraries in the same process.

---

## Static Linking

### musl Advantages

- **True standalone binaries**: zero external dependencies — no libc, no ld-linux, no NSS modules, no locale files
- **Tiny binaries**: minimal static binary under 10KB; with threads under 50KB
- **MIT license**: no LGPL static linking encumbrances
- **Deployment simplicity**: single binary, any Linux kernel of the right arch
- **No runtime library search**: LD_LIBRARY_PATH, rpath, ldconfig — all irrelevant

### glibc Static Linking Disadvantages

- **Strongly discouraged** by maintainers — fragile, can cause subtle issues (NSS not working, locale not loading, `dlopen` unavailable)
- **Large binary size**: even trivial static program is ~662KB due to internal coupling
- **LGPL concerns**: requires providing object files for relinking

> **musl is the superior choice for static linking, period.** This is why it dominates in containers and embedded Linux.

---

## Docker & Container Image Size

### Image Size Comparison

| Image | Size | Notes |
|-------|------|-------|
| `alpine:3.21` | ~7 MB | musl + busybox + apk |
| `debian:bookworm-slim` | ~80 MB | glibc + coreutils + dpkg |
| `ubuntu:24.04` | ~78 MB | glibc + more utilities |
| `distroless/base` | ~25 MB | glibc-based, minimal |
| `distroless/static` | ~2 MB | non-glibc, for static binaries |

### Why Alpine is Smaller

- **musl itself is smaller**: ~527KB .so vs glibc's ~7.9MB
- **busybox instead of coreutils**: single ~1MB binary replaces dozens of GNU utilities
- **apk package manager**: simpler than dpkg/apt, smaller database
- **No locales, no man pages**: smaller default install

### The Docker Trade-off

| Approach | Pros | Cons |
|----------|------|------|
| **Alpine + musl** | ~7MB base, small attack surface, good for static Go/Rust | Compatibility issues with prebuilt glibc binaries |
| **Debian slim + glibc** | Maximum compatibility, predictable behavior | ~80MB base, larger attack surface |

For a statically compiled Go or Rust application:
- **Distroless static or scratch**: ~2-20MB total
- **Alpine-based**: ~8-30MB total
- **Debian slim**: ~80-100MB total

---

## DNS Resolution

### glibc DNS

- Uses **NSS** (Name Service Switch) via `/etc/nsswitch.conf` — supports files, dns, systemd-resolved, LDAP, mDNS, sssd
- **Sequential** nameserver queries: tries each nameserver from `/etc/resolv.conf` in order
- Supports IDN (internationalized domain names)
- DNS over TCP since early versions
- AI_ADDRCONFIG and other socket extension flags

### musl DNS

- **Parallel** nameserver queries: queries ALL configured nameservers simultaneously, accepts the first response. Faster and more resilient.
- **No NSS**: no nsswitch.conf support. Only `/etc/hosts` and DNS from `/etc/resolv.conf`.
- **No IDN support** (yet) — programs must convert to Punycode themselves
- **Limited search behavior**: names with enough dots only tried literally (no fallback to search)
- **search lines over 256 chars** are silently ignored
- **DNS over TCP added in musl 1.2.4** — prior versions could not handle large DNS responses (DNSSEC, DKIM)

### Practical Impact for Go/Rust/Python

| Language | Uses C lib's `getaddrinfo`? | Impact |
|----------|---------------------------|--------|
| **Go** | **No** (pure Go resolver by default) | Musl DNS is irrelevant — Go resolves DNS itself |
| **Rust** | **No** (pure Rust resolver via `std::net`) | Musl DNS is irrelevant |
| **Python** | **Yes** (via `socket.getaddrinfo`) | Musl's parallel DNS is faster; no NSS/LDAP |
| **Node.js** | **Yes** (via `getaddrinfo`) | Same as Python |
| **Ruby** | **Yes** | Same as Python |

**Key takeaway**: For Go and Rust apps, DNS behavior is identical on glibc and musl. For interpreted languages, musl's DNS is faster (parallel) but can't integrate with systemd-resolved or LDAP.

---

## Threading Model

### Default Thread Stack Size

| Library | Default Stack |
|---------|--------------|
| **glibc** | 2-10 MB (based on `RLIMIT_STACK` of main thread) |
| **musl** | 128 KB (80KB prior to 1.1.21) |

**Practical impact**: musl's smaller default stack is great for programs with thousands of threads but can cause **stack overflows** in code that allocates large stack variables or has deep recursion. Use `pthread_attr_setstacksize()` to increase it.

### Thread Cancellation

- **glibc**: Implements cancellation as a C++ exception. Cleanup handlers AND C++ destructors both run (technically undefined behavior, works in practice).
- **musl**: Strict POSIX. Cancellation does NOT unwind C++ stack — destructors will not run. Only POSIX cleanup handlers run.

> **If you use `pthread_cancel` in C++ code on musl, destructors will leak.**

### Mutex/Condvar Correctness

musl was the **first** Linux libc to have correct implementations of:
- Mutexes safe inside reference-counted objects
- Condition variables without "stolen wakeup" bugs
- Thread cancellation without race conditions (double-close, resource leaks)

glibc has since fixed many of these, but musl got them right from the start.

---

## Memory Allocation

### glibc (ptmalloc2)

- Derived from dlmalloc with per-thread arenas
- Complex heuristics for bin management
- Can grow arena count up to 2x CPU count
- Known for memory fragmentation under certain patterns

### musl (mallocng)

- Simple design: all allocations via `mmap` (no `sbrk`)
- Each allocation is a separate mmap slot (or small group)
- Very low memory waste but higher number of mmap calls
- Predictable behavior with no hidden fragmentation
- Strictly reports ENOMEM on failure — never calls `abort()`

### Practical Implications

- glibc has better **peak throughput** for malloc-intensive workloads
- musl has more **predictable and bounded** memory usage
- musl is safer under memory pressure (never aborts)
- If you see `mmap` count increasing rapidly in strace on musl, that's expected

---

## Locale Handling

### glibc

- Requires locale data installed on system (`locale-gen`, `/usr/lib/locale/`)
- Default C locale is pseudo-ASCII
- Comprehensive `localedef` with thousands of locale definitions
- Full `iconv` with `//TRANSLIT` and `//IGNORE` support
- Locale-dependent behavior for many functions (`toupper`, `strcoll`)

### musl

- **No external locale files needed** — built-in minimal locale data
- Default locale is **C.UTF-8** (not just "C")
- **Strict UTF-8 validation**: rejects surrogates, overlong sequences, and 5/6 byte sequences (glibc accepts them)
- `iconv` built-in, compact but less comprehensive:
  - No `//TRANSLIT` support
  - Legacy East Asian encodings limited as destination charset
  - `//IGNORE` is supported

**Practical impact**: musl makes UTF-8 "just work" without locale generation. Great for containers. If you need complex locale-specific behavior (e.g., Turkish `i`/`İ` case conversion), glibc is more comprehensive.

---

## Distro Ecosystem

### glibc Distributions

Debian, Ubuntu, Fedora, RHEL, CentOS, Arch Linux, openSUSE, Gentoo (default), Slackware, Void Linux (option), Mint, Kali, Rocky, AlmaLinux

### musl Distributions

Alpine Linux (by far the most deployed), Void Linux (option), Adélie Linux, PostmarketOS, OpenWrt, Sabotage Linux, Talos Linux

---

## Go & musl

Go's runtime uses **direct Linux syscalls** — NOT the C library:

```bash
# Pure Go — works everywhere, smallest image
CGO_ENABLED=0 GOOS=linux go build -o app .

# cgo on Alpine — needs build-base
# Dockerfile: RUN apk add --no-cache build-base
# Build: CGO_ENABLED=1 GOOS=linux go build
```

**Compatibility**: Excellent. Go statically links everything by default. `CGO_ENABLED=0` binary built on any Linux runs everywhere.

**Known issues:**
- Race detector (`-race`) requires glibc — not supported on musl (as of Go 1.22)
- Some cgo packages use glibc-internal headers
- Use `netgo` build tag for pure Go DNS resolver (recommended for musl)

---

## Rust & musl

Rust provides **Tier 2** musl targets with **default static linking** (`crt_static_default = true`):

```bash
rustup target add x86_64-unknown-linux-musl
cargo build --target x86_64-unknown-linux-musl --release
# Produces fully static binary
```

**Available musl targets:**
- `x86_64-unknown-linux-musl` (targets musl 1.2.5)
- `aarch64-unknown-linux-musl`
- `i686-unknown-linux-musl`
- `arm*-unknown-linux-musleabi[hf]`
- `riscv64gc-unknown-linux-musl`

**Known issues:**
- Some crates with C dependencies may need musl-compatible C libraries
- `jemalloc` may interact differently with musl vs glibc

---

## Practical Pain Points & Gotchas

### DNS Issues
- **No NSS**: systemd-resolved, nscd, sssd, LDAP auth won't work
- **No mDNS**: `.local` hostname resolution via Avahi doesn't work
- **search list >256 chars** silently dropped
- **No `/etc/resolv.conf` `sortlist`** support

### Threading Surprises
- **128KB default stack** can cause segfaults in code assuming large stacks
- **C++ cancellation**: `pthread_cancel` in musl does NOT run C++ destructors

### Locale Surprises
- **Strict UTF-8 validation** can reject data glibc accepts (5/6 byte sequences, surrogates)
- **`mbstowcs`** may reject data glibc silently accepts

### Dynamic Loading
- **`dlclose` is a no-op** — memory from libraries never freed
- **No lazy binding** — all symbols resolved at load time
- **No `dlvsym`** — symbol versioning not supported

### Build System Issues
- Many `configure` scripts and Makefiles assume glibc
- `__GLIBC__` guards in source code skip musl-compatible code
- Some inline assembly / GNU extensions may not compile
- `getopt` processes options differently (no argv permutation)

### iconv Limitations
- `//TRANSLIT` not supported
- Fewer destination charset conversions
- Non-representable chars replaced with `*` (not `EILSEQ`)

---

## Standards & Undefined Behavior

musl is **significantly stricter** than glibc about undefined behavior:

| Area | glibc | musl |
|------|-------|------|
| Resource exhaustion | May `abort()` | Reports failure |
| Thread cancellation | Additional guarantees via exceptions | Strict POSIX |
| `setjmp` signal mask | Saves/restores by default | Never saves (POSIX) |
| `printf` format specifiers | Accepts non-standard aliases | Returns error on invalid |
| UTF-8 overlong sequences | Some accepted | All rejected |
| UTF-8 surrogates | Some accepted | All rejected |
| `iconv` non-representable | Returns `EILSEQ` | Replaces with `*` (POSIX) |

**Philosophy**: glibc prioritizes "works on existing code". musl prioritizes "correct per the specification".

---

## When to Choose Which

### Choose musl when

- **Static linking** — truly standalone binaries
- **Container image size** matters — Alpine's 7MB
- **Embedded/resource-constrained** systems
- **Security-sensitive** environments — smaller codebase, fewer CVEs
- **Go or Rust static binaries** — natural pairing
- **Correctness** over compatibility
- **High thread counts** — 128KB default stack
- **Greenfield projects** with no glibc dependencies

### Choose glibc when

- **Maximum compatibility** — prebuilt binaries, proprietary software
- **C++ with thread cancellation** — musl doesn't unwind destructors
- **Need NSS integration** — LDAP, AD, systemd-resolved, mDNS
- **Need complex locale behavior** — full localization
- **Running Java** — JVM heavily optimized for glibc
- **Python with C extensions** — SciPy, PyPI packages assume glibc
- **Performance-critical string processing** — glibc's SIMD is faster
- **Legacy/vendor software** — Oracle DB, MATLAB
- **Need race detector** in Go (`-race` requires glibc)

---

## Quick Reference Table

| Feature | glibc | musl |
|---------|-------|------|
| Size (.so) | ~7.9 MB total | ~527 KB shared |
| Static hello world | ~662 KB | ~13 KB |
| License | LGPL | MIT |
| Default locale | C (pseudo-ASCII) | C.UTF-8 |
| Default thread stack | 2-10 MB | 128 KB |
| DNS resolution | Sequential, NSS-based | Parallel, no NSS |
| Lazy binding | Yes | No |
| `dlclose` | Reference-counted unload | No-op |
| Symbol versioning | Full GNU | Default version only |
| `setjmp`/`longjmp` | Saves signal mask (BSD) | Never saves (POSIX) |
| Regex `regoff_t` (64-bit) | 32-bit (non-conforming) | 64-bit (conforming) |
| iconv `//TRANSLIT` | Yes | No |
| UTF-8 strictness | Lenient | Strict |
| errno from math | Yes (`MATH_ERRNO`) | No (only `MATH_ERREXCEPT`) |
| Static linking | Discouraged, large | Encouraged, tiny |
| Process startup | ~864 µs | ~446 µs |
| Memory allocation | ptmalloc2 (complex) | mallocng (mmap-based) |
| NSS support | Yes | No |
| PAM support | Yes | No |
| Go compatibility | Excellent (default) | Excellent (pure Go) |
| Rust compatibility | Excellent | Excellent (native targets) |
| Alpine Docker base | Not used | ~7 MB |
| Debian/Ubuntu base | ~80 MB | Not used |

---

## Summary

The choice between glibc and musl depends on your priorities:

- **For maximum compatibility** with existing software, databases, and middleware → **glibc**
- **For static binaries, small containers, and embedded systems** → **musl**
- **For Go and Rust applications** → either works, but musl gives you smaller static binaries and Alpine images
- **For Python/Node/Ruby with C extensions** → glibc is safer (most wheels are precompiled for glibc)

For most users building cloud-native applications in Go or Rust, **musl on Alpine** is the sweet spot: tiny images, single-binary deployments, and no compatibility issues since the standard library is statically linked.

For traditional server applications, middleware, or anything that needs to run vendor-provided binaries, **glibc on Debian/Ubuntu** is the safer choice.

---

## Related

- [nektos/act — Run GitHub Actions Locally](act.md) — runs on glibc typically
- [Taskfile.dev — Modern Task Runner](taskfile.md) — Go binary, glibc or musl
- [Dagger — A Better Way to Ship](dagger.md) — CI/CD platform, runs in containers
- [musl official site](https://musl.libc.org/)
- [GNU C Library](https://www.gnu.org/software/libc/)
- [musl Functional Differences from glibc](https://wiki.musl-libc.org/functional-differences-from-glibc.html)
- [Comparison of C/POSIX Library Implementations](https://www.etalabs.net/compare_libcs.html)
