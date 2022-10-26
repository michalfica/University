
type properties = { value : int; spine : int }
type tree = Leaf | Node of tree * properties * tree

(* Leaf też powinnien mieć wysokość (najlepiej funkcja rank) -> upraszcza kod *)
(* Joint (lepsza nazwa: merge) powinno korzystać z add *)

(* -------------------- *)
(*  przykladowe drzewka *)
(* -------------------- *)

let drzewko1 =
  Node
    ( Node
        ( Node (Leaf, { value = 8; spine = 1 }, Leaf),
          { value = 7; spine = 2 },
          Node (Leaf, { value = 9; spine = 1 }, Leaf) ),
      { value = 5; spine = 2 },
      Node (Leaf, { value = 6; spine = 1 }, Leaf) )

let drzewko2 = Node (Leaf,{value=10;spine=1},Leaf)

(* tree1 i tree2 to poprawne drzew lewicowe
   LEWYM poddrzewem ma być to z drzew t1 t2 które ma większy spine *)

let add tree1 tree2 x =
  match (tree1, tree2) with
  | Leaf, Leaf                                  -> Node (Leaf, { value = x; spine = 1 }, Leaf)
  | Leaf, Node (l, p, r) | Node (l, p, r), Leaf -> Node (Node (l, p, r), { value = x; spine = 1 }, Leaf)
  | Node (l1, p1, r1), Node (l2, p2, r2) -> (
      match p1.spine > p2.spine with
      | true  -> Node( Node (l1, p1, r1), { value = x; spine = p2.spine + 1 }, Node (l2, p2, r2) )
      | false -> Node( Node (l2, p2, r2), { value = x; spine = p1.spine + 1 }, Node (l1, p1, r1) ))

let rec joint tree1 tree2 = 
  begin match tree1, tree2 with 
  (* | Leaf, tree | tree, Leaf -> tree *)
  | Leaf, Leaf -> Leaf
  | Leaf, Node(l1,p1,r1) | Node(l1,p1,r1), Leaf -> Node(l1,p1,r1)
  | Node(l1,p1,r1), Node(l2,p2,r2) ->
    begin match p1.value <= p2.value with
    | true  -> (* l1 {p1.value;spine} (joint r1 Node (l2,p2,r2)) *)
      let Node (sbl, sbp, sbr) = (joint r1 (Node (l2,p2,r2))) in (* wynik joint nie może być liściem *)
      begin match l1 with (* l1 może być liściem *)
      | Leaf -> Node (Node (sbl, sbp, sbr),{value=p1.value;spine=1},l1) 
      | Node (l1l, l1p, l1r) -> 
        begin match sbp.spine < l1p.spine with
        | true  -> Node (l1,{value=p1.value;spine=sbp.spine+1},Node (sbl, sbp, sbr))
        | false -> Node (Node (sbl, sbp, sbr),{value=p1.value;spine=l1p.spine+1},l1) 
        end
      end  
    | false -> joint tree2 tree1 
    end 
  end 


let insert tree x = joint tree (Node (Leaf, {value=x;spine=1}, Leaf)) 
let delete_min = function 
  | Leaf -> Leaf 
  | Node (l,p,r) -> joint l r

