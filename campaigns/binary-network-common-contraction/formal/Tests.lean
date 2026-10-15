import Challenge
open BinaryNetworkCommonContraction
example : contract ([0,1,2],[(0,1),(1,2)]) (0,1) = some ([0,2],[(0,2)]) := by native_decide
example : contract ([0,1],[(0,1)]) (0,1) = none := by native_decide
example : contract ([0,1,2],[(0,1),(0,2),(2,1),(1,2)]) (0,1) = none := by native_decide

example : contract ([0,1,2,3],[(0,1),(0,2),(2,1),(1,3)]) (0,1) = none := by native_decide
