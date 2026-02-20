# Ergonomic Components Structure

## 2. Concept spec: “Ergonomic Components Structure”

### 2.1. Intention

The Ergonomic Components Structure is used to design and control the runtime structure of a backend service as a graph of long-lived objects.
It replaces informal reasoning like “where should we put this logic and how should these classes depend on each other” with verifiable constraints on component kinds and allowed dependencies.
The goal is to keep effects and dependencies explicit, prevent coupling growth, and keep entrypoints thin.

The Ergonomic Components Structure complements the Ergonomic Data Model.
If the Ergonomic Data Model constrains information structure (records, components, references), then the Ergonomic Components Structure constrains runtime state and behavior structure (ports, resources, operations, and their connections).

### 2.2. Ontological status

The Ergonomic Components Structure is a conceptual model and a set of coding constraints for runtime components.
It is expressed as a dependency graph between long-lived objects created and wired at application startup (typically via a DI container).
It describes what components exist at runtime, how they are connected, and which components are allowed to call which.

It is not a package layering scheme by itself.
It is not a requirement to always introduce interfaces, adapters, or clean-architecture style boundaries.
It is not a static “class diagram of everything,” but a model of key runtime objects and their stable links.

Related framework conventions.
See `../ergo/tech/jvm/coding-conventions/naming.md` for class suffix taxonomy and `../ergo/tech/jvm/coding-conventions/packages.md` for a default package layout.

Operational distinction.
If the artifact cannot be used to reconstruct the port/operation/resource graph and check dependency constraints (no port-to-port links, no operation-to-operation links, and resource incoming-link rules), then it is not an Ergonomic Components Structure.

### 2.3. Concept invariants

The Ergonomic Components Structure remains an “Ergonomic Components Structure” only if all statements below hold.

* **Runtime focus: the model describes long-lived objects and their stable links.**
  Check: components are created and wired at startup and keep their references stable during the process lifetime.

* **Minimal required block types are only Ports and Resources.**
  Check: every external signal is handled by a Port, and effects are performed through Resources.

* **Additional block types are optional and introduced only when needed (KISS).**
  Check: Operations, Domain Operations, and Primitive Resources exist only where the problem requires them.

* **Dependency constraints between block types are enforced.**
  Check: the artifact shows all links and allows validating the following rules.

  * Ports cannot be linked to other Ports.
  * Operations cannot be linked to other Operations.
  * A Resource can have incoming links either:
    * from a single Resource (being a Primitive Resource / implementation detail), or
    * from any number of Operations.

* **A Port may be linked to multiple Operations and Resources.**
  Check: the component-level graph may contain multiple outgoing edges from a Port.
  Check: each Port method still performs exactly one call to an Operation or to a Resource method.

* **Coupling is controlled by a degree limit.**
  Check: for each node, count links.
  Guideline: more than 4 links is discouraged, more than 8 links is strongly discouraged.

### 2.4. Minimal notation

The minimal notation describes a directed graph of components.

#### Element types

* **Port (`Port`)** — an entrypoint handling an external signal (HTTP controller, message listener, scheduler handler).
* **Resource (`Resource`)** — a component representing internal state or an external system API (repo/DAO, MQ client, partner REST API client, mail sender).
* **Operation (`Operation`)** — an optional component that performs multiple effects over one or multiple resources in response to a signal.
* **Domain Operation (`DomainOperation`)** — an optional reusable effect composition created inside an Operation (not a DI component by default).
* **Primitive Resource (`PrimitiveResource`)** — an optional resource that is an implementation detail of another Resource.

#### Edge types

* `calls`: `Port -> Operation|Resource`
* `uses`: `Operation -> Resource`
* `implements_with`: `Resource -> PrimitiveResource`
* `creates`: `Operation -> DomainOperation`

#### Canonical textual format (for AI)

```yaml
components:
  ports:
    - name: HttpControllerA
      calls: [OpReplicate]

  operations:
    - name: OpReplicate
      uses: [Repo, MessageQueue, ExternalSystem1, ExternalSystem2]
      creates: [SendToMq, PushToExt1, PushToExt2]

  resources:
    - name: Repo
      implements_with: [SqlDao, MinioClient]
    - name: MessageQueue
    - name: ExternalSystem1
    - name: ExternalSystem2

  primitive_resources:
    - name: SqlDao
    - name: MinioClient
```

### 2.5. Construction algorithm

1. Fix Ports.
   Input: list of external signals (HTTP endpoints, MQ topics/queues, scheduled triggers).
   Output: a list of Ports and a mapping “signal -> Port”.

2. Identify Resources.
   Input: where the system stores and mutates state, and which external systems it integrates with.
   Output: a list of Resources.

3. Decide whether an Operation is needed for each Port.
   Input: external signal and the number of effects required.
   Output: for each external signal handled by the Port, decide whether it is implemented as a direct edge `Port -> Resource` (single effect) or as an edge `Port -> Operation` (multiple effects/resources).

4. Make effects explicit through Operation dependencies.
   Input: for each Operation, the list of effects and the target Resources.
   Output: Operation depends directly on the Resources it affects.

5. Factor out reusable effect compositions as Domain Operations.
   Input: repeated effect sequences across multiple Operations.
   Output: Domain Operation procedures/functions (or manually-created objects) that take required Resources as parameters.

6. Decompose complex Resources into Primitive Resources.
   Input: Resources that internally use multiple infrastructure clients (DB, object storage, MQ, etc.).
   Output: Resource includes Primitive Resources but exposes a stable API without leaking infrastructure types.

7. Validate the graph against invariants.
   Input: the graph artifact.
   Output: a checklist pass confirming block-type constraints and degree constraints.

### 2.6. Common mistakes (anti-patterns)

* **Operations call other Operations.**
  Detection: dependency edge `Operation -> Operation`.
  Highlight: “Operations are top-level scenarios; do not chain them.”
  Auto-correct: merge, or extract common part into a Domain Operation.

* **Resources become orchestrators.**
  Detection: a Resource coordinates multiple other Resources to implement a scenario.
  Highlight: “Scenario composition belongs to Operations.”
  Auto-correct: move orchestration into an Operation.

* **Excessive dependencies per component.**
  Detection: a node exceeds 8 dependencies.
  Highlight: “High degree indicates coupling and unclear boundaries.”
  Auto-correct: introduce a higher-level Resource abstraction that encapsulates multiple resources, or split the scenario.

* **Primitive resources leak to operations/ports.**
  Detection: Operations depend on low-level infrastructure clients directly.
  Highlight: “Primitive resources should be hidden behind Resources.”
  Auto-correct: introduce or extend a Resource that owns the primitive.
