(* CEL: merge cmp xs ys -> zs (merge 2 posortowanych list w porządku cmp) *)
(* w wersji nie ogonowej i ogonowej *)

let rec merge cmp xs ys =
  match xs, ys with 
  | xs, [] -> xs
  | [], ys -> ys
  | x::xs, y::ys -> match cmp x y with
                    | true  -> x :: merge cmp xs (y :: ys)  (* x < y *)
                    | false -> y :: merge cmp (x :: xs) ys  (* y < x *)
                    
let rec merge2 cmp xs ys acc = 
  match xs, ys with 
  | xs, [] -> (List.rev acc) @ xs
  | [], ys -> (List.rev acc) @ ys
  | x::xs, y::ys -> match cmp x y with 
                    | true ->  merge2 cmp xs (y::ys) (x::acc)
                    | false -> merge2 cmp (x::xs) ys (y::acc)

let merge_tail cmp xs ys = merge2 cmp xs ys []

(* halve xs -> dzilei liste xs na 2 listy o n/2 elementach *)
(* co drugi elt do jednej co drugi elt do drugiej *)
let rec halve xs = 
  match xs with
  | []       -> [], []
  | [x]      -> [x], []
  | x::y::xs -> let l, r = halve xs in (x::l), (y::r)

let rec mergesort cmp xs = 
  match xs with 
  | [] | [_] -> xs
  | xs  -> let left, right = halve xs in (merge cmp (mergesort cmp left) (mergesort cmp right)) 