(* ZAD 1 *)
(* length [X], rev [X], map [X], rev_map[X], append [X], rev_append [], filter [] *)

let length xs = List.fold_right (fun hd length -> length + 1) xs 0

(* let moj_rev xs =
   let rec rev_rec xs acc =
     match xs with [] -> acc | x :: xs -> rev_rec xs (x :: acc)
   in
   rev_rec xs [] *)
let rev xs = List.fold_left (fun acc x -> x :: acc) [] xs
let map f xs = List.fold_right (fun hd mapped_list -> f hd :: mapped_list) xs []
let rev_map f xs = List.fold_left (fun acc x -> f x :: acc) [] xs
let append xs ys = List.fold_right (fun hd tl -> hd :: tl) xs ys
let rev_append xs ys = List.fold_left (fun acc x -> x :: acc) ys xs

let filter f xs =
  List.fold_right
    (fun hd ys -> if f hd then hd :: ys else ys)
    [] xs
