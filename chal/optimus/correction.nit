
# See https://fr.wikipedia.org/wiki/Nombre_de_Mersenne_premier

var i = 0
var n = 0
while n < 9 do # Sorry, we overflow at M10 :(
	var m = (2 ** i) - 1
	print "p={i} M_p={m}?"
	if m.is_prime then
		n += 1
		print "\tpremier! n={n}"
	end
	i += 1
end
