from __future__ import annotations

from typing import List, TypedDict

from django.utils.translation import gettext_lazy as _


class TopicSection(TypedDict, total=False):
    title: str
    description: str
    items: List[str]


class Topic(TypedDict, total=False):
    slug: str
    title: str
    summary: str
    tagline: str
    sections: List[TopicSection]
    url_name: str


TOPICS: List[Topic] = [
    {
        "slug": "foundations",
        "title": _("Core Python Foundations"),
        "summary": _(
            "Master everyday syntax, built-in types, and workflows so the rest of the curriculum feels natural."
        ),
        "tagline": _("Language core"),
        "sections": [
            {
                "title": _("Syntax & keywords"),
                "items": [
                    _("Function and class declarations, docstrings, annotations, and return semantics."),
                    _("Flow control keywords including if/elif/else, for/while, match/case, and comprehension forms."),
                    _("Functional helpers such as lambda, yield, async/await, and context-aware 'with' blocks."),
                ],
            },
            {
                "title": _("Data & composite types"),
                "items": [
                    _("Primitive numbers, bools, decimals, fractions, and portable text/bytes handling."),
                    _("Built-in containers (list, tuple, dict, set) with slicing semantics and view objects."),
                    _("Object references, mutability rules, equality vs identity, and truthiness."),
                ],
            },
            {
                "title": _("Operators & evaluation rules"),
                "items": [
                    _("Arithmetic, bitwise, and comparison operators with precedence awareness."),
                    _("Membership and identity tests (in, not in, is) for defensive programming."),
                    _("Augmented assignment, iterable unpacking, and structural pattern matching basics."),
                ],
            },
            {
                "title": _("Error handling & exceptions"),
                "items": [
                    _("Structured try/except/else/finally blocks and exception chaining."),
                    _("Custom exception hierarchies tailored to domain errors."),
                    _("Assertions, warnings, and graceful failure patterns for CLIs and services."),
                ],
            },
            {
                "title": _("I/O & runtime environment"),
                "items": [
                    _("File, text, and binary handling with pathlib, codecs, and context managers."),
                    _("Environment variables, CLI args (argparse/typer), and layered configuration loading."),
                    _("Shell orchestration with subprocess, logging basics, and structured output."),
                ],
            },
            {
                "title": _("Standard library essentials"),
                "items": [
                    _("Platform tools (os, sys, pathlib) and schedulers (datetime, time, zoneinfo)."),
                    _("Data wrangling modules such as json, csv, sqlite3, statistics, and dataclasses."),
                    _("Utilities for iteration, caching, randomness, and typing (itertools, functools, random, typing)."),
                ],
            },
        ],
    },
    {
        "slug": "data_structures",
        "title": _("Data Structures"),
        "summary": _("Get fluent with Python's native containers, iterators, and batteries-included helpers."),
        "tagline": _("Python collections"),
        "sections": [
            {
                "title": _("Native collections"),
                "items": [
                    _("Lists, tuples, dicts, and sets with slicing, unpacking, and view semantics."),
                    _("String operations, slicing tricks, and immutability considerations."),
                    _("Memory layout, dynamic resizing, and amortized-cost analysis."),
                ],
            },
            {
                "title": _("Collections module power-ups"),
                "items": [
                    _("deque for queue/stack workloads and thread-safe rotations."),
                    _("Counter, defaultdict, and OrderedDict for frequency analysis and default state."),
                    _("namedtuple and dataclasses for lightweight record types."),
                ],
            },
            {
                "title": _("Priority queues & heaps"),
                "items": [
                    _("heapq usage patterns and custom key comparisons."),
                    _("Simulating max-heaps and multi-queue coordination."),
                    _("Scheduling problems, streaming medians, and bounded leaderboards."),
                ],
            },
            {
                "title": _("Iterators & generators"),
                "items": [
                    _("Iterator protocol, __iter__/__next__, and generator functions."),
                    _("Generator expressions, chaining, and lazy evaluation for large datasets."),
                    _("Contextlib helpers, itertools recipes, and backpressure-aware pipelines."),
                ],
            },
        ],
    },
    {
        "slug": "algorithms",
        "title": _("Algorithms"),
        "summary": _("Implement the classic problem-solving toolkit with idiomatic Python."),
        "tagline": _("Problem solving"),
        "sections": [
            {
                "title": _("Core data structures"),
                "items": [
                    _("Trees, BSTs, heaps, and tries implemented with Python lists/dicts."),
                    _("Union-find, disjoint sets, and interval scheduling helpers."),
                    _("Hash-table collision handling and custom equality/ordering hooks."),
                ],
            },
            {
                "title": _("Sorting & searching"),
                "items": [
                    _("Implementations of quicksort, mergesort, heapsort, and timsort insights."),
                    _("Binary search helpers via bisect and invariants for rotated arrays."),
                    _("Stability, in-place trade-offs, and key functions."),
                ],
            },
            {
                "title": _("Graph algorithms"),
                "items": [
                    _("Adjacency lists vs matrices, graph traversal templates."),
                    _("BFS/DFS variants for connected components, topological sorts, and cycle detection."),
                    _("Weighted shortest path routines (Dijkstra, A*) and heuristics."),
                ],
            },
            {
                "title": _("Dynamic programming & optimization"),
                "items": [
                    _("Memoization with functools.lru_cache and manual caches."),
                    _("Tabulation strategies, prefix sums, and sliding windows."),
                    _("Complexity analysis (Big-O/Ω/Θ) tied to Python's runtime characteristics."),
                ],
            },
        ],
    },
    {
        "slug": "oop",
        "title": _("Python Object-Oriented Principles"),
        "summary": _("Design expressive class hierarchies, leverage protocols, and model domains clearly."),
        "tagline": _("Modeling"),
        "sections": [
            {
                "title": _("Class anatomy"),
                "items": [
                    _("__init__/__new__ lifecycles, attribute slots, and datamodel hooks."),
                    _("Docstrings, annotations, and runtime introspection for IDE help."),
                    _("Rich comparisons, hashing, and truthiness overrides."),
                ],
            },
            {
                "title": _("Encapsulation"),
                "items": [
                    _("Visibility via single/double underscore naming conventions."),
                    _("Properties, cached_property, and validation guards."),
                    _("Composition over inheritance for clarity and testability."),
                ],
            },
            {
                "title": _("Inheritance & composition"),
                "items": [
                    _("Multiple inheritance, mixins, and cooperative super() calls."),
                    _("Aggregation vs composition semantics in domain models."),
                    _("Data modeling with dataclasses, attrs, and pydantic."),
                ],
            },
            {
                "title": _("Polymorphism & protocols"),
                "items": [
                    _("Duck typing, structural subtyping, and typing.Protocol usage."),
                    _("Strategy objects, adapters, and interface segregation."),
                    _("Abstract base classes (abc.ABC) and plugin registries."),
                ],
            },
        ],
    },
    {
        "slug": "patterns",
        "title": _("Advanced Python Language Features"),
        "summary": _("Harness decorators, context managers, metaclasses, and pattern matching to shape clean APIs."),
        "tagline": _("Language patterns"),
        "sections": [
            {
                "title": _("Generators & streaming"),
                "items": [
                    _("Yield-based coroutines, send/throw, and backpressure-aware pipelines."),
                    _("Generator-based resource cleanup with contextlib.contextmanager."),
                    _("Async generators and streaming responses."),
                ],
            },
            {
                "title": _("Decorators"),
                "items": [
                    _("Function/class decorators, functools.wraps, and metadata preservation."),
                    _("Parameterized decorators for dependency injection and tracing."),
                    _("Stacking decorators safely with typing annotations."),
                ],
            },
            {
                "title": _("Context managers"),
                "items": [
                    _("Custom __enter__/__exit__ implementations for transactional code."),
                    _("contextlib utilities, ExitStack, and async context managers."),
                    _("Resource pooling patterns for DB sessions, caches, and temp files."),
                ],
            },
            {
                "title": _("Descriptors & metaclasses"),
                "items": [
                    _("Descriptor protocol for validation, computed attributes, and lazy loading."),
                    _("property vs cached_property vs custom descriptor trade-offs."),
                    _("Metaclasses for registration, enforcing contracts, and DSL-like APIs."),
                ],
            },
            {
                "title": _("Modules & pattern matching"),
                "items": [
                    _("Package layouts, namespace packages, and __all__ hygiene."),
                    _("match/case structural patterns for parsers and protocol dispatch."),
                    _("Plugin discovery via entry points and importlib."),
                ],
            },
        ],
    },
    {
        "slug": "web",
        "title": _("Backend & Web Interfaces"),
        "summary": _("Ship polished user experiences with Django, React, Tailwind, and modern deployment stacks."),
        "tagline": _("Product surface"),
        "sections": [
            {
                "title": _("Django foundations"),
                "items": [
                    _("URL routing, class-based views, serializers, and template composition."),
                    _("Form handling, validation flows, and CSRF/session management."),
                    _("Internationalization, localization, and accessibility guardrails."),
                ],
            },
            {
                "title": _("React & Vite integration"),
                "items": [
                    _("TypeScript components compiled via Vite and served through django-vite."),
                    _("State management options (context, SWR, TanStack Query) for rich widgets."),
                    _("Bridging Django templates with React islands and HMR."),
                ],
            },
            {
                "title": _("Styling system"),
                "items": [
                    _("Tailwind v4 utility workflows and DaisyUI component patterns."),
                    _("Design tokens, responsive grids, and accessible color palettes."),
                    _("Custom themes shared between Django and standalone Vite builds."),
                ],
            },
            {
                "title": _("Auth & security"),
                "items": [
                    _("django-allauth flows, social login, and MFA add-ons."),
                    _("Permission checks in views, templates, and DRF viewsets."),
                    _("Secure cookie/session settings and HTTPS hardening."),
                ],
            },
            {
                "title": _("Performance & delivery"),
                "items": [
                    _("Template streaming, caching (per-view, per-template), and CDN strategies."),
                    _("Asset optimization via Vite, code-splitting, and preloading hints."),
                    _("Measuring Core Web Vitals and backend response budgets."),
                ],
            },
        ],
    },
    {
        "slug": "db",
        "title": _("Storage & Databases"),
        "summary": _("Model relational schemas, interact with key-value stores, and reason about migrations."),
        "tagline": _("Data layer"),
        "sections": [
            {
                "title": _("Relational modeling"),
                "items": [
                    _("PostgreSQL-first design, normalization, and constraints."),
                    _("Schema migrations with Django, Alembic, and zero-downtime patterns."),
                    _("Transactions, isolation levels, and locking semantics."),
                ],
            },
            {
                "title": _("ORM best practices"),
                "items": [
                    _("Querysets, select_related/prefetch_related, and lazy evaluation."),
                    _("Bulk operations, pagination, and concurrency-safe updates."),
                    _("Connection pooling, read replicas, and sharding strategies."),
                ],
            },
            {
                "title": _("Document & cache stores"),
                "items": [
                    _("MongoDB, DynamoDB, and schema-on-read conventions."),
                    _("Redis for caching, rate limits, and distributed locks."),
                    _("TTL management, eviction policies, and serialization formats."),
                ],
            },
            {
                "title": _("Search & analytics"),
                "items": [
                    _("Elasticsearch/OpenSearch indexing, analyzers, and aggregations."),
                    _("Full-text search integration with Django and Postgres GIN."),
                    _("Reporting warehouses, columnar stores, and dbt-style transformations."),
                ],
            },
            {
                "title": _("Messaging & streaming"),
                "items": [
                    _("Kafka topics, partitions, and consumer groups."),
                    _("RabbitMQ/Redis Streams for task queues and async workflows."),
                    _("Outbox patterns and exactly-once-ish delivery guarantees."),
                ],
            },
        ],
    },
    {
        "slug": "api",
        "title": _("APIs & Service Contracts"),
        "summary": _("Design resilient HTTP and RPC interfaces backed by OpenAPI-first tooling."),
        "tagline": _("Service edges"),
        "sections": [
            {
                "title": _("REST fundamentals"),
                "items": [
                    _("Resource modeling, status codes, pagination, and filtering conventions."),
                    _("Idempotency keys, optimistic concurrency, and caching headers."),
                    _("Versioning schemes (URI, header, media type) and deprecation playbooks."),
                ],
            },
            {
                "title": _("Frameworks"),
                "items": [
                    _("Django REST Framework serializers, viewsets, and throttling."),
                    _("FastAPI for async endpoints with dependency injection."),
                    _("Tornado/aiohttp for streaming and WebSocket workloads."),
                ],
            },
            {
                "title": _("Schema & documentation"),
                "items": [
                    _("OpenAPI/Swagger generation, ReDoc, and Postman collections."),
                    _("Generated clients via datamodel-codegen or orval feeding TypeScript/Swift/Go."),
                    _("Contract testing and backward-compatibility gates in CI."),
                ],
            },
            {
                "title": _("Security & auth"),
                "items": [
                    _("OAuth2 flows, JWT validation, and API key management."),
                    _("Rate limiting, abuse monitoring, and audit logging."),
                    _("mTLS, signed URLs, and secrets distribution."),
                ],
            },
        ],
    },
    {
        "slug": "async",
        "title": _("Execution & Concurrency"),
        "summary": _("Understand CPython internals, the GIL, and async primitives for IO-heavy workloads."),
        "tagline": _("Runtime"),
        "sections": [
            {
                "title": _("Interpreter & bytecode"),
                "items": [
                    _("CPython compilation pipeline, .pyc caching, and disassembly."),
                    _("Code object layouts, stack frames, and tracing hooks."),
                    _("C-API bridges such as Cython, PyO3, and HPy."),
                ],
            },
            {
                "title": _("Memory model"),
                "items": [
                    _("Reference counting, generational GC, and weakref usage."),
                    _("Object pools, freelists, and memoryview buffers."),
                    _("Profiling leaks with tracemalloc and objgraph."),
                ],
            },
            {
                "title": _("GIL-aware concurrency"),
                "items": [
                    _("threading vs multiprocessing trade-offs and shared-state hazards."),
                    _("Concurrent.futures pools for CPU vs IO workloads."),
                    _("C extensions, PyPy, and nogil builds for hotspots."),
                ],
            },
            {
                "title": _("AsyncIO & event loops"),
                "items": [
                    _("async/await syntax, Tasks, Futures, and event loop policies."),
                    _("Backpressure, cancellation, and structured concurrency patterns."),
                    _("Integration with HTTP clients, websockets, and message brokers."),
                ],
            },
            {
                "title": _("Performance tuning"),
                "items": [
                    _("Profiling with cProfile, py-spy, scalene, and line_profiler."),
                    _("Caching, batching, and vectorization (Numba, numpy)."),
                    _("Observability of async stacks with tracing and metrics."),
                ],
            },
        ],
    },
    {
        "slug": "devops",
        "title": _("DevOps & Delivery"),
        "summary": _("Automate builds, deployments, and observability across multiple cloud targets."),
        "tagline": _("Runtime ops"),
        "sections": [
            {
                "title": _("Application servers"),
                "items": [
                    _("Gunicorn, Uvicorn, and Daphne configuration for WSGI/ASGI apps."),
                    _("Process managers (systemd, supervisord) and graceful reloads."),
                    _("Nginx/HAProxy reverse proxies, SSL termination, and HTTP/3."),
                ],
            },
            {
                "title": _("Containers & orchestration"),
                "items": [
                    _("Dockerfiles, multi-stage builds, and SBOM scanning."),
                    _("docker-compose vs Kubernetes Helm charts and Kustomize."),
                    _("Service meshes, ingress controllers, and autoscaling policies."),
                ],
            },
            {
                "title": _("Infrastructure as code"),
                "items": [
                    _("Terraform modules, Terragrunt, and drift detection."),
                    _("Ansible/Pulumi workflows for config management."),
                    _("Secrets management with Vault, SOPS, and cloud KMS."),
                ],
            },
            {
                "title": _("CI/CD pipelines"),
                "items": [
                    _("GitHub Actions, GitLab CI, Jenkins shared libraries, and reusable workflows."),
                    _("Artifact management, SBOM generation, and supply-chain security."),
                    _("Progressive delivery (blue/green, canary, feature flags)."),
                ],
            },
            {
                "title": _("Observability"),
                "items": [
                    _("Prometheus metrics, Grafana dashboards, and alert routing (PagerDuty/Opsgenie)."),
                    _("Structured logging stacks (ELK/EFK) and log sampling."),
                    _("OpenTelemetry traces wired to Honeycomb/Jaeger/New Relic."),
                ],
            },
            {
                "title": _("Cloud platforms"),
                "items": [
                    _("AWS (boto3), Azure SDKs, and Google Cloud clients."),
                    _("Serverless runtimes (Lambda, Cloud Functions, Cloud Run)."),
                    _("Cost monitoring, tagging strategies, and multi-account governance."),
                ],
            },
        ],
    },
    {
        "slug": "system_design",
        "title": _("System Design & Scalability"),
        "summary": _("Architect resilient distributed systems with clear data contracts and failure plans."),
        "tagline": _("Architecture"),
        "sections": [
            {
                "title": _("Distributed fundamentals"),
                "items": [
                    _("CAP theorem, consistency models, and latency budgets."),
                    _("Leader election, consensus, and clock synchronization."),
                    _("SLOs, SLIs, and error budgets driving design decisions."),
                ],
            },
            {
                "title": _("Caching strategies"),
                "items": [
                    _("Client, edge, and data-layer caches (Redis, Memcached)."),
                    _("Cache invalidation, warming, and dogpile protection."),
                    _("Content-addressable storage, CDN, and ETag coordination."),
                ],
            },
            {
                "title": _("API design"),
                "items": [
                    _("REST vs GraphQL vs gRPC decision trees."),
                    _("Pagination, rate limiting, and SLA-backed contracts."),
                    _("Multi-tenant boundaries, request tracing, and auditability."),
                ],
            },
            {
                "title": _("Resilience patterns"),
                "items": [
                    _("Circuit breakers, retries with jitter, and bulkheads."),
                    _("Saga/outbox patterns for eventual consistency."),
                    _("Chaos drills, load testing, and capacity modeling."),
                ],
            },
            {
                "title": _("Data partitioning"),
                "items": [
                    _("Sharding, consistent hashing, and data locality."),
                    _("Event sourcing, CQRS, and append-only logs."),
                    _("Idempotent processing, deduplication, and replay strategies."),
                ],
            },
            {
                "title": _("Security & compliance"),
                "items": [
                    _("OAuth2, OIDC, and service-to-service auth."),
                    _("TLS termination, cert rotation, and secrets governance."),
                    _("Encryption at rest/in transit, HSMs, and key rotation."),
                ],
            },
        ],
    },
    {
        "slug": "tests",
        "title": _("Development Workflow & Quality"),
        "summary": _("Run projects end-to-end with reliable tooling, automated tests, and fast feedback."),
        "tagline": _("Feedback loop"),
        "sections": [
            {
                "title": _("Project workflow"),
                "items": [
                    _("Virtual environments (venv, uv, poetry) and dependency pinning."),
                    _("Package layouts, pyproject.toml metadata, and make/Invoke task runners."),
                    _("Documentation with Markdown, Sphinx, MkDocs, and OpenAPI."),
                ],
            },
            {
                "title": _("Testing stack"),
                "items": [
                    _("pytest, unittest, and Django test client patterns."),
                    _("Mocking, monkeypatching, and pytest fixtures for isolation."),
                    _("Testcontainers, factory_boy, and data builders."),
                ],
            },
            {
                "title": _("Advanced QA"),
                "items": [
                    _("Property-based testing with Hypothesis and fuzzers."),
                    _("Contract tests for APIs and consumer-driven Pact flows."),
                    _("Coverage enforcement, flaky-test detection, and parallel execution."),
                ],
            },
            {
                "title": _("Static analysis"),
                "items": [
                    _("Formatting with black/ruff-format and import sorting."),
                    _("Linting via ruff/pylint/flake8 and type checking with mypy or pyright."),
                    _("Security scanners, bandit, and dependency vulnerability checks."),
                ],
            },
            {
                "title": _("Debugging & profiling"),
                "items": [
                    _("pdb/ipdb workflows, VS Code/pycharm debuggers, and breakpoints."),
                    _("cProfile, line_profiler, scalene, and PyInstrument for hotspots."),
                    _("Tracing async code, logging correlation IDs, and cloud debugger hooks."),
                ],
            },
        ],
    },
    {
        "slug": "leadership",
        "title": _("Leadership & Collaboration"),
        "summary": _("Guide teams with architectural clarity, empathetic processes, and thoughtful reviews."),
        "tagline": _("People"),
        "sections": [
            {
                "title": _("Code review & standards"),
                "items": [
                    _("Review checklists, style guides, and constructive feedback loops."),
                    _("Automating guardrails with linters, tests, and templates."),
                    _("Coaching engineers toward clarity and empathy in reviews."),
                ],
            },
            {
                "title": _("Architecture decisions"),
                "items": [
                    _("ADR templates, RFC rituals, and lightweight governance."),
                    _("Balancing experimentation with reliability and compliance."),
                    _("Budgeting time for spikes, prototyping, and deprecation."),
                ],
            },
            {
                "title": _("Mentorship & onboarding"),
                "items": [
                    _("Buddy programs, learning paths, and pair rotations."),
                    _("Skills matrices, growth frameworks, and continuous feedback."),
                    _("Knowledge bases, runbooks, and documentation culture."),
                ],
            },
            {
                "title": _("Process & delivery"),
                "items": [
                    _("Scrum, Kanban, and flow-based planning with realistic WIP limits."),
                    _("Ritual design for standups, demos, retros, and async updates."),
                    _("Balancing product velocity with technical debt paydown."),
                ],
            },
            {
                "title": _("Cross-functional collaboration"),
                "items": [
                    _("Partnering with product, design, and DevOps for shared outcomes."),
                    _("Risk communication, stakeholder updates, and decision logs."),
                    _("Scaling culture across distributed and hybrid teams."),
                ],
            },
        ],
    },
]


def get_topic(slug: str) -> Topic:
    for topic in TOPICS:
        if topic["slug"] == slug:
            topic = topic.copy()
            topic.setdefault("url_name", f"tutorial_{slug}:home")
            return topic
    raise KeyError(slug)
