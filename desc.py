import random, string

def random_description(name, planet_type):
	patterns = {
		'$A$':['an atmosphere of $G$ and $G$',
		      'traces of $g$ in its atmosphere'],
		'$C$':['cold','fiery','freezing','hot','mountainous','rugged','scorching','temperate','verdant'],
		'$D$':['$I$ is a $T$. It has $A$, and a $S$.',
		       'A $T$ with $A$. $I$ has a $S$.',
		       'A $T$ with a $S$. $I$ has $A$.'],
		'$Dd$':['$I$ is a $T$, with a $S$.',
		        'A $T$. $I$ has a $S$.'],
		'$Dg$':['$I$ is a $T$. It has $A$.',
		        'A $T$. $I$ has $A$.',],
		'$G$':['helium','hydrogen','oxygen','nitrogen','methane','chlorine','ammonia','carbon dioxide'],
		'$g$':['neon', 'argon', 'krypton', 'xenon', 'radon', 'flourine'],
		'$I$':['$N$','This planet','The planet $N$','This world','The world $N$'],
		'$M$':['iron','zinc','copper','alumina','nickel','calcium carbonate','silica','silicon carbide','titanium carbide','graphite','methane','water','ice'],
		'$m$':['beryllium','magnesium','calcium','strontium','barium','radium','gold','platinum','silver','cadmium','titanium','uranium','tungsten'],
		'$S$':['$C$ surface that is composed mainly of $M$ and $M$',
			   'surface that is composed mainly of $M$ and $M$',
		       '$C$ surface that is mostly composed of $M$ with deposits of $m$',
		       'surface that is mostly composed of $M$ with deposits of $m$'],
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
