# Architecture Decision Records

## ADR-001: No Staging Environment (Accepted Risk)
**Date:** 2026-05-10
**Status:** Accepted

**Context:**
211 is a learning project running on a single app droplet. A staging
environment would require a second droplet mirroring prod, adding cost
and maintenance overhead.

**Decision:**
Deploy directly to production. Accept the risk of untested changes
hitting prod.

**Consequences:**
- Every push is a prod deploy — changes must be verified locally first
- No rollback mechanism beyond git revert + redeploy
- Manual git pull required on server until CI/CD ownership is resolved

**Future:**
When 211 moves toward a real service, implement:
- Staging droplet mirroring prod
- Blue/green deployment via nginx upstream switching
- Automated smoke tests post-deploy

## ADR-002: cicd-runner Repo Ownership (Deferred)
**Date:** 2026-05-10
**Status:** Deferred

**Context:**
The repo at /home/deploy/211 is owned by the deploy account. The
cicd-runner service account runs the pipeline but cannot write to
the repo, breaking automatic git pull.

**Decision:**
Manual git pull on server after each push as workaround.

**Future:**
Transfer repo ownership to cicd-runner, add deploy to cicd-runner
group for manual access.
