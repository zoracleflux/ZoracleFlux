# Strongest zero-cost reference architecture

This is a staged architecture, not a claim that a production service is
already deployed.

```text
Users
  |
  |  static docs/release links
  v
GitHub Pages (public, static, $0)
  ^
  | Pages workflow after CI
GitHub repository (Issues, Projects, Discussions, Releases)
  |
  +-- Actions: CI, CodeQL, Dependabot, Scorecard, export, best-effort probe
  |       |
  |       +-- short-retention artifact staging copy
  |       +-- OIDC -> external role (optional)
  |                         |
  |                         +-- encrypted Cloudflare R2 export (free quota)
  |
  +-- optional HTTP runtime (not Pages/Actions)
          Cloudflare Workers Free JS/TS adapter (workers.dev)
             +-- Worker secrets / optional D1 metadata / optional R2 objects
             +-- UptimeRobot or Better Stack external checks
             +-- PagerDuty Free human schedule (up to 5 users)
```

## Recommended zero-cost stages

### Stage 0: verified local pilot

Use RC3's offline CLI, SQLite evidence, backup/restore and threat checks. It
uses no credentials, endpoint, domain or network. This is the only stage
already validated in this workspace.

### Stage 1: public project operations without runtime

Copy the base overlay. Turn on Pages, Issues, Projects, Discussions,
Dependabot, CodeQL and Scorecard. Require CI/security checks and review. Use
Releases for package assets and Actions artifacts for short-lived export
staging. This stage is free for a public repository but still needs a
maintainer.

### Stage 2: free-quota edge adapter (optional)

Implement a separately reviewed JavaScript/TypeScript adapter for a narrow
health or read-only operation in Cloudflare Workers Free. The included
`cloudflare-worker-reference` responds only with a deterministic health
document; it does **not** run ZoracleFlux or accept customer input. Use a
workers.dev URL while evaluating; a custom domain is optional but requires
domain ownership/DNS.

Store runtime secrets in Worker secrets, not source. A GitHub deployment needs
either a protected Cloudflare API token environment secret or a vendor
integration. Cloudflare Workers has no assumed GitHub OIDC exchange in this
bundle, so do not claim secretless deployment.

### Stage 3: backup and human response

Send encrypted exports to R2 within the 10 GB/1M Class A/10M Class B free
allowances. Create an UptimeRobot or Better Stack monitor against a real
health URL. Configure PagerDuty Free's one schedule and one escalation policy
with real people. Link alerts to an incident issue. Run a restore drill.

## The unavoidable boundary

The first non-local request crosses a real-human boundary. At minimum someone
must create and own:

1. a GitHub repository and maintainer permissions;
2. a cloud account for a Worker/R2, or another external host;
3. a real endpoint and its health semantics;
4. a secret/trust policy and rotation owner;
5. a domain/DNS/TLS owner if a custom URL is required;
6. an independent monitor account;
7. an on-call rota with humans who can receive and acknowledge alerts.

Payment becomes unavoidable when a quota is exceeded, a provider requires a
paid plan for the needed CPU/storage/retention/custom domain/SLA, or a
provider's free plan is not eligible. A domain can be avoided temporarily with
`github.io`/`workers.dev`, but a trustworthy branded production service
normally requires domain ownership and renewal cost. No provider SLA,
customer-data contract, compliance approval, or production availability is
implied by a free tier.
