# 33. Operations & DevOps Knowledge

**Part 8 — The Software Architect Role** · [Back to curriculum index](../../../README.md)

## One-sentence pitch
An architecture that only works on a whiteboard isn't an architecture yet — an architect who understands how their design actually gets built, deployed, and kept running (containers, IaC, CI/CD, serverless tradeoffs) designs systems that survive contact with production.

## Learning objectives
- Can containerize an application and explain what problem the container boundary actually solves (environment parity, not just "packaging").
- Can write or read a basic Infrastructure-as-Code definition and explain why IaC beats manual/console-driven provisioning for anything beyond a throwaway experiment.
- Can describe the tradeoffs between a long-running containerized service and a serverless function for a given workload (cold start, cost model, operational complexity).
- Can describe what a CI/CD pipeline does stage by stage (build, test, deploy) and why automating the path to production reduces risk rather than just saving time.
- Can name the core Linux/Unix concepts (processes, filesystem permissions, standard streams, basic networking) an architect needs to reason about where their design will actually run.

## Session outline (~45–60 min)

| Segment | Time | Content |
|---|---|---|
| Hook: the architecture that only exists on paper | 5 min | Contrast a diagram-only "architecture" with the same design once someone has to actually build, ship, and operate it. Land on: an architect who can't reason about the operational reality of their own design will get overruled by whoever can. |
| Linux/Unix fundamentals | 8 min | Just enough grounding: processes and how they're isolated, the filesystem and permission model, standard streams (stdin/stdout/stderr) as the universal interface most tooling assumes, and basic networking (ports, sockets) as the substrate everything above is built on. This is the layer containers and cloud services are ultimately built from — not trivia. |
| Containers | 8 min | A container packages an app with its dependencies so it runs the same in dev, CI, and production — the problem being solved is "works on my machine," not just smaller VMs. Distinguish an image (a built artifact) from a container (a running instance of that image). Briefly mention orchestration (Kubernetes, ECS) as the layer that manages many containers across many machines — out of scope to teach here, but architects need to know it exists and why. |
| Infrastructure as Code & cloud providers | 8 min | IaC: describing infrastructure (servers, networks, databases) as versioned, reviewable text instead of manual console clicks — the same reasons you version application code apply to infrastructure (reproducibility, review, rollback). Briefly survey the major cloud providers (AWS, Azure, GCP) as roughly-equivalent building blocks (compute, storage, managed databases, networking) with different names and pricing, not fundamentally different concepts. |
| Serverless & CI/CD | 12 min | Serverless: no server to manage, billed per invocation, but subject to cold starts and a different cost model (can be cheaper at low/spiky volume, more expensive at sustained high volume) versus an always-on container. Walk through a CI/CD pipeline stage by stage: build (compile/package), test (automated gates before anything ships), deploy (push to an environment) — and why each stage exists to catch a specific class of problem before a human does. |
| Service mesh & wrap-up | 8-10 min | Service mesh (e.g., Istio, Linkerd) as infrastructure-level handling of service-to-service concerns (retries, mTLS, observability) that would otherwise be duplicated in every service's code — connect back to Part 7's reliability patterns (circuit breaker, bulkhead) as things a mesh can provide for free at the infrastructure layer. Introduce the homework: containerize + IaC, wire up CI/CD, and compare containerized vs. serverless deployment of the same logic. |

## Homework notes

### 1. Containerize an app and write its IaC definition
> Containerize an application from a prior module (Dockerfile) and write an Infrastructure-as-Code definition (Terraform, Pulumi, or even a documented CLI script) that provisions what it needs to run.

- **Goal:** Tests whether students can translate "an app that runs on my machine" into "an app that runs anywhere, reproducibly" — the foundational DevOps skill everything else in this topic builds on.
- **Approach / hints:** Start from an app built in an earlier module. Write a Dockerfile that installs dependencies and runs it, and actually build and run the image locally before calling it done. For the IaC piece, don't feel obligated to reach for a full cloud deployment if that's out of budget/scope — a well-documented CLI script (or a Terraform config targeting a free-tier provider, or even a local tool like a Docker Compose file provisioning a database alongside the app) satisfies the spirit of the assignment: infrastructure described in versioned, re-runnable text rather than manual steps.
- **Starter example:**
```dockerfile
FROM node:20-slim
WORKDIR /app
COPY package*.json ./
RUN npm ci --omit=dev
COPY . .
EXPOSE 3000
CMD ["node", "server.js"]
```
```hcl
# main.tf — minimal example: provision a compute instance to run the container
resource "aws_instance" "app" {
  ami           = "ami-xxxxxxxx"
  instance_type = "t3.micro"
  tags = { Name = "prior-module-app" }
}
```
- **Definition of done:** A working Dockerfile that builds and runs the app locally, plus a committed IaC definition (or thoroughly documented provisioning script) that someone else could run to stand up whatever the container needs (compute, a database, networking) without manual console steps.

### 2. CI/CD pipeline for the containerized app
> Set up a CI/CD pipeline (GitHub Actions or similar) that builds, tests, and deploys that containerized app automatically on push to main.

- **Goal:** Tests whether students can automate the path from commit to running system, and understand why each stage (build, test, deploy) exists as a gate rather than a formality.
- **Approach / hints:** Build on homework 1's Dockerfile. A minimal real pipeline: on push to main, build the Docker image, run whatever automated tests exist (even a handful), and deploy — deployment can be as simple as pushing the image to a registry, or redeploying to wherever homework 1's IaC provisioned, depending on time/budget. Make the test stage a genuine gate: intentionally break a test once and confirm the pipeline stops before deploy.
- **Starter example:**
```yaml
name: CI/CD
on:
  push:
    branches: [main]
jobs:
  build-test-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build image
        run: docker build -t app:${{ github.sha }} .
      - name: Run tests
        run: docker run app:${{ github.sha }} npm test
      - name: Deploy
        if: success()
        run: echo "deploy step — push to registry / trigger redeploy"
```
- **Definition of done:** A committed pipeline config that runs automatically on push to main, visibly builds and tests the app, and demonstrably blocks deployment when a test fails (shown with at least one intentionally-broken-then-fixed run).

### 3. Compare containerized vs. serverless for the same logic
> Deploy the same piece of business logic as both a long-running containerized service and a serverless function; compare cold start, cost model, and operational complexity.

- **Goal:** Tests whether students can reason about deployment-model tradeoffs concretely, with real numbers, instead of reciting "serverless is for spiky workloads" without ever having measured it.
- **Approach / hints:** Pick one small, self-contained piece of logic (a single endpoint or function is enough — e.g., "calculate order total" or "resize an image"). Deploy it once in a container (any host, even local, timed consistently) and once as a serverless function (a provider's free tier — AWS Lambda, Cloudflare Workers, etc. all have one). Measure cold-start latency on the serverless version (first request after idle) vs. the container's always-warm response time. Write the cost comparison as a model (cost per request at low volume vs. at sustained high volume), not necessarily a real bill — the point is understanding the shape of the tradeoff.
- **Definition of done:** The same logic running in both deployment models, with measured cold-start numbers for the serverless version and a written comparison covering cost model and operational complexity (what you had to manage in each case) — ending in a stated recommendation for which fits which kind of workload and why.

## Further resources
- Free companion: freeCodeCamp, [DevOps articles & tutorials](https://www.freecodecamp.org/news/tag/devops/)
