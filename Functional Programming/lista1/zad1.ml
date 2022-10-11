fun x -> x;;
(* - : 'a -> 'a = <fun> *)

(* TYPE int -> int = <fun> *)
(* E.g: *) fun x -> x + 1;;

(* TYPE (’a -> ’b) -> (’c -> ’a) -> ’c -> ’b *)
(* E.g *) fun f -> fun g -> fun x -> (f)  ((g) x);;

(* TYPE ’a -> ’b -> ’a *)
(* E.g *) fun x -> fun y -> x;;

(* TYPE ’a -> ’a -> ’a *)
(* E.g *) fun y -> fun x -> if x>y then x else y;;