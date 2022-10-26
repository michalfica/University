(* CEL: perms xs -> wszystkie permutacje xs *)

let wstaw x xs =
  let rec wstaw_rek x pref xs acc =
    (* wstaw x miedzy pref a xs i dorzuć powstałą liste do acc *)
    match xs with
    | [] -> (pref @ [ x ]) :: acc
    | hd :: tl -> wstaw_rek x (pref @ [ hd ]) tl ((pref @ (x :: xs)) :: acc)
  in
  wstaw_rek x [] xs []

let foo x tail_perms =
  List.fold_right
    (fun tail_perm perms_with_x -> List.append (wstaw x tail_perm) perms_with_x)
    tail_perms []

let perms xs = List.fold_right foo xs [ [] ]

(* komentarz : bind i monady (listy tworzą monade) *)

