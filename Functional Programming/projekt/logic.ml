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
let rec list_to_bool xs =
  match xs with 
  | []    -> false 
  | x::xs -> x || list_to_bool xs   
let rec free_in_term var t = 
  match t with 
  | Var x       -> if var==x then true else false  
  | Sym (f, xs) -> list_to_bool (List.map (fun x -> (free_in_term var x)) xs) 

let rec free_in_formula var f = 
  match f with 
  | For_all (Var x, f) ->
    if var==x then false else free_in_formula var f 
  | _              -> true 
(* --------------------------------------------------------------- *)

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

let prosta_formula = Implication (Variable "p", Variable "q")
let formula3przyklad = Implication( Implication(Variable "p", Implication(Variable "q", Variable "r")), 
                                    Implication(Implication(Variable "p", Variable "q"),
                                                Implication(Variable "p", Variable "r")) )