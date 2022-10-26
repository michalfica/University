
let ctrue prawda falsz =
  let warunek = prawda <> falsz in
  prawda

let cfalse prawda falsz =
  let warunek = prawda <> falsz in
  falsz

let cand v1 v2 = if v1 == cfalse || v2 == cfalse then cfalse else ctrue
let cor v1 v2 = if v1 == ctrue || v2 == ctrue then ctrue else cfalse

let cbool_of_bool v = if v == true then ctrue else cfalse
let bool_of_cbool v = if v true false then true else false
