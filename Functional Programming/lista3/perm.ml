module type OrderedType = 
sig
    type t
    val compare : t -> t -> int
end

module type S = 
sig
    type key
    type t

    val apply : t -> key -> key
    val id : t
    val invert : t -> t
    val swap : key -> key -> t
    val compose : t -> t -> t
    val compare : t -> t -> int
end

module Make(Key : OrderedType) = 
struct 
  
  module Aux = Map.Make(Key)

  type t = |Permutacja of (Key.t Aux.t) *  (Key.t Aux.t) 

  let (id:t) = Permutacja (Aux.empty, Aux.empty)

  let apply perm k = 
    let Permutacja (perm, inver) = perm in    
      match Aux.find k perm with 
            | exception Not_found -> k 
            | value               -> value;;

  let invert perm = 
    let Permutacja (perm, inver) = perm in 
    Permutacja (inver,perm);;

  let swap key1 key2 = 
    Permutacja (Aux.add key1 key2 (Aux.add key2 key1 Aux.empty), 
      Aux.add key2 key1 (Aux.add key1 key2 Aux.empty));;

  let compose p1 p2 = 
    let Permutacja (p1, inv1) = p1 in 
    let Permutacja (p2, inv2) = p2 in

    let apply2 p k =     
      match Aux.find k p with 
              | exception Not_found -> k 
              | value               -> value in

    let merge p1 p2 = 
      let singleKeyCompose k x y = 
        match x with 
        | None   -> Some (apply2 p2 k) 
        | Some x -> Some (apply2 p2 x)
      in Aux.merge singleKeyCompose p1 p2 in 

    Permutacja (merge p1 p2, merge inv2 inv1)

  let compare p1 p2 = 
    Aux.compare Key.compare p1 p2 

end 