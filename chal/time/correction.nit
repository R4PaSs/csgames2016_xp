# nombre de secondes dans 12h
var mod = 60*60*12

var t
if args.length > 1 then
	# lit heures et minues
	t = args[0].to_i*60*60 + args[1].to_i*60 + (1000+2000.rand)*mod
	print "t = {t}"
else
	# lit le temps
	t = args.first.to_i
end


# on mesure les angres en `mod`-eme de circonference.
var h = t % (60*60*12)
var s = (h % (60*60)) * 12
var diff = (mod + h - s) % mod
diff = diff.min(mod-diff)

print "angles en mod: {h} et {s}: {diff}"
print "angles en dec: {h.to_f / mod.to_f * 360.0} {s.to_f / mod.to_f * 360.0}: {diff.to_f / mod.to_f * 360.0}"
