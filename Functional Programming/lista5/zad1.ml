let rec fix f x = f (fix f) x 

let fib_f fib n =
  if n <= 1 then n
  else fib (n-1) + fib (n-2)

(* ---------------------- *)
(*          ZAD 1         *)
(* ---------------------- *)
 
let rec fix_with_limit limit f = 
  fun (x) -> 
    match limit with 
    | 0 -> failwith "limit exceeded"
    | n -> f (fix_with_limit (limit-1) f) x
let fib_with_limit = fix_with_limit 10 fib_f
let fib_array = Hashtbl.create 1000

(* ZBYT SKOMPLIKOWANE ... *)
let rec fix_memo f =
  fun (x) ->
    match Hashtbl.find_opt fib_array x with
    | Some y -> y 
    | None   ->
      let result = (f (fun(n) -> (fix_memo f) (n)))(x) in 
      let _ = Hashtbl.add fib_array x result in
      result 
let fib = fix_memo fib_f
  