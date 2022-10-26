(* funkcja scan: f, a, s -> new_s  *)

let scan f a s =
  let rec nowy_strumien = function
    | 0 -> f a (s 0)
    | x -> f (nowy_strumien (x - 1)) (s x)
  in
  nowy_strumien

let moj_print x = Printf.printf "%d " x
let print_sequence seq n = List.iter moj_print (List.init n seq)
let ciag x = x;;

print_sequence ciag 10

let test_scan f a s = print_sequence (scan f a s) 10
