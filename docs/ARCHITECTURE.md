# Repopackage Architecture

## The Recursive Model

Traditional package managers assume a hierarchy: **Projects** depend on **Libraries**.
Repopackage breaks this by using the **Composable Unit** abstraction. 

Every node in the graph is a Repopackage. Some Repopackages also act as Projects by owning a `Composition Index` (`compose.lock.yaml`) that assembles other nodes. This allows a complex system (like a "Diagnostics Platform") to be developed as a Project but consumed as a single Repopackage node by a higher-level "Main Project".

## Typed Integration Surface

Instead of relying on fragile version numbers, Repopackage uses **Integration Contracts**.

### Exports vs Consumes
- **Exports**: A list of data schemas the unit promises to provide.
- **Consumes**: A list of data schemas the unit requires to function.

The **Solver** validates the graph not just by looking at versions, but by ensuring that every `consumes` requirement in the graph is satisfied by an `exports` from a descendant node.

## Development Lines vs Central Lines

To allow parallel evolution, Repopackage supports two types of history:
1.  **Central Line**: The stable, canonical version of a package.
2.  **Development Line**: A contextual branch tied to a specific project. 

The `compose.yaml` file allows a project to "pin" a dependency to a specific development line, which the solver then locks into the `compose.lock.yaml` with an exact commit hash.

## Control Plane vs execution Plane

Repopackage is a **Control Plane**. It manages the **Metadata** (Contracts, Graph, VCS state). It does not execute your code. It ensures that the environment your code runs in is consistent and structurally sound.
