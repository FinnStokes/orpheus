import random, string

def random_description(name, planet_type):
	patterns = {
		'$A$':['an atmosphere of $G$ and $G$',
                       'traces of $g$ in its atmosphere'],
		'$C$':['chilly','nippy','cold','fiery','freezing','frozen','icy','hot','aqueous','tellurian','beautiful','magical','enchanting','mountainous','rugged','scorching','temperate','verdant'],
		'$D$':['$N$ is a $T$. It has $A$, and a $S$.',
                       '$N$, a $T$ with $A$, has a $S$.',
                       '$N$ is a $T$. It has $A$, and a $S$.',
                       '$N$, a $T$ with $A$, has a $S$.',
		       'A $T$ with $A$, $N$ has a $S$.',
		       'A $T$ with a $S$, $N$ has $A$.'],
		'$Dd$':['$I$ is a $T$, with a $S$.',
		        'A $Wd$ $T$, $N$ has a $S$.',
                        '$I$, a $T$, sometimes has $A$. $N$\'s $Fp$.',
                        'A $T$, the $Wd$ $N$ has a $S$.',
                        'The $Wd$ world of $N$, a $Wd$ $T$, has a $S$.',
                        'The $Wd$ $N$ is a $T$. $N$\'s $Sp$.',
                        'The $C$ $T$ $N$\'s $Fp$.'],
		'$Dg$':['$I$ is a $T$. It has $A$. $I$ $F$.',
		        '$N$, a $Wg$ $T$, has $A$. $I$\'s $Fp$.',
                        'A $Wg$ $T$, $N$ has $A$.',
                        '$N$, a $Wg$ $T$, has $A$',
                        '$I$, a $Wg$ $T$, has $A$.',
                        '$I$ is a $T$ with $A$.'],
                '$F$':['has $Mo$'],
                '$Fp$':['$C$ $Mf$ was the inspiration for $Fa$ on board the Orpheus'],
                '$Fa$':['a painting','an opera','a poem','a poem','a painting','a painting','a poem','a song','a song','an assassination attempt on your father'],
                '$Mf$':['moon','moon','moon','moon','moon','third moon','second moon','second moon','second moon','third moon','moon','moon','second moon'],
                '$Mo$':['no moons','a single moon','a single moon','a single moon','a single moon','a single moon','one moon','one moon','one moon','one moon','one moon','two moons','two moons','two moons','two moons','many moons','many moons','a fuckload of moons. I mean, I thought Jupiter had  a lot of moons, but this shit is -- et excusez mon Francais sil-vous-plait -- ridiculous'],
		'$G$':['helium','hydrogen','oxygen','nitrogen','methane','chlorine','ammonia','carbon dioxide'],
		'$g$':['neon', 'argon', 'krypton', 'xenon', 'radon', 'flourine'],
		'$I$':['$N$','This planet','The planet $N$','This world','The world $N$'],
                '$i$':['the world of $N$','this world','$N$'],
		'$M$':['iron','zinc','copper','alumina','nickel','calcium carbonate','silica','silicon carbide','titanium carbide','graphite','methane','water','ice'],
		'$m$':['beryllium','magnesium','calcium','strontium','barium','radium','gold','platinum','silver','cadmium','titanium','uranium','tungsten'],
                '$Wd$':['frankly tiny','comically small','puny','practically invisible'],
                '$Wg$':['massive','humongous','ridiculously huge','gigantic'],
		'$S$':['$C$ surface that is composed mainly of $M$ and $M$',
			   'surface that is composed mainly of $M$ and $M$',
		       '$C$ surface that is mostly composed of $M$ with deposits of $m$',
		       'surface that is mostly composed of $M$ with deposits of $m$',
                       'surface that is almost entirely composed of $M$, with deposits of $m$ sprinkling its $C$ landscape'],
                '$Sp$':['$C$ surface is chiefly composed of $M$ and $M$',
                        'surface is chiefly composed of $M$ and $M$',
                        '$C$ surface is almost entirely $M$ with deposits of $m$',
                        'surface is almost entirely composed of $M$ with some deposits of $m$'],
	}
	desc = '$D$'
	if planet_type == 'dwarf planet':
		desc = '$Dd$'
	elif planet_type == 'gas giant':
		desc = '$Dg$'
	replaced = True
	while replaced:
		replaced = False
		for pattern,subs in patterns.iteritems():
			if pattern in desc:
				replaced = True
				new = random.choice(subs)
				patterns[pattern].remove(new)
				desc = string.replace(desc, pattern, new, 1)
	desc = string.replace(desc, '$N$', name)
	desc = string.replace(desc, '$T$', planet_type)
	return desc

if __name__ == '__main__':
        for i in xrange(0,3):
                print(random_description('Testington','terrestrial planet')+"\n")
                print(random_description('Testington','dwarf planet')+"\n")
                print(random_description('Testington','gas giant')+"\n")
