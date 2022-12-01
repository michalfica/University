type fraction  = | Frac of int * int 
type interval  = | Inter of fraction * fraction 

let add f1 f2 = match f1, f2 with 
  | Frac(a,b), Frac(c,d) -> Frac(a+c,b+d)

type lazy_tree = 
  | LTree of interval * (unit -> lazy_tree) * (unit -> lazy_tree) 

let label_of_LTree = function 
  | LTree(Inter(beg,endd), left, right) -> add beg endd  

let rec create_ltree inter = match inter with 
    | Inter(beg,endd) -> 
      let mid = add beg endd in 
      LTree( inter, 
             (fun () -> create_ltree (Inter(beg,mid))), 
             (fun () -> create_ltree (Inter(mid,endd))) )

let rec rational_num = create_ltree (Inter(Frac(0,1),Frac(1,0)))