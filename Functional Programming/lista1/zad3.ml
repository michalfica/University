(* Strumień (nieskończony ciąg) typu t to funkcja s: int -> t  *)

(* hd: głowa strumienia, tl: ogon strumienia *)
let hd = fun f -> (f) 0;;
let tl = fun f -> fun x -> (f) x+1;;  

(* add: funkcja, która tworzy strumień większy o stałą od zadanego strumienia *)
(* czy powinna być 2 argumentowa?? *)
let add = fun f -> fun c -> fun x -> c + (f) x;;

(* map *)
let map = fun f -> fun g -> fun x -> (g) ((f) x);;

(* map2 *)
let map2 = fun f s1 s2 -> fun x -> f (s1 x) (s2 x);;

(* replace *)
let replace = fun n a s -> fun x -> if x!=n then s x else a;;

(* take_every *)
let take_every = fun n s -> fun x -> s (n * x);;