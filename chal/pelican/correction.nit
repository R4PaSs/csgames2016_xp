fun jouer: Int
do
	var d1 = 6.rand + 1
	var d2 = 6.rand + 1
	if d1 == d2 then return 2
	if d1 == 6 and d2 == 1 then return 2 + jouer + jouer + jouer
	if d2 == 6 and d1 == 1 then return 2 + jouer + jouer + jouer
	return 2 + jouer
end

var n = 0.0
var sum = 0.0
var m = 1.0
loop
	n += 1.0
	sum += jouer.to_f
	if n > m then
		print sum/n
		m *= 2.0
	end
end
