<h1 align="center">Neha Karamchandani</h1>

<p align="center">
  <b>Backend &amp; data engineer</b> · Java · Python · PostgreSQL · SQL
</p>

<p align="center">
  I build systems where correctness is the feature: medical records an LLM can read but never interpret,<br>
  university exam timetables solved in milliseconds, and data pipelines that test their own numbers.
</p>

<p align="center">
  <a href="https://www.linkedin.com/in/nehakaramchandani/">LinkedIn</a> ·
  <a href="https://medium.com/@nehakaramchandanii">Medium</a> ·
  <a href="https://drive.google.com/file/d/1Wn0S8QGpAZx_U4xaSKsXx1PFyGHzvjZd/view?usp=drive_link">Resume</a> ·
  <a href="mailto:nehakaramchandani2005@gmail.com">Email</a>
</p>

---

### At a glance

| | |
|---|---|
| **Focus** | Backend services, data pipelines, and the tests that keep them honest |
| **Core stack** | Java 21 · Spring Boot · Python · FastAPI · PostgreSQL · Redis · React · Docker |
| **Flagship work** | [Medfold](https://github.com/n3h4a/medfold): 3-service medical records app, **479 tests, 93–97% coverage, p95 reads under 12 ms** <br> [ExamGrid](https://github.com/n3h4a/ExamGrid): exam scheduling engine, **6,500 students / 65,000 enrolments planned in 181 ms** |
| **How I work** | Architecture decision records for every major choice, CI on every push, and numbers you can re-measure with one command |
| **Status** | IT undergraduate · open to backend and data engineering internships |

---

## Featured projects

### [Medfold](https://github.com/n3h4a/medfold): a private, searchable record built from paper medical reports

Upload a PDF or phone photo from any lab. Medfold reads it in the background and gives you a timeline, a trend line for every test, typo-tolerant search and a one-page summary for your next doctor visit. It never tells you what a result means.

- **Async pipeline on PostgreSQL alone.** The upload and its job commit in one transaction. Workers claim jobs with `FOR UPDATE SKIP LOCKED`, retry with backoff, and recover jobs from a crashed worker.
- **LLM safety by design, not by prompt.** The extraction schema has no field for advice. "Above range" is arithmetic in Java against the range printed on that report, not a model's opinion.
- **Privacy you can test.** A test reads the API's route table and attacks every endpoint as a second user (25 of 25 routes), so a new endpoint can't ship unchecked.
- **Claims you can reproduce.** `scripts/verify-claims.sh` re-runs the suites and recounts every number in the README.

`Java 21` `Spring Boot 4` `FastAPI` `Tesseract OCR` `Claude API` `PostgreSQL 16` `React 19` `Docker` · [11 ADRs](https://github.com/n3h4a/medfold/tree/main/docs/03-design/adr) · [bug log](https://github.com/n3h4a/medfold/blob/main/docs/05-testing/bug-log.md)

### [ExamGrid](https://github.com/n3h4a/ExamGrid): exam timetabling, seating and invigilation for universities

ExamGrid takes course enrolments and works out **when** each exam runs, **where** each student sits and **who** supervises each room. It then publishes hall tickets and a "find my seat" page for result day.

- **Solver in plain Java, no framework.** A conflict graph feeds DSatur colouring with TabuCol repair, then simulated annealing or tabu search over Kempe-chain moves. Rooms are assigned by min-cost max-flow and seats by a CSP that never puts two students with the same paper next to each other.
- **Explains infeasible inputs.** When no valid timetable exists, it proves why (Hall's condition, clique bounds, lock clashes) and names the courses and roll numbers involved.
- **Built for result-day traffic.** Solver runs are async with live SSE progress, publishing needs two-person approval, and seat lookups are a single Redis `GET` behind per-IP rate limiting.
- **Measured.** JMH benchmarks: [2,600 students in 59 ms, 6,500 in 181 ms](https://github.com/n3h4a/ExamGrid/blob/main/docs/benchmarks/README.md), with jqwik property tests on every hard constraint.

`Java 21` `Spring Boot 4` `PostgreSQL` `Redis` `Flyway` `Testcontainers` `JMH` `jqwik` · [8 ADRs](https://github.com/n3h4a/ExamGrid/tree/main/docs/adr)

### [What Makes a Global Top 50 Hit Last?](https://github.com/n3h4a/spotify-powerbi-dashboard): end-to-end analytics on Spotify charts

27,800 daily chart entries modelled into a star schema, nine business questions answered with significance tests, and a model that predicts a song's chart life from its first week.

- **Pipeline:** Python + SQL on DuckDB, bronze → silver → gold → marts, guarded by **45 data-quality checks** and **103 tests**.
- **Model:** **ROC-AUC 0.91** on held-out 2024 songs. A leakage test rebuilds the warehouse with future days appended and checks that no feature changes.
- **Dashboards:** a [live web dashboard](https://n3h4a.github.io/spotify-powerbi-dashboard/) with browser end-to-end tests that check each displayed number against independent SQL, and a Power BI project generated as code (TMDL + PBIR, 40 DAX measures).

`Python` `DuckDB` `SQL` `scikit-learn` `statsmodels` `Power BI` `GitHub Actions`

<details>
<summary><b>More work</b></summary>
<br>

| Project | What it shows |
|---|---|
| [SQL Data Warehouse](https://github.com/n3h4a/sql-data-warehouse-project) | Medallion warehouse in SQL Server that combines ERP and CRM sources into a star schema. Includes ETL procedures, silver and gold quality checks, a data catalog and 13 analytical reports. |
| [DSA in Java](https://github.com/n3h4a/dsa-practise) | 90+ LeetCode solutions grouped by 13 patterns, not by problem number. Each states its approach and complexity, and CI compiles every solution on each push. |

</details>

---

## Tech stack

| Area | Tools |
|---|---|
| **Languages** | Java 21, Python 3.12, SQL, TypeScript |
| **Backend** | Spring Boot 4, FastAPI, REST, JWT + RBAC, Flyway, OpenAPI, Server-Sent Events |
| **Data** | PostgreSQL 16 (`pg_trgm`, `SKIP LOCKED`), Redis, DuckDB, SQL Server, Parquet |
| **Analytics & ML** | pandas, scikit-learn, statsmodels, SciPy, Power BI (DAX, TMDL) |
| **AI** | Claude API, Tesseract OCR, schema-constrained extraction |
| **Frontend** | React 19, Vite, Tailwind CSS, TanStack Query |
| **Testing** | JUnit, Testcontainers, jqwik, JMH, pytest, Vitest |
| **Delivery** | Docker Compose, GitHub Actions, nginx, GitHub Pages |

---

## Engineering interests

<details open>
<summary><b>Architecture problems I like to work on</b></summary>
<br>

- **Using one database for several jobs.** Postgres can serve as the job queue, search index and rate limiter, so the critical writes stay atomic and there's only one system to back up.
- **Long-running work behind fast APIs.** Return `202` right away, run the job on a worker, stream progress over SSE, and survive crashes partway through.
- **Combinatorial optimisation in real products.** Graph colouring, flows and local search for constraint problems that real users have.
- **Guardrails for LLM features.** Leave the model no place to put unsafe output instead of asking it nicely in the prompt.
- **Point-in-time data modelling.** Medallion layers, star schemas, and features that can't leak future data.
- **Recording decisions.** ADRs that note the options I rejected and what my choice costs.

</details>

---

## Currently building

- **ExamGrid, milestones 8–10:** React admin console, live run views, timetable and seating screens, a student portal, then full-stack Docker, CI/CD and load tests for result-day traffic. [Roadmap →](https://github.com/n3h4a/ExamGrid/blob/main/docs/ROADMAP.md)
- **Medfold, next release:** password reset and two-factor login, read-only sharing links for doctors, and FHIR export. [Roadmap →](https://github.com/n3h4a/medfold/blob/main/ROADMAP.md)

<details>
<summary><b>What I'm learning, and which project needs it</b></summary>
<br>

| Topic | Why |
|---|---|
| HL7 FHIR | Exporting Medfold records in a format hospitals can import |
| Load testing and capacity planning | Showing ExamGrid's seat lookup can handle every student refreshing at once on result day |
| Vision models for document understanding | Sending only the hard-to-read pages to a vision model while keeping each value traceable to its source |
| Multi-factor authentication flows | Adding two-factor login to Medfold without weakening token rotation |

</details>

---

## GitHub activity

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://github-readme-stats.vercel.app/api?username=n3h4a&show_icons=true&include_all_commits=true&count_private=true&hide_border=true&theme=github_dark&bg_color=00000000">
    <img height="165" alt="GitHub stats" src="https://github-readme-stats.vercel.app/api?username=n3h4a&show_icons=true&include_all_commits=true&count_private=true&hide_border=true&bg_color=00000000">
  </picture>
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://github-readme-stats.vercel.app/api/top-langs/?username=n3h4a&layout=compact&langs_count=6&hide_border=true&theme=github_dark&bg_color=00000000">
    <img height="165" alt="Top languages" src="https://github-readme-stats.vercel.app/api/top-langs/?username=n3h4a&layout=compact&langs_count=6&hide_border=true&bg_color=00000000">
  </picture>
</p>

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://streak-stats.demolab.com?user=n3h4a&hide_border=true&theme=github-dark-blue&background=00000000">
    <img alt="Contribution streak" src="https://streak-stats.demolab.com?user=n3h4a&hide_border=true&background=00000000">
  </picture>
</p>

<details>
<summary><b>Contribution graph</b></summary>
<br>
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github-readme-activity-graph.vercel.app/graph?username=n3h4a&theme=github-compact&hide_border=true&bg_color=0d1117&area=true">
  <img width="100%" alt="Contribution graph" src="https://github-readme-activity-graph.vercel.app/graph?username=n3h4a&theme=minimal&hide_border=true&bg_color=ffffff&area=true">
</picture>
</details>

---

<details>
<summary><b>Fun facts</b></summary>
<br>

- My worst bug so far: **every test passed and every document failed.** Java's HTTP client sent an HTTP/2 upgrade header and the Python service rejected every upload. Since then, CI starts the whole Docker stack on every push.
- I found Medfold's problem in **Razorpay's list of startup problem statements**, where it was one of the highest scorers.
- I once quoted a coverage number that was measured on the wrong machine. That's why Medfold has a script that re-checks every number in its README.
- On 21 Apr 2024, Taylor Swift held **30 of the 50** spots on Spotify's Global Top 50. A SQL query found it.

</details>

---

<p align="center">
  <sub>Each number on this page links to the repository that measures it.</sub><br>
  <sub><a href="https://www.linkedin.com/in/nehakaramchandani/">LinkedIn</a> · <a href="https://medium.com/@nehakaramchandanii">Medium</a> · <a href="https://drive.google.com/file/d/1Wn0S8QGpAZx_U4xaSKsXx1PFyGHzvjZd/view?usp=drive_link">Resume</a> · <a href="mailto:nehakaramchandani2005@gmail.com">nehakaramchandani2005@gmail.com</a></sub>
</p>
