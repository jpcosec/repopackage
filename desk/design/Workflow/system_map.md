# System Map: Workflow Dimensions

```mermaid
graph LR

%% ─────────────────────────────────────────
%% SPACE-TIME ZONES (Where / When)
%% ─────────────────────────────────────────

    subgraph FUTURE["📦 FUTURE — drawers/"]
        DS[DesignSpec]
        MC[ModuleContract]
        ADR[ADR\nWhy we decided X]
    end

    subgraph NOW["🖥️ NOW — desk/"]
        subgraph DESK_DESIGN["desk/design/"]
            SPEC[ActiveSpec]
        end
        subgraph DESK_TASKS["desk/tasks/"]
            B[Board]
            PH[Phase]
            T[Task]
        end
        subgraph DESK_PILLS["desk/pills/"]
            P[Pill]
        end
    end

    subgraph PAST["📚 PAST — git + runs/"]
        EV[Evidence]
        GC[GitCommit]
        SRC[Source Code]
    end

%% ─────────────────────────────────────────
%% ACTORS (Who)
%% ─────────────────────────────────────────

    subgraph WHO["👥 Who"]
        SUP["🧠 Supervisor\nLLM — thinks"]
        EXE["⚒️ Executor\nLLM — implements"]
        CLI["⚙️ CLI\nautomated — executes"]
    end

%% ─────────────────────────────────────────
%% ARTIFACT COMPOSITION (What)
%% ─────────────────────────────────────────

    B -->|organizes| PH
    PH -->|contains| T
    T -.->|refs by id| P
    B -->|owns| P
    ADR -.->|informs| SPEC

%% ─────────────────────────────────────────
%% FLOWS (How — transitions between zones)
%% ─────────────────────────────────────────

    DS -->|"promote-spec\n[CLI]"| T
    DS -->|"activate\n[SUP]"| SPEC
    SPEC -->|"atomize\n[SUP+CLI]"| T
    T -->|"bind\n[CLI]"| P
    T & P -->|"index\n[CLI]"| B

    T -->|"implement\n[EXE]"| SRC
    SRC -->|"test+lint\n[CLI]"| EV
    EV -->|"audit\n[SUP]"| GC
    GC -->|"closes"| T

    GC -->|"phase commit\n[CLI]"| PH

%% ─────────────────────────────────────────
%% WHO TOUCHES WHAT
%% ─────────────────────────────────────────

    SUP -->|designs| DS
    SUP -->|writes| ADR
    SUP -->|atomizes| T
    SUP -->|audits| EV

    EXE -->|implements| SRC
    EXE -->|writes| EV

    CLI -->|creates| T
    CLI -->|creates| P
    CLI -->|syncs| B
    CLI -->|commits| GC

%% ─────────────────────────────────────────
%% STYLING
%% ─────────────────────────────────────────

    classDef future fill:#f5f0ff,stroke:#9b59b6
    classDef now fill:#f0f8ff,stroke:#2980b9
    classDef past fill:#f0fff4,stroke:#27ae60
    classDef actor fill:#fff8f0,stroke:#e67e22
    classDef adr fill:#fff0f0,stroke:#e74c3c

    class DS,MC future
    class SPEC,B,PH,T,P now
    class EV,GC,SRC past
    class SUP,EXE,CLI actor
    class ADR adr
```

## Reading Guide

| Dimension | Colour | Elements |
|-----------|--------|----------|
| **What** | — | DS, MC, T, P, B, PH, EV, GC, SRC, ADR |
| **Where / When** | Purple=future · Blue=now · Green=past | drawers/ → desk/ → git/ |
| **Who** | Orange | Supervisor, Executor, CLI |
| **How** | Arrow labels | promote-spec, atomize, bind, index, implement, audit, commit |
| **Why** | Red | ADR — informs Spec, never executes |
