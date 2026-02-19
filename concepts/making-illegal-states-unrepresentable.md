# Making illegal states unrepresentable

## 2. Concept spec: "Making illegal states unrepresentable"

### 2.1. Intention

This concept is used to reduce defects and incidental complexity by shrinking the set of representable program states to (as much as practical) the set of states the system is prepared to handle correctly.

It replaces repeated, scattered “if this combination is allowed” reasoning with explicit type- and constructor-level constraints, so that illegal states are rejected at construction time (or earlier) and cannot be introduced later by normal usage of the public API.

It provides measurable benefit in tasks such as: domain modeling, API design, refactoring, state-machine design, boundary/DTO-to-domain conversion, and designing invariants that must hold across multiple modules.

### 2.2. Ontological Status

This is a design principle plus a modeling technique: it yields concrete code artifacts (types and constructors/factories/parsers) whose public surface makes certain invalid combinations impossible to express.

It is not:
- a replacement for validating untrusted input (it relocates validation to construction/boundary points, not to “nowhere”);
- a guarantee that all business rules are enforced statically (some rules are dynamic, contextual, or too volatile/costly to encode);
- a security mechanism (it does not address malicious bypass via reflection/unsafe code/serialization hacks unless the environment guarantees those cannot occur).

Operational rule to distinguish “similar but not the same”:
- This concept is applied if illegal states are impossible (or intentionally unreachable) through the public construction and mutation surface of the model.
- If illegal states remain representable and are only prevented by conventions, documentation, or ad-hoc validation calls, the concept is not applied (or is applied only partially at specific boundaries).

Scope boundaries / non-goals:
- It does not prescribe a specific language, paradigm, or persistence strategy.
- It does not require immutability, but it requires that public mutation cannot violate invariants (immutability is one common way to achieve that).
- It does not mandate “encode everything in the type system”; it requires explicit choices about what is prevented by construction vs. what is handled dynamically.

### 2.3. Concept Invariants

Invariant 1 — Explicit legality criteria exist.
- Definition: “Illegal” is defined as a violation of stated invariants of the modeled concept (domain, protocol, lifecycle).
- Verification: the concept application includes an explicit list of invariants (in code as types/constructors and/or in a short textual invariant list near the types).
- Falsifier: “illegal” is used only rhetorically (no explicit invariants), or legality is only implied by tests and scattered checks.

Invariant 2 — A construction boundary prevents illegal values from entering the model.
- Definition: there exists at least one controlled constructor/factory/parser that is the only normal way to create instances that claim the invariant, and it rejects/does not produce illegal values.
- Verification: direct construction is restricted (e.g., private fields/constructors, opaque types, module encapsulation) and creation APIs return either a legal instance or an explicit failure.
- Falsifier: callers can directly instantiate or mutate the value into an illegal form using public APIs.

Invariant 3 — Illegal combinations are eliminated by representation, not by post-hoc checks.
- Definition: the representation is shaped so that invalid combinations cannot be assembled (e.g., via sum types, refined/newtypes, typestate, constrained constructors), rather than “represented and later checked”.
- Verification: illegal combinations are unnameable/unconstructable without bypassing encapsulation; dependent fields are not represented as independent nullable/optional flags where their relationships are enforced only by runtime checks.
- Falsifier: the core model is a “bag of fields” where legality depends on cross-field validation performed elsewhere.

Invariant 4 — Public transitions preserve invariants.
- Definition: any public operation that changes the state either (a) cannot produce illegal states by construction, or (b) yields an explicit failure instead of producing an illegal value.
- Verification: state-changing APIs are total over legal inputs and do not expose setters/mutators that can break invariants; transitions between states are represented as functions producing the next legal type/state or a failure.
- Falsifier: after creation, normal API usage can drive the instance into an illegal configuration.

Invariant 5 — Failure is not silent.
- Definition: when construction/transition cannot produce a legal value, the failure is surfaced to the caller via an agreed failure channel (e.g., explicit result value or a documented exception) rather than via silent coercion, partial initialization, out-of-band flags, or sentinel values.
- Verification: for each fallible construction/transition, there is exactly one declared failure channel used consistently in the layer/module.
- Falsifier: illegal inputs cause silent coercion, partially-initialized values, sentinel values, or “success” values that violate invariants.

Invariant 6 — The representation supports exhaustive handling of legal variants when branching is required.
- Definition: when the modeled concept has variants (states/cases), branching on them is designed to be checkable for completeness (e.g., exhaustive pattern matching over a closed set).
- Verification: the variant set is closed/explicit (sealed/enum/ADT); adding a new variant forces compiler or tooling-visible updates in handlers.
- Falsifier: variants are encoded as open strings/ints with “default” branches that silently accept unknown states.

Variants / profiles (all share Invariants 1–6; variant-specific aspects are noted):

Variant A — Refined value types (newtypes + smart constructors).
- What it targets: single-value constraints (format, range, non-emptiness, units), lightweight domain primitives.
- Selection criteria: choose when invalidity is local to one value and validation is stable and cheap.
- Variant-specific emphasis: Invariants 2 and 5 are primarily realized via opaque wrappers and construction-time validation.

Variant B — Sum-of-products modeling (closed variants, each with its own data).
- What it targets: illegal combinations caused by “state tag + unrelated optional fields”, protocol variants, domain cases.
- Selection criteria: choose when different cases have different required/forbidden fields or behavior.
- Variant-specific emphasis: Invariants 3 and 6 are primarily realized via closed variant types and exhaustive handling.

Variant C — Typestate / lifecycle types (state machine encoded in types).
- What it targets: illegal transitions (calling operations in the wrong order), staged builders, resource lifecycles.
- Selection criteria: choose when the main risk is misordered usage rather than single-value validation.
- Variant-specific emphasis: Invariant 4 is realized by making transitions consume/produce different state types, preventing calls in the wrong state.

Variant D — Explicit failure in types/signatures (recommended profile).
- What it targets: expected/recoverable failures at boundaries; composition-friendly pipelines; codebases that already standardize on Result/Either/Option or domain result ADTs.
- Selection criteria:
  - Use when the surrounding code in the same layer already uses explicit return-based error signaling.
  - Or when the layer has no established failure signaling yet: pick a single failure channel for the layer and apply it consistently, budgeting the refactoring/propagation cost and aligning with neighboring layers.
  - Use when failure is a normal outcome that callers are expected to branch on locally.
  - Avoid if adopting it would require cascading signature changes across many layers without a clear payoff.
- Operational rule: if chosen, do not mix with throwing in the same layer; provide conversion at the boundary between layers if needed.

Variant E — Exception-based failure channel (compatibility profile).
- What it targets: ecosystems/layers where exceptions are the established “fallible operation” mechanism; cases where introducing Result-types would be disproportionately costly.
- Selection criteria:
  - Use when the surrounding codebase is exception-centric and changing conventions would be high effort.
  - Use when failures are exceptional in the local context and primarily propagated upward.
- Operational rule: exceptions used for construction/transition must be documented and domain-scoped (not silent null/sentinels); construction must not yield partially valid values.

### 2.4. Minimal Formalization (Vocabulary mode)

Illegal state (for a concept X): a value/configuration that violates the explicit invariants of X.

Representable state space: the set of values/configurations that can be constructed and passed around through normal (public, supported) APIs.

Unrepresentable: impossible to construct/hold/obtain through normal public APIs without bypassing encapsulation or using “unsafe/reflective” escape hatches.

Construction boundary: the smallest surface through which raw/untrusted/loosely-typed data is converted into the constrained representation (parsers, factories, decoders, mappers).

Refined type / newtype: a wrapper around an underlying representation that adds a distinct meaning and enforces constraints at construction.

Smart constructor: a constructor-like function that enforces invariants before producing an instance (often paired with restricted/hidden direct constructors).

Closed variant type (sum type / discriminated union): a type that can be exactly one of a fixed set of variants, each potentially with its own data.

Typestate: a technique where the lifecycle state is carried in the type, restricting available operations and encoding legal transitions as type transformations.

### 2.5. Construction Algorithm

1) Define the target scope.
- Input: a feature/use-case slice or model boundary (e.g., domain entity/value, protocol message, lifecycle object).
- Output: an explicit list of “where illegal states matter” (the scope statement).

2) Enumerate invariants and classify them.
- Input: domain/protocol rules, required fields, lifecycle constraints, allowed transitions.
- Output: an invariant list tagged as (a) value-local, (b) cross-field/case-based, (c) transition-based, (d) contextual/dynamic (left to runtime).

3) Identify boundary points for raw data.
- Input: sources of untrusted/loose data (HTTP/JSON, DB rows, user input, external APIs).
- Output: a map of construction boundaries where parsing/validation must happen.

4) Choose a variant (A/B/C) per invariant cluster.
- Input: invariant tags from step 2.
- Output: selected representation approach(es) with a short justification recorded near the code (or in decision log).

5) Implement constrained representations with restricted construction.
- Input: chosen variants.
- Output:
  - refined types with private fields + smart constructors (Variant A), and/or
  - closed variants with per-variant payloads (Variant B), and/or
  - state-parameterized types with transition functions (Variant C).

6) Choose and apply a failure signaling profile for the layer (Variant D or Variant E).
- Input: current layer conventions + neighboring code conventions + estimated refactoring surface.
- Output:
  - selected profile recorded near the boundary/types (or in decision log),
  - one consistent failure channel for fallible construction/transition within the layer,
  - explicit bridging rules if this layer borders a differently-styled layer.

7) Make failure non-bypassable (regardless of channel).
- Input: construction/transition APIs.
- Output: no public setters/constructors that can create illegal values; no “partially valid” objects; no silent coercion/sentinels.

8) Adapt boundaries to produce only legal representations.
- Input: DTOs/raw inputs.
- Output: boundary code that parses/constructs constrained types; raw types do not flow past the boundary.

9) Add regression checks targeted at the boundary, not scattered across business logic.
- Input: invariant list + boundary map.
- Output: tests (or checks) that (a) invalid raw inputs fail to construct, and (b) legal inputs construct and can be processed without additional validation.

### 2.6. Typical Errors (anti-patterns)

Error 1 — “Bag of fields + boolean/enum tag + many optionals” for case-based models.
- Detection: multiple optional/nullable fields whose validity depends on another field; presence of “state” plus unrelated optional fields.
- Highlight: illegal combinations remain representable; invariants are enforced only by conventions or scattered checks.
- Auto-correction: propose a closed variant type where each variant carries only the fields it needs.

Error 2 — Public constructors/fields allow bypassing invariants.
- Detection: callers can directly instantiate wrappers or set fields without validation.
- Highlight: construction boundary is porous; illegal states can be introduced after validation.
- Auto-correction: make constructors/fields private; expose only smart constructors and safe transitions.

Error 3 — Mixed validated/unvalidated representations in the same layer.
- Detection: both raw primitives and refined/domain types are used interchangeably for the same concept.
- Highlight: invariants are not stable across the codebase; refactoring and reviews become unreliable.
- Auto-correction: enforce “raw only at boundaries” and migrate internal APIs to constrained types.

Error 4 — Mixed failure channels inside one layer (Result/Either in some places, exceptions in others).
- Detection: the same kind of construction/transition failure is sometimes returned as a value and sometimes thrown; frequent ad-hoc conversions at arbitrary depths.
- Highlight: callers cannot predict how to handle failure; composition and refactoring costs rise.
- Auto-correction: pick one profile per layer; move conversions to the boundary between layers.

Error 5 — Introducing explicit Result-types in an exception-centric neighborhood without budgeting propagation cost.
- Detection: widespread signature churn up the call stack; large-scale refactors solely to thread Result/Either; frequent wrapping/unwrapping noise with no local handling.
- Highlight: benefit/cost mismatch; convention divergence from neighboring code.
- Auto-correction: keep the exception-based profile in that layer, or introduce an explicit-result boundary only at the ingress/egress where local handling is needed.

Error 6 — Over-encoding volatile rules into types (type churn).
- Detection: frequent changes require widespread type rewrites; many narrowly-specialized types appear for unstable requirements.
- Highlight: the model is optimizing for the wrong stability horizon.
- Auto-correction: move volatile constraints to runtime validation at boundaries; keep stable core constraints in types.

Error 8 — Mutation can violate invariants after construction.
- Detection: setters or exposed mutable collections/fields can create illegal states post-creation.
- Highlight: invariants are not preserved by public transitions.
- Auto-correction: remove setters; replace with functions that return a new legal value or explicit failure.

## 3. Sources and Attributions

### 3.1. Sources

- Yaron Minsky, “Effective ML Revisited” (Jane Street blog), 2011, section “Make illegal states unrepresentable”. :contentReference[oaicite:0]{index=0}
- Scott Wlaschin, “Designing with types: Making illegal states unrepresentable” (F# for Fun and Profit), 2013. :contentReference[oaicite:1]{index=1}
- Scott Wlaschin, “Domain Modeling Made Functional” (Pragmatic Programmers catalog page), statement on encoding business rules and “making illegal states unrepresentable”. :contentReference[oaicite:2]{index=2}
- Rust API Guidelines, “Type safety” (rust-lang.github.io), guidance on using deliberate types to convey interpretation and invariants. :contentReference[oaicite:3]{index=3}
- Nicolai Parlog, “Make Illegal States Unrepresentable — Data-Oriented Programming v1.1” (Inside.java), 2024. :contentReference[oaicite:4]{index=4}
- Alexis King, “Parse, don’t validate”, 2019. :contentReference[oaicite:5]{index=5}
- HaskellWiki, “smart_constructors” (smart constructor pattern overview). :contentReference[oaicite:6]{index=6}
- Mark Seemann, “Encapsulation in Functional Programming” (Ploeh blog), discussion of invariants and smart constructors. :contentReference[oaicite:7]{index=7}

### 3.2. Direct Borrowings

- The phrase and core example theme “Make illegal states unrepresentable” is attributed to Yaron Minsky’s “Effective ML” material; the OCaml example of refactoring a flat record with many optionals into a variant type is the canonical illustration. :contentReference[oaicite:8]{index=8}
- The emphasis on “encoding business logic/invariants in types” as a primary motivation is aligned with Wlaschin’s “Designing with types” and the “Domain Modeling Made Functional” framing. :contentReference[oaicite:9]{index=9}
- The guideline “use deliberate/custom types to convey interpretation and invariants” is borrowed as an API-design phrasing from Rust API Guidelines. :contentReference[oaicite:10]{index=10}
- The boundary-oriented idea that parsing structured values is preferable to validating less-structured ones is borrowed as a supporting pattern from “Parse, don’t validate”. :contentReference[oaicite:11]{index=11}

### 3.3. Synthesized Elements

- Invariants 1–6 (explicit legality criteria; construction boundary; representation-level elimination; invariant-preserving transitions; explicit fallibility; exhaustiveness) are synthesized as a framework-stable checklist that generalizes:
  - Minsky’s ADT refactoring and exhaustiveness emphasis, :contentReference[oaicite:12]{index=12}
  - Wlaschin’s “designing with types” domain modeling lens, :contentReference[oaicite:13]{index=13}
  - Rust API Guidelines’ invariants-through-types API guidance, :contentReference[oaicite:14]{index=14}
  - Parlog’s DOP principle framing. :contentReference[oaicite:15]{index=15}
- The three variants/profiles (Refined value types; Sum-of-products; Typestate/lifecycle) are synthesized as a selection mechanism:
  - refined/newtype + construction-time validation is supported by Wlaschin’s “designing with types” style and by the broader “parse, don’t validate” boundary approach, :contentReference[oaicite:16]{index=16}
  - sum-of-products is directly supported by Minsky’s refactoring example, :contentReference[oaicite:17]{index=17}
  - lifecycle/transition encoding is a generalization consistent with “illegal states” discussion across typed modeling communities; it is included as a standard profile for “illegal transitions” even when value constraints are minimal. :contentReference[oaicite:18]{index=18}
- The construction algorithm is synthesized to be artifact-verifiable and boundary-first, combining DOP’s “legal combinations representable” framing with typed-construction practices. :contentReference[oaicite:19]{index=19}
- Smart constructor and construction boundary vocabulary definitions are synthesized from the Haskell “smart constructor” pattern description and Seemann’s invariants framing. :contentReference[oaicite:20]{index=20}

### 3.4. Discrepancies and Resolutions

- Terminology discrepancy (“illegal” vs “invalid”): sources use both; this spec treats them as synonymous, preferring “illegal” to match the concept name while defining it operationally as “violates explicit invariants”. :contentReference[oaicite:21]{index=21}
- Emphasis discrepancy (compile-time vs construction-time): some framings imply “compile-time prevention”; this spec resolves by treating “unrepresentable through public APIs” as the criterion, allowing construction-time rejection with explicit failure when static proof is impractical. :contentReference[oaicite:22]{index=22}
- Scope discrepancy (how far to push invariants into types): community discussions warn about overconfidence and requirement volatility; this spec resolves by making “non-goals / scope boundaries” explicit and by including an anti-pattern for over-encoding volatile rules. :contentReference[oaicite:23]{index=23}
