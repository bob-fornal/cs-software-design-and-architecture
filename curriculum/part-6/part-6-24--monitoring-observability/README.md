# 24. Monitoring & Observability

**Part 6 — Asynchronous & Distributed Communication** · [Back to curriculum index](../../../README.md)

## One-sentence pitch
If you can't see what your system is doing right now, you'll find out it's broken from
your users instead of from a dashboard — monitoring and observability are how you buy
back that warning time.

## Learning objectives
- Can name the five monitoring categories (health, availability, performance,
  security, usage) and give a concrete metric example for each.
- Can instrument a service with request count, error rate, and p95 latency metrics
  plus a `/health` endpoint.
- Can explain the difference between a metric that's collected and a condition that
  triggers an alert, and why alert thresholds need to be chosen deliberately.
- Can define and wire up an alert condition, then simulate it to prove it fires.

## Session outline (~50 min)

| Segment | Time | Content |
|---|---|---|
| Hook: the outage nobody saw coming | 5 min | A service degrades slowly (latency creeps up) with no alert until users complain — the cost of not watching |
| The five monitoring categories | 10 min | Health, availability, performance, security, usage — with a concrete metric for each |
| Instrumentation | 12 min | What to measure and how: counters, gauges, histograms; request count, error rate, p95/p99 latency; the `/health` endpoint pattern |
| Visualization | 8 min | Turning raw metrics into dashboards that answer a question at a glance; the four golden signals (latency, traffic, errors, saturation) as a dashboard skeleton |
| Alerts | 10 min | Alerting on symptoms (user-facing) vs. causes; threshold selection; alert fatigue and why "alert on everything" is worse than no alerts |
| Wrap-up / homework framing | 5 min | From "we have metrics" to "we get paged before users notice" |

**Hook (5 min).** Walk through a service whose latency creeps up over an hour — no
crash, no error spike, just a slow bleed — until users start complaining. Ask: what
would have caught this an hour earlier? The answer motivates the whole session:
instrumentation you can see, and alerts that fire on the right signal.

**The five monitoring categories (10 min).**
- *Health:* is this specific instance/process up and able to do its job right now
  (a `/health` check, often including dependency checks).
- *Availability:* is the service reachable and successfully serving traffic over time
  (uptime percentage, often the basis of an SLA).
- *Performance:* how fast and how efficiently is it serving traffic (latency,
  throughput, resource utilization).
- *Security:* are there signs of abuse or compromise (failed auth spikes, unusual
  access patterns).
- *Usage:* who's using what, how much, and how — feeds capacity planning and product
  decisions, not just incident response.

**Instrumentation (12 min).** Introduce the three common metric shapes: counters
(monotonically increasing, e.g. total requests), gauges (a value that goes up or down,
e.g. current queue depth), and histograms (a distribution, e.g. request latency,
letting you compute p50/p95/p99). Cover the specific trio this session's homework
uses — request count, error rate, p95 latency — and why percentiles matter more than
averages (an average can look fine while 5% of users have a terrible experience). Then
the `/health` endpoint pattern: a lightweight endpoint that checks the process itself
and optionally its critical dependencies (DB reachable, queue reachable), returning
200 or 503 accordingly, used by load balancers and orchestrators to decide whether to
route traffic to this instance.

**Visualization (8 min).** Raw metrics in a time-series database (Prometheus, etc.)
aren't useful until they're on a dashboard that answers a question at a glance.
Introduce the four golden signals (from Google's SRE practice) — latency, traffic,
errors, saturation — as a minimal dashboard skeleton that applies to almost any
service. A dashboard's job is triage: is something wrong, and roughly where.

**Alerts (10 min).** The critical distinction: alert on symptoms that affect users
(error rate, latency) as the primary page, and use cause-level metrics (CPU, queue
depth) for diagnosis once you're already investigating — paging on every internal
metric leads to alert fatigue, where real pages get ignored because they're drowned in
noise. Threshold selection is a judgment call informed by historical data (what's
normal?) and business impact (what error rate actually hurts users?), not a
one-size-fits-all number.

**Wrap-up (5 min).** The goal isn't "we have metrics" — it's "we get paged before
users notice." Both homework assignments build toward that: first instrument and
visualize, then define alerts and prove they actually fire.

## Homework notes

### 1. Instrument a toy service and wire up a simple dashboard

**Goal:** Get hands-on with the core instrumentation trio (request count, error rate,
p95 latency) plus a health endpoint, and see them rendered somewhere visual.

**Approach / hints:**
- Pick any small service you already have (or a minimal one you stand up for this
  exercise) and add: a request counter, an error counter, and a latency histogram,
  incremented/observed on every request via middleware.
- Add a `/health` endpoint that returns 200 (and checks a dependency like a DB
  connection if you have one) or 503 if something's wrong.
- Expose the metrics for scraping (e.g. `prometheus_client`'s `/metrics` endpoint in
  Python, or `prom-client` in Node) and stand up a local Prometheus + Grafana stack
  (Docker Compose is the fastest path) to scrape and chart them — or, if you'd rather
  skip the infra, poll `/metrics` yourself on an interval and render a simple
  rolled-your-own chart (even a periodically-updated plot is fine).
- Generate some synthetic traffic (a loop of requests, some deliberately erroring) so
  the dashboard has real data to show.

**Starter example (Python, Flask + prometheus_client):**
```python
from flask import Flask
from prometheus_client import Counter, Histogram, generate_latest
import time

app = Flask(__name__)
REQUEST_COUNT = Counter("requests_total", "Total requests", ["status"])
REQUEST_LATENCY = Histogram("request_latency_seconds", "Request latency")

@app.route("/work")
def work():
    start = time.time()
    try:
        result = do_work()  # TODO: your toy service logic
        REQUEST_COUNT.labels(status="200").inc()
        return result
    except Exception:
        REQUEST_COUNT.labels(status="500").inc()
        raise
    finally:
        REQUEST_LATENCY.observe(time.time() - start)

@app.route("/health")
def health():
    return ("ok", 200) if dependency_ok() else ("unhealthy", 503)

@app.route("/metrics")
def metrics():
    return generate_latest()
```

**Definition of done:** A running service exposing request count, error rate (derived
from the status-labeled counter), and p95 latency (derived from the histogram), a
working `/health` endpoint, and a dashboard (Grafana or your own) that renders all
three from synthetic traffic.

### 2. Define, implement, and prove 3 alert conditions

**Goal:** Go from "metrics exist" to "the right people get paged" — define concrete
alert conditions and demonstrate each one actually fires under the condition it
targets.

**Approach / hints:**
- Using the service from homework 1, define three alert conditions: error rate > 5%
  (over some window, e.g. 1 minute), p95 latency > 500ms (over the same kind of
  window), and the `/health` check failing.
- If you're running Prometheus, implement these as real Prometheus alerting rules
  (`ALERT`/`rule` expressions) with Alertmanager, or a lightweight equivalent
  (a script that polls `/metrics` and `/health` and prints/logs/emails when a
  threshold is crossed) if you'd rather stay out of the full stack.
- For each condition, write a small script or manual trick that pushes the metric
  past the threshold on purpose (flood the service with slow requests to breach p95,
  force errors to breach the error-rate condition, kill a dependency to fail
  `/health`), and capture evidence the alert fired (a screenshot, a log line, an
  Alertmanager notification).
- Reset each condition afterward and confirm the alert clears.

**Starter example (Prometheus alerting rule, YAML):**
```yaml
groups:
  - name: toy-service-alerts
    rules:
      - alert: HighErrorRate
        expr: |
          sum(rate(requests_total{status="500"}[1m]))
          / sum(rate(requests_total[1m])) > 0.05
        for: 1m
        labels: { severity: page }
        annotations: { summary: "Error rate above 5%" }

      - alert: HighP95Latency
        expr: histogram_quantile(0.95, rate(request_latency_seconds_bucket[5m])) > 0.5
        for: 1m
        labels: { severity: page }
      # TODO: add a HealthCheckFailing alert driven by your /health probe
```

**Definition of done:** Three defined alert conditions (error rate, p95 latency,
health check), each wired to actually evaluate against live metrics, and for each one
a documented demonstration of the alert firing when the condition is deliberately
triggered and clearing once it's resolved.

## Further resources
- Free companion: Google, [SRE Book — Monitoring Distributed Systems](https://sre.google/sre-book/monitoring-distributed-systems/)
