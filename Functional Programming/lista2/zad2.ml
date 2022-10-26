(* CEL: sublists xs -> wszystkie polisty (podciągi) xs *)

(* W TEJ WERSJI SĄ NIEUŻYTKI (
  w każdym wywołaniu : List.map (fun seq -> x::seq) sub) *)

(* let sublists xs = List.fold_right 
                  (fun x sub -> List.append (List.map (fun seq -> x::seq) sub) sub)
                  xs 
                  [[]];; *)

let map_app f xs ys = List.fold_right (fun hd mapped_list -> f hd :: mapped_list) xs ys
let sublists xs = List.fold_right 
                  (fun x result -> (map_app (fun seq -> x::seq) result result))
                  xs
                  [[]]

let rec sublists xs =
  match xs with 
  | [] -> [[]]
  | (x::xs) -> let ys = (sublists xs) in List.fold_right (fun e acc -> (x::e) ::acc) ys ys 