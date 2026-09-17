# Manuscript consistency addendum

Date: 2026-09-16. Decision: **advance retained**.

I compared `work/manuscript.typ` against the previously reviewed construction,
proof and executable evidence, and inspected the mathematical arc content of
its three SVG figures. This is a theorem/construction consistency check. PDF
rendering and visual-layout inspection are being handled by the main researcher.
The algorithm and checkers are unchanged; no full suite was rerun.

## Findings

No new or stronger unsupported mathematical claim was found. Theorem 1 retains
the exact binary input restriction, variable threshold, same labeled leaves,
linear graph size, deterministic polynomial map and arbitrary-valid-witness
recovery. The explicit exclusions immediately following it prevent an inference
of constant-threshold, bounded-taxon, bounded-level or edit-distance hardness.

The incidence arcs, two marked paths, auxiliary labels, spine port order and
spine node count agree with the reviewed rule. Lemmas 1–4 preserve the legality,
forcing, counting and connectivity arguments without dropping a needed premise.
Completeness retains exact quotient-arc equality and the admissibility
characterization. Runtime and encoding bounds remain the reviewed polynomial
bounds. The figures depict the stated omitted components and the two-input,
two-output spine correctly.

The manuscript now explicitly attributes the reversal principle to Proposition
7/Figure 3, addressing the original review's nonblocking recommendation. The
novelty and expert-assessment qualifications are retained. Its description of
my independent checks matches the saved results: eight sources, nine queries,
twelve recovery calls, including two free-variable witnesses and the merged
path case. The 139/109 numbers are the respective maxima for the left/right
network orders in that suite.

## Optional wording clarifications

These are editorial ambiguities, not proof gaps or conditions on advancement:

- At `manuscript.typ:31`, write the conversion explicitly as
  `|I(M)| > q iff |I(M)| >= q+1`. “Increasing the threshold” otherwise leaves
  the direction of conversion implicit.
- At `manuscript.typ:116`, replace “each fixed-group replacement and its cherry
  parent” with “each fixed-group replacement into its designated group bag,
  and each cherry parent C_g into group g.” Only R, A and B have the added
  cherries; U_j and V_j do not. The existing construction and subsequent proof
  already determine the intended partition unambiguously.
- At `manuscript.typ:149`, “largest left and right input orders” is clearer than
  “largest two input orders,” since other tested left orders exceed 109.

No theorem-level repair or additional candidate execution is needed for this
manuscript version. The original bounded literature-coverage limitations and
need for human expert assessment continue to apply.
