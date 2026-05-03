# WORKFLOW_DIAGRAM.md — CRUX flow diagrams

> All diagrams are mermaid. They render natively on GitHub, GitLab, and Bob's Bob Findings panel. If a diagram needs to evolve, edit the mermaid source here and re-render — don't keep parallel PNG copies.

---

## 1. End-to-end: notebook in, deployable service out

```mermaid
flowchart TD
    Input([User points Bob at samples/02_messy.ipynb])
    Bob[IBM Bob IDE in crux-mode]
    Skill1[skills/notebook-narrative]
    Skill2[skills/production-audit]
    MCP[mcp_server / FastMCP]
    
    Input --> Bob
    Bob -->|invokes| Skill1
    
    Skill1 -->|writes| RP[recovered_pipeline.py]
    Skill1 -->|writes| IR[intent_report.md]
    
    Bob -->|user confirms| Skill2
    Skill2 -->|reads| RP
    Skill2 -->|writes| AD[audit_dossier.md]
    Skill2 -->|writes| DL[decision_log.md]
    Skill2 -->|writes| Service[service.py + schema.py + preprocessor.py]
    Skill2 -->|writes| Tests[tests/parity_test.py]
    Skill2 -->|writes| Docker[Dockerfile + docker-compose.yml]
    Skill2 -->|runs| ParityRun{parity test passes?}
    
    ParityRun -->|yes| Done([Bob reports success to user])
    ParityRun -->|no| Surface[Surface failure in dossier]
    
    Bob -.->|optionally calls| MCP
    MCP -.->|exposes| ToolList[5 MCP tools]
    
    style Input fill:#dbeafe
    style Done fill:#d1fae5
    style MCP fill:#fef3c7
    style Surface fill:#fee2e2
```

---

## 2. Stage 1 detail: narrative intent recovery

```mermaid
flowchart TD
    NB([input.ipynb])
    
    Parse[parse_notebook.py<br/>nbformat → list of Cell]
    Lineage[lineage_graph.py<br/>ast → DiGraph of cell name-flow]
    Score[narrative_scorer.py<br/>regex on markdown_before/after]
    
    NB --> Parse
    Parse --> Lineage
    Parse --> Score
    
    Classify[classifier.py<br/>combine 3 signals]
    
    Lineage --> Classify
    Score --> Classify
    Parse --> Classify
    
    FindTerm{find terminal artifacts<br/>joblib.dump? predict()? last cell?}
    Classify --> FindTerm
    FindTerm --> Trace[trace backward via lineage<br/>cells on a path = load-bearing]
    Trace --> Decide[per-cell label<br/>load-bearing / scaffolding / exploratory / dead<br/>+ confidence]
    
    Decide --> Writer[pipeline_writer.py<br/>topo-sort load-bearing cells<br/>emit recovered_pipeline.py]
    Decide --> Report[intent_report.py<br/>emit intent_report.md]
    
    Writer --> Out1([recovered_pipeline.py])
    Report --> Out2([intent_report.md])
    
    style NB fill:#dbeafe
    style Out1 fill:#d1fae5
    style Out2 fill:#d1fae5
```

---

## 3. Stage 2 detail: 15-gap audit pipeline

```mermaid
flowchart LR
    RP([recovered_pipeline.py])
    NB([original notebook])
    
    Runner[audit_runner.py<br/>orchestrator]
    
    RP --> Runner
    NB --> Runner
    
    subgraph Critical [🔴 critical gaps]
        G1[gap_01_input_validation]
        G2[gap_02_schema_contract]
        G3[gap_03_train_serve_skew]
        G4[gap_04_missing_model]
        G9[gap_09_hardcoded_paths]
    end
    
    subgraph High [🟡 high gaps]
        G5[gap_05_no_versioning]
        G6[gap_06_logging]
        G7[gap_07_input_range]
        G10[gap_10_rate_limit_timeout]
        G12[gap_12_authentication]
        G14[gap_14_no_tests]
        G15[gap_15_no_dockerfile]
    end
    
    subgraph Medium [🟢 medium gaps]
        G8[gap_08_drift_detection]
        G11[gap_11_batch_endpoint]
        G13[gap_13_repro_metadata]
    end
    
    Runner --> Critical
    Runner --> High
    Runner --> Medium
    
    Critical --> Findings[list of Finding]
    High --> Findings
    Medium --> Findings
    
    Findings --> Assemble[assemble dossier<br/>severity-ranked sections]
    Findings --> Decisions[extract decision options]
    Findings --> Patches[apply autopatches]
    
    Assemble --> Out1([audit_dossier.md])
    Decisions --> Out2([decision_log.md])
    Patches --> Out3([service.py, schema.py,<br/>preprocessor.py, Dockerfile, …])
    Patches --> Out4([tests/parity_test.py])
    
    Out4 --> RunTest{pytest passes?}
    RunTest -->|yes| Done([AuditResult.parity_test_passed=True])
    RunTest -->|no| Fail([record failure in dossier])
    
    style RP fill:#dbeafe
    style NB fill:#dbeafe
    style Out1 fill:#d1fae5
    style Out2 fill:#d1fae5
    style Out3 fill:#d1fae5
    style Out4 fill:#d1fae5
    style Critical fill:#fee2e2
    style High fill:#fef3c7
    style Medium fill:#dcfce7
```

---

## 4. The MCP server topology

```mermaid
flowchart TD
    subgraph Clients [MCP clients]
        Bob[IBM Bob IDE]
        Inspector[MCP Inspector<br/>localhost:6274]
        CI[GitHub Actions runner]
    end
    
    subgraph Server [crux MCP server]
        FastMCP[FastMCP 3.x dispatcher]
        T1[audit_notebook]
        T2[get_dossier]
        T3[list_open_decisions]
        T4[compare_notebooks]
        T5[block_merge_if_critical_gaps]
        FastMCP --> T1
        FastMCP --> T2
        FastMCP --> T3
        FastMCP --> T4
        FastMCP --> T5
    end
    
    subgraph Skills [crux skills layer]
        Narrative[notebook-narrative]
        Audit[production-audit]
        Cache[(out/&lt;notebook-stem&gt;/<br/>cached results)]
    end
    
    Bob -.stdio.-> FastMCP
    Inspector -.streamable-http.-> FastMCP
    CI -.streamable-http.-> FastMCP
    
    T1 --> Narrative
    T1 --> Audit
    T2 --> Cache
    T3 --> Cache
    T4 --> Narrative
    T4 --> Audit
    T5 --> Cache
    
    Narrative --> Cache
    Audit --> Cache
    
    style Bob fill:#dbeafe
    style Inspector fill:#dbeafe
    style CI fill:#dbeafe
    style FastMCP fill:#fef3c7
    style Cache fill:#f3e8ff
```

---

## 5. The CI block-on-gaps flow (DevOps wow moment)

```mermaid
sequenceDiagram
    actor Dev as Data scientist
    participant GH as GitHub
    participant Action as ci/block-on-gaps.yml
    participant MCP as crux MCP server
    participant Out as out/&lt;stem&gt;/

    Dev->>GH: opens PR with changed notebook
    GH->>Action: triggers workflow
    Action->>Action: uv sync, install crux
    Action->>MCP: starts server (background)
    Action->>MCP: audit_notebook(path) via streamable-http
    MCP->>Out: writes audit_dossier.md, decision_log.md
    MCP-->>Action: AuditResult JSON
    Action->>MCP: block_merge_if_critical_gaps(notebook_id)
    MCP->>Out: reads cached AuditResult
    
    alt critical gaps unresolved
        MCP-->>Action: {allow_merge: false, blocking_gaps: [4, 9]}
        Action->>GH: post PR comment with dossier excerpt
        Action->>GH: exit 1 (block merge)
        GH->>Dev: ❌ checks failed
    else clean or only non-critical
        MCP-->>Action: {allow_merge: true, blocking_gaps: []}
        Action->>GH: post PR comment "audit passed"
        Action->>GH: exit 0
        GH->>Dev: ✅ checks passed
    end
```

---

## 6. The decision-log resolution flow

```mermaid
flowchart TD
    Audit([initial audit run]) --> Open[decision_log.md<br/>4 open decisions]
    
    Open --> Walk{user walks through<br/>decisions in Bob}
    
    Walk -->|Decision 7: input range| Choice7{A: warn / B: reject / C: clip}
    Walk -->|Decision 8: drift detection| Choice8{A: hourly / B: real-time / C: defer}
    Walk -->|Decision 11: batch endpoint| Choice11{A: scaffold / B: defer}
    Walk -->|Decision 12: auth| Choice12{A: API key / B: OAuth / C: defer}
    
    Choice7 --> Resolve[crux audit --resolve 7=A 8=C 11=B 12=C]
    Choice8 --> Resolve
    Choice11 --> Resolve
    Choice12 --> Resolve
    
    Resolve --> Rerun[re-runs Stage 2<br/>with chosen options]
    Rerun --> Updated[updated audit_dossier.md<br/>updated service.py<br/>updated tests/]
    Updated --> Done([all decisions resolved<br/>service ready to deploy])
    
    style Open fill:#fef3c7
    style Done fill:#d1fae5
```

---

## 7. The three demo wow moments (timing)

```mermaid
gantt
    title 5-minute demo timeline
    dateFormat mm:ss
    axisFormat %M:%S
    
    section Setup
    Brief intro & problem statement      :done, intro, 00:00, 60s
    
    section Wow #1
    Open 02_messy.ipynb (47 cells)        :w1a, 01:00, 15s
    Invoke Bob recover                     :w1b, after w1a, 30s
    Show intent_report.md                  :crit, w1c, after w1b, 25s
    Show recovered_pipeline.py (80 LOC)    :crit, w1d, after w1c, 20s
    
    section Wow #2
    Trigger production audit               :w2a, after w1d, 30s
    Open audit_dossier.md                  :crit, w2b, after w2a, 25s
    Highlight gap 3 (train/serve skew)     :w2c, after w2b, 15s
    Read decision 8 aloud (drift)          :crit, w2d, after w2c, 20s
    
    section Wow #3
    Show MCP tools in inspector            :w3a, after w2d, 15s
    Trigger fake CI workflow               :w3b, after w3a, 15s
    Show red ❌ on PR + blocking_gaps       :crit, w3c, after w3b, 20s
    
    section Close
    Closing line + repo + Bob sessions     :close, after w3c, 30s
```

---

## 8. Build sequence (high-level)

```mermaid
flowchart LR
    P0[Hour 0–3<br/>setup repo<br/>refine AGENTS.md<br/>pick samples]
    P1[Hour 3–14<br/>build skills/notebook-narrative<br/>tune heuristics on samples]
    P2[Hour 14–24<br/>build skills/production-audit<br/>15 gaps + autopatches + service gen]
    P3[Hour 24–32<br/>build mcp_server<br/>register with Bob<br/>mock CI workflow]
    P4[Hour 32–38<br/>dossier polish<br/>stakeholder template<br/>third sample if time]
    P5[Hour 38–44<br/>demo polish<br/>rehearse 3x<br/>record backup video]
    P6[Hour 44–48<br/>export bob_sessions<br/>final commit<br/>submit]
    
    P0 --> P1 --> P2 --> P3 --> P4 --> P5 --> P6
    
    style P4 fill:#e0f2fe
    style P6 fill:#d1fae5
```

---

## 9. State of artifacts during a run

```mermaid
stateDiagram-v2
    [*] --> NotebookExists: input file present
    
    NotebookExists --> Parsed: parse_notebook.py
    Parsed --> Classified: classifier.py
    Classified --> RecoveredOnly: pipeline_writer.py + intent_report.py
    
    RecoveredOnly --> Audited: audit_runner.py runs all 15 gaps
    Audited --> ServiceWritten: service_generator.py
    ServiceWritten --> TestsWritten: parity_test_generator.py
    TestsWritten --> ParityChecked: pytest run
    
    ParityChecked --> Pass: outputs match training sample
    ParityChecked --> Fail: outputs diverge
    
    Pass --> [*]: AuditResult complete
    Fail --> Surfaced: dossier shows red flag
    Surfaced --> [*]: AuditResult complete (parity_test_passed=False)
    
    note right of RecoveredOnly
      Demo wow #1 happens here:
      intent_report.md visible
    end note
    
    note right of ParityChecked
      Demo wow #2 happens
      around here: dossier visible
    end note
```

---

## 10. Bobcoin spend curve (planned vs. risk)

```mermaid
xychart-beta
    title "Cumulative Bobcoin spend across 48 hours"
    x-axis "Hour" [0, 6, 12, 18, 24, 30, 36, 42, 48]
    y-axis "Bobcoins spent" 0 --> 40
    line "Planned spend" [2, 6, 10, 16, 22, 28, 32, 33, 34]
    line "Risk envelope" [3, 9, 15, 22, 30, 35, 38, 39, 40]
```

The 6-Bobcoin gap between the planned curve and the 40-Bobcoin ceiling is the **demo-day reserve**. It saves you when the live demo crashes and you need to invoke Bob to fix something on stage.

---

## 11. Component-to-focus-area mapping (for the pitch)

```mermaid
flowchart LR
    subgraph FocusAreas [Hackathon focus areas]
        FA1[AI agents doing<br/>complex multi-step work]
        FA2[App modernization]
        FA3[DevOps]
    end
    
    subgraph CRUX [CRUX components]
        L1[Layer 1<br/>narrative intent recovery]
        L2[Layer 2<br/>15-gap audit + autopatch]
        L3[Layer 3<br/>MCP server + CI gate]
    end
    
    L1 -->|recovers buried intent<br/>= multi-step reasoning| FA1
    L2 -->|patches + decisions<br/>= multi-step reasoning| FA1
    L1 -->|notebooks are legacy from birth| FA2
    L2 -->|turns prototype into production| FA2
    L3 -->|MCP server in 200 LOC| FA3
    L3 -->|CI gate via MCP| FA3
    
    style FA1 fill:#dbeafe
    style FA2 fill:#dbeafe
    style FA3 fill:#dbeafe
```

This map is the same one you'll use in the pitch. The brief has three focus areas; CRUX has three layers; each layer hits at least one focus area, with several touching two.

---

*Diagrams should be edited as code, not as images. If a diagram is wrong, fix it here and re-render in your README — don't paste a screenshot back.*
