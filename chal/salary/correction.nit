var n = args.first.to_i
var b = 2
loop
	var r = n.to_base(b,true)
	if r == r.reversed then
		print "{n} => {r} en base {b}"
		return
	end
	b += 1
	assert b <= 36
end
