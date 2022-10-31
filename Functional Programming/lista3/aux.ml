exception Invalid_input
module Aux = Map.Make(Int)
  
let id = (Aux.empty, Aux.empty)

let pusta_perm = id;;
let inna_perm = (Aux.add 2 1 (Aux.add 1 2 Aux.empty), 
                  Aux.add 1 2 (Aux.add 2 1 Aux.empty));;

let apply perm k = 
  let perm, inver = perm in    
    match Aux.find k perm with 
           | exception Not_found -> k 
           | value               -> value;;

(* CO POWINNA ROBIĆ funkcja INVERT ??  *)
(* zamieniać kolejnościa perm i inver  *)
let invert perm = let perm, inver = perm in (inver,perm);;

(* CO POWINNA ROBIĆ funkcja SWAP ?? *)
(* to ma być funkcja, ma przyjąć 2 klucze jako argumenty i 
   zwrócić permutację, która tylko zamienia ze sobą te 2 klucze *)
let swap key1 key2 = 
  (Aux.add key1 key2 (Aux.add key2 key1 Aux.empty), 
    Aux.add key2 key1 (Aux.add key1 key2 Aux.empty));;

    
(* teraz funkcja COMPOSE *)

(* przykłąd do funkcji merge:
    https://stackoverflow.com/questions/3751596/ocaml-semantics-of-merge-in-functor-map-make *)