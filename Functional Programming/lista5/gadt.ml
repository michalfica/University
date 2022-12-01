type _ ty =
| Int    : int ty
| Bool   : bool ty
| String : string ty
| Pair   : 'a ty * 'b ty -> ('a * 'b) ty
| List   : 'a ty -> 'a list ty

let rec print : type a. a ty -> a -> string =
  fun tp x ->
  match tp with
  | Int    -> string_of_int  x
  | Bool   -> string_of_bool x
  | String -> "\"" ^ String.escaped x ^ "\""
  | Pair(tp1, tp2) ->
    "(" ^ print tp1 (fst x) ^ "," ^ print tp2 (snd x) ^ ")"
  | List tp ->
    "[" ^ String.concat ";" (List.map (print tp) x) ^ "]"