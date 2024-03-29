type term = | Var of string 
            | Sym of string * term list 

type formula = | False 
               | Variable of string 
               | Implication of formula * formula
               | R_application of string * int * term list 
               | For_all of term * formula  (** tutaj term musi być zmienną termową *)

let rec list_to_string xs =
  match xs with 
  | []    -> ""
  | x::xs -> x ^ list_to_string xs

let rec string_of_term t =  
  begin match t with 
  | Var x       -> x
  | Sym (s, xs) -> s ^ "(" ^ (list_to_string (List.map (fun t -> (string_of_term t) ^ ", ") xs)) ^ ")"
  end 

let rec string_of_formula f =
  begin match f with
  | False                -> "⊥"
  | Variable p           -> p 
  | Implication (f1, f2) -> 
    let s1 = (string_of_formula f1) in
    let s2 = (string_of_formula f2) in
    begin match f1 with 
    | False | Variable _ -> s1 ^ " → " ^s2
    | _                  -> "(" ^ s1 ^ ")" ^ " → " ^ s2 
    end 
  | R_application (r,n,xs) -> r ^ "(" ^ (list_to_string (List.map (fun t -> (string_of_term t) ^ ", ") xs)) ^ ")" 
  | For_all (Var x, f)     -> "∀ " ^ x ^ ". " ^ (string_of_formula f)
  | For_all (_, _)         -> failwith "invalid formula" (** should never happen *)
  end

let pp_print_formula fmtr f =
  Format.pp_print_string fmtr (string_of_formula f)

type theorem = Theorem of formula list * formula
let assumptions thm = match thm with 
  | Theorem(assumptions, consequence) -> assumptions
let consequence thm = match thm with 
  | Theorem(assumptions, consequence) -> consequence

let pp_print_theorem fmtr thm =
  let open Format in
  pp_open_hvbox fmtr 2;
  begin match assumptions thm with
  | [] -> ()
  | f :: fs ->
    pp_print_formula fmtr f;
    fs |> List.iter (fun f ->
      pp_print_string fmtr ",";
      pp_print_space fmtr ();
      pp_print_formula fmtr f);
    pp_print_space fmtr ()
  end;
  pp_open_hbox fmtr ();
  pp_print_string fmtr "⊢";
  pp_print_space fmtr ();
  pp_print_formula fmtr (consequence thm);
  pp_close_box fmtr ();
  pp_close_box fmtr ()

(* --------------------------------------------------------------- *)
(* ---------------------- sprawdzenie czy zmienna jest wolna ------*)
(** compute or map on list of bool *)
let rec or_map xs =
  match xs with 
  | []    -> false 
  | x::xs -> x || or_map xs   

(** checks if `var` appears in term `t` *)
let rec free_in_term var t = 
  match t with 
  | Var x       -> if var=x then true else false  
  | Sym (f, xs) -> or_map (List.map (fun x -> (free_in_term var x)) xs) 

(** checks if `var` appears in `f` and is not quantified in `f` *)
let rec free_in_formula var f = 
  match f with 
  | For_all (Var x, f) ->
    (* let _ = print_string x in  *)
    if var=x then false else free_in_formula var f 
  | Variable x              -> var=x  
  | Implication(f1, f2)     -> free_in_formula var f1 || free_in_formula var f2 
  | R_application(r, n, xs) -> or_map (List.map (fun t -> (free_in_term var t)) xs)
  | _              -> false  
(* --------------------------------------------------------------- *)
(* ------------------------------------PODSTAWIANIE--------------- *)
(** returns first var which not appears in `f` nor in `t` or appers but quantified *)
let next_var_name f t = 
  let rec aux f t var =
    let v = "x" ^ string_of_int var in 
    let _ = print_string ("sprawdzam " ^ v ^ "\n") in
    if (free_in_formula v f) || (free_in_term v t)
      then aux f t (var + 1) 
      else v
  in aux f t 0 

(** substitute term `s` for each FREE occurence of `x` in `t` *)
let rec subst_in_term_slow x s t = 

  match t with 
  | Var a      -> if a=x then s else Var a 
  | Sym(f, xs) -> Sym(f, List.map (subst_in_term_slow x s) xs) 

(** substitute term `s` for each FREE occurence of `x` in `t` 
    not sure about result on Variable a *)
let rec subst_in_formula_slow x s f = 
  match f with 
  | False                   -> False 
  | Variable a              -> Variable a (*if a=x then s else Variable a*) 
  | Implication(f1, f2)     -> Implication(subst_in_formula_slow x s f1, subst_in_formula_slow x s f2)
  | R_application(r, n, xs) -> R_application(r, n, List.map (subst_in_term_slow x s) xs)
  | For_all(Var a, f)       -> 
    if a=x then For_all(Var a, f) (* nie ma żadnych wolnych wystapien x *)
    else 
      if not (free_in_term a s) 
      then For_all(Var a, subst_in_formula_slow x s f)
      else let z = next_var_name f s in 
        let formula_bez_a = (subst_in_formula_slow a (Var z) f) in
        let formula_bez_x = (subst_in_formula_slow x s formula_bez_a) in 
        For_all(Var z, formula_bez_x)
  | _ -> failwith "Invalid formula" (** should never happen *)
(* --------------------------------------------------------------- *)
(* ------------------PODSTAWIANIE_ZA_WSZYSTKO_NARAZ--------------- *)
module VarMap = Map.Make(String)
let counter = ref 0
let fresh_var () = counter := (!counter) + 1; "x" ^ string_of_int !counter

let rec psubst_in_term map t =
  match t with 
  | Var a -> let z = try VarMap.find a map with Not_found -> Var a in 
    z
  | Sym(f, xs) -> Sym(f, List.map (psubst_in_term map) xs)
let subst_in_term x s t = psubst_in_term (VarMap.singleton x s) t 

let rec psubst_in_formula map f = 
  match f with 
  | False                   -> False 
  | Variable a              -> Variable a (*if a=x then s else Variable a*) 
  | Implication(f1, f2)     -> Implication(psubst_in_formula map f1, psubst_in_formula map f2)
  | R_application(r, n, xs) -> R_application(r, n, List.map (psubst_in_term map) xs)
  | For_all(Var a, f)       -> 
    let check = VarMap.exists (fun key value -> key=a) map in 
    if check then For_all(Var a, psubst_in_formula (VarMap.remove a map) f) (* nie ma żadnych wolnych wystapien x *)
             else let check = VarMap.exists (fun key value -> free_in_term a value) map in 
                  if check then let new_var = Var (fresh_var ()) in For_all(new_var, psubst_in_formula (VarMap.add a new_var map) f)
                  else For_all(Var a, psubst_in_formula map f)
  | _ -> failwith "Invalid formula" (** should never happen *)

let subst_in_formula x s f = psubst_in_formula (VarMap.singleton x s) f 
(* --------------------------------------------------------------- *)
(* ----------------------------------- RÓWNOŚĆ FORMUŁ ------------ *)
let rec and_map xs = 
  match xs with 
  | [] -> true 
  | x::xs -> x && and_map xs 

let rec eq_term t1 t2 = 
  match t1, t2 with
  | Var x, Var y -> x=y 
  | Sym(f, xs), Sym(g, ys) -> f=g && List.length xs = List.length ys && (and_map (List.map2 (fun i j -> eq_term i j) xs ys))
  | _, _ -> false 

let next_var_name_f f1 f2 = 
  let rec aux var =
    let v = "x" ^ string_of_int var in 
    if (free_in_formula v f1) || (free_in_formula v f2)
      then aux (var + 1) 
      else v
  in aux 0 

  let rec eq_formula f1 f2 = 
  match f1, f2 with 
  | False, False           -> true 
  | Variable x, Variable y -> x=y 
  | Implication(f1, f2), Implication(g1, g2) 
                           -> eq_formula f1 g1 && eq_formula f2 g2
  | R_application(r1, n, xs), R_application(r2, m, ys) 
                           -> r1=r2 && n=m && and_map (List.map2 (fun i j -> eq_term i j) xs ys) 
  | For_all(Var x, f1), For_all(Var y, f2) 
                           -> let z = Var (next_var_name_f f1 f2)  in 
                              let f1_bez_x = subst_in_formula x z f1 in 
                              let f2_bez_y = subst_in_formula y z f2 in 
                              eq_formula f1_bez_x f2_bez_y 
  | _, _ -> false
(* --------------------------------------------------------------- *)
(* -------------------------------- REGUŁY DOWODZENIA ------------ *)

let by_assumption f = Theorem([f], f)

let imp_i f thm =
  let remove sigma asmp = List.filter (fun form -> if form=sigma then true else false) asmp in 
  match thm with 
  | Theorem(assumptions, consequence) -> Theorem(remove f assumptions, Implication(f,consequence))

let imp_e th1 th2 =

  let rec remove_duplicates lst = 
    match lst with
    | [] -> []
    | h::t -> h::(remove_duplicates (List.filter (fun x -> x<>h) t)) in 

  match th1, th2  with
  |Theorem(a1,Implication(f1,f2)), Theorem(a2,f) when  f1=f                                   
      -> Theorem(remove_duplicates (a1 @ a2), f2)
  | _ -> failwith "invalid arguments"

let bot_e f thm =
  match thm with
  | Theorem(a,False) -> Theorem(a,f)
  | _                -> failwith "invalid arguments"    


(** val for_all : theorem -> string -> theorem *)
let for_all th x = 
  match th with 
  | Theorem(assumptions, consequence) -> 
    let condition = or_map (List.map (free_in_formula x) assumptions) in 
    if condition then failwith "invalid argments"
    else Theorem(assumptions, For_all(Var x, consequence))

(** val exist : theorem -> theorem *)
let exist th t = 
  match th with 
  | Theorem(a, For_all(Var x, f)) -> 
    let new_f = subst_in_formula x t f in 
    Theorem(a, new_f)
  | _ -> failwith "invalid arguments"

let prosta_formula = Implication (Variable "p", Variable "q")
let formula3przyklad = Implication( Implication(Variable "p", Implication(Variable "q", Variable "r")), 
                                    Implication(Implication(Variable "p", Variable "q"),
                                                Implication(Variable "p", Variable "r")) )