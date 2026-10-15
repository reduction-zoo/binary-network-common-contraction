module

public import Mathlib.Computability.TuringMachine.Computable

@[expose] public section

namespace BinaryNetworkCommonContraction

/-- Q001's self-delimiting binary natural; length is logarithmic, not unary. -/
def encodeNat (n : Nat) : List Bool :=
  let bits := (Nat.toDigits 2 n).map (fun c => c == '1')
  List.replicate bits.length true ++ [false] ++ bits

def encodeList {α : Type} (encode : α → List Bool) (xs : List α) : List Bool :=
  encodeNat xs.length ++ xs.flatMap encode

def encodeOption {α : Type} (encode : α → List Bool) : Option α → List Bool
  | none => [false]
  | some x => true :: encode x

/-- None denotes mathematical nonexistence, never an execution error. -/
def searchOutput {I W : Type} (legal : I → Bool) (witness : I → W → Bool)
    (x : I) : Option W → Prop
  | some w => legal x = true ∧ witness x w = true
  | none => legal x = true ∧ ¬ ∃ w, witness x w = true

/-- Relational version for witnesses with quantified real or optimality conditions. -/
def relationalOutput {I W : Type} (legal : I → Bool) (witness : I → W → Prop)
    (x : I) : Option W → Prop
  | some w => legal x = true ∧ witness x w
  | none => legal x = true ∧ ¬ ∃ w, witness x w

structure Formula where
  n : Nat
  clauses : List (List Nat)
  deriving Repr

def legalSource (x : Formula) : Bool :=
  x.clauses.all (fun c => decide c.Nodup && c.all (fun v => v < x.n))

def sourceWitness (x : Formula) (a : List Bool) : Bool :=
  a.length == x.n && x.clauses.all (fun c =>
    c.any (fun v => a[v]? == some true) && c.any (fun v => a[v]? == some false))

def encodeSource (x : Formula) : List Bool :=
  encodeNat x.n ++ encodeList (encodeList encodeNat) x.clauses
structure Digraph where
  n : Nat
  arcs : List (Nat × Nat)
  deriving Repr

def legalDigraph (g : Digraph) : Bool :=
  decide g.arcs.Nodup && g.arcs.all (fun e => e.1 < g.n && e.2 < g.n)
def indegree (g : Digraph) (v : Nat) := (g.arcs.filter (fun e => e.2 == v)).length
def outdegree (g : Digraph) (v : Nat) := (g.arcs.filter (fun e => e.1 == v)).length
def acyclic (g : Digraph) : Bool := (List.range g.n).permutations.any (fun order =>
  g.arcs.all (fun e => order.idxOf e.1 < order.idxOf e.2))
def encodeDigraph (g : Digraph) := encodeList encodeNat (List.range g.n) ++
  encodeList (fun e => encodeNat e.1 ++ encodeNat e.2) g.arcs

structure Network where
  graph : Digraph
  leaves : List Nat
  deriving Repr
def legalNetwork (x : Network) : Bool :=
  legalDigraph x.graph && acyclic x.graph &&
  ((List.range x.graph.n).filter (fun v => indegree x.graph v == 0)).length == 1 &&
  decide (x.leaves.Perm ((List.range x.graph.n).filter (fun v => outdegree x.graph v == 0))) &&
  (List.range x.graph.n).all (fun v =>
    let i := indegree x.graph v
    let o := outdegree x.graph v
    (i == 0 && o == 2) || (i == 1 && o == 2) || (i == 2 && o == 1) || (i == 1 && o == 0))
abbrev Current := List Nat × List (Nat × Nat)
def contract (g : Current) (edge : Nat × Nat) : Option Current :=
  if g.2.contains edge && g.2.any (fun e => e.1 == edge.1) && g.2.any (fun e => e.1 == edge.2) then
    let rename := fun v => if v == edge.2 then edge.1 else v
    let vertices := g.1.erase edge.2
    let arcs := ((g.2.map (fun e => (rename e.1,rename e.2))).filter (fun e => e.1 != e.2)).eraseDups
    if vertices.permutations.any (fun order => arcs.all (fun e => order.idxOf e.1 < order.idxOf e.2))
    then some (vertices,arcs) else none
  else none
def contractions : Current → List (Nat × Nat) → Option Current
  | g, [] => some g
  | g, e :: rest => do
    let next ← contract g e
    contractions next rest
structure Instance where
  left : Network
  right : Network
  bound : Nat
  deriving Repr
structure Witness where
  leftSteps : List (Nat × Nat)
  rightSteps : List (Nat × Nat)
  image : List Nat
  deriving Repr
def legalTarget (x : Instance) := legalNetwork x.left && legalNetwork x.right && x.left.leaves.length == x.right.leaves.length
def targetWitness (x : Instance) (w : Witness) : Bool :=
  match contractions (List.range x.left.graph.n,x.left.graph.arcs) w.leftSteps,
      contractions (List.range x.right.graph.n,x.right.graph.arcs) w.rightSteps with
  | some a, some b =>
    decide (w.image.Perm b.1) && w.image.length == a.1.length &&
    let image := fun v => w.image[a.1.idxOf v]?.getD 0
    a.1.all (fun u => a.1.all (fun v => a.2.contains (u,v) == b.2.contains (image u,image v))) &&
    (x.left.leaves.zip x.right.leaves).all (fun (u,v) => image u == v) &&
    (a.1.filter (fun v => a.2.any (fun e => e.1 == v))).length ≥ x.bound
  | _, _ => false
def encodeNetwork (x : Network) := encodeDigraph x.graph ++ encodeList encodeNat x.leaves
def encodeTarget (x : Instance) := encodeNetwork x.left ++ encodeNetwork x.right ++ encodeNat x.bound
def encodeSteps := encodeList (fun e : Nat × Nat => encodeNat e.1 ++ encodeNat e.2)
def encodeWitness (w : Witness) := encodeSteps w.leftSteps ++ encodeSteps w.rightSteps ++ encodeList encodeNat w.image
def validSourceOutput := searchOutput legalSource sourceWitness
def validTargetOutput := searchOutput legalTarget targetWitness

/-- Both algorithms use Q001's explicit bit encoding and TM2 cost model.
Recovery receives the full pair of source instance and target output. -/
def Reduction (forward : Formula → Instance)
    (recover : Formula × Option Witness → Option (List Bool)) : Prop :=
  Nonempty (Turing.TM2ComputableInPolyTime encodeSource encodeTarget forward) ∧
  Nonempty (Turing.TM2ComputableInPolyTime
    (fun input => encodeSource input.1 ++ (encodeOption encodeWitness) input.2)
    (encodeOption (encodeList (fun b => [b]))) recover) ∧
  (∃ bound : Polynomial Nat, ∀ x,
    (encodeTarget (forward x)).length ≤ bound.eval (encodeSource x).length) ∧
  (∃ bound : Polynomial Nat, ∀ input,
    ((encodeOption (encodeList (fun b => [b]))) (recover input)).length ≤
      bound.eval (encodeSource input.1 ++ (encodeOption encodeWitness) input.2).length) ∧
  (∀ x, legalSource x = true → legalTarget (forward x) = true) ∧
  (∀ x, legalSource x = true → ∀ y, validTargetOutput (forward x) y →
    validSourceOutput x (recover (x, y)))


def Goal : Prop :=
  ∃ (forward : Formula → Instance)
    (recover : Formula × Option Witness → Option (List Bool)), Reduction forward recover

/-- Open question only; this placeholder is not a solution. -/
theorem solve : Goal := by
  sorry

end BinaryNetworkCommonContraction
