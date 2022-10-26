(* CEL: suf  xs -> wszystkie sufiksy  xs 
        pref xs -> wszystkie prefiksy xs *)

let suf xs = List.fold_right (fun x suf_list -> (x::(List.hd suf_list))::suf_list ) xs [[]] 

(* dla [1; 2; 3] -> [ []; [1]; [1; 2]; [1; 2; 3] ] *)

let pref xs = List.rev (List.fold_left (fun acc x -> ((List.hd acc)@[x])::acc) [[]] xs)
(* lepszy pomysł z usuwaniem ostatniego elementu *)

let rec pref xs =
        match x with 
        | [] -> [[]]
        | h::ogon -> 
                let podprefiksy = pref ogon in 
                []  :: (List.map (fun y -> h::y) podprefiksy)

let rec suf x = 
        x::
        match x with 
        | [] -> []
        | h::ogon -> suf ogon;;