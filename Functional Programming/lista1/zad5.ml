let tabulate s ?(first = 0) last =
  List.init (last - first + 1) (fun x -> s x + first)
  