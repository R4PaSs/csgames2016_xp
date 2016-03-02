
# See https://fr.wikipedia.org/wiki/Nombre_de_Mersenne_premier

var i = 0
var n = 0
while n < 10 do
	var m = (2 ** i) - 1
	print "p={i} Mp={m}?"
	if m.is_prime then
		n += 1
		print "\tpremier! n={n}"
	end
	i += 1
end
