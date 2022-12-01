(* zadanie na zastosowania GADT [podobne do przyykładu ewaluatora: https://blog.mads-hartmann.com/ocaml/2015/01/05/gadt-ocaml.html] 
   trudność: czym jest typ z słowem kluczowym format ??? *)

(* CO znaczy słowo kluczowe foramt?  
   za co mają odpowiadać poszczególn konstruktory tego typu? *)
type ('a, 'b) format= 
  | Lit 
  | Int 
  | Str
  | Cat 

let ksprintf : ('a, 'b) format -> (string -> 'b) -> 'a = function 
  | Lit -> failwith "not implemented"
  | Int -> failwith "not implemented"
  | Str -> failwith "not implemented"
  | Cat -> failwith "not implemented"

(* TO DO: użyć ksprintf do napisania sprintf *)

