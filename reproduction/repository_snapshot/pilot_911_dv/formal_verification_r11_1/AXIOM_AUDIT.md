# R11.1 axiom audit

Command: pinned `lake -Kjobs=1 build`, with every named theorem listed through `#print axioms` in `FormalVerification.lean`.

Result: `PASS`.

| Module | Named theorems | Dependency union |
|---|---:|---|
| `BasicDefinitions` | 2 | `propext`, `Classical.choice`, `Quot.sound` |
| `PublicStates` | 3 | none or `propext` |
| `Kitagawa` | 2 | standard Lean foundations |
| `CompositionOnly` | 5 | standard Lean foundations |
| `BridgeProduct` | 6 | standard Lean foundations |
| `Frechet` | 5 | standard Lean foundations |
| `QueueFlow` | 6 | standard Lean foundations |
| `IdentifiedSets` | 3 | none or standard Lean foundations |
| `DVClassification` | 5 | standard Lean foundations |
| `SelectionBounds` | 5 | standard Lean foundations |
| `PriorityHistory` | 5 | none or standard Lean foundations |
| `WitnessDeletion` | 2 | none or standard Lean foundations |
| `Regularization` | 2 | standard Lean foundations |
| `DeterministicTransform` | 3 | `propext`, `Quot.sound` |
| `Standardization` | 3 | standard Lean foundations |
| `JointMass` | 3 | standard Lean foundations |
| `WitnessRegimes` | 2 | standard Lean foundations |
| `SetPropagation` | 3 | none |
| **Total** | **65** | **No project-defined axioms** |

`propext`, `Classical.choice`, and `Quot.sound` are standard Lean foundations used by Mathlib and real-number reasoning. The package contains no `native_decide` proof axiom. The finite 54-regime theorem uses kernel-reduced `decide`.

Focused source scans found:

- zero declarations beginning with `axiom`;
- zero `sorry` placeholders;
- zero `admit` placeholders.

This audit concerns proof dependencies. It does not validate the paper-to-Lean semantic mapping.
