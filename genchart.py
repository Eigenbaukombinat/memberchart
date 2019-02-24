from gocept.collmex.collmex import Collmex

collmex = Collmex()

eintritte = {}
austritte = {}

LINE = '[new Date({y}, {m}, {d}), {total_ein}, {einmems}, {total_aus}, {ausmems}, {total}],'

for member in collmex.get_members():
    nr = member.get('Mitgliedsnummer')
    ein = member.get('Eintrittsdatum')
    aus = member.get('Austrittsdatum')
    if ein not in eintritte:
        eintritte[ein] = []
    eintritte[ein].append(nr)
    if aus is not None:
        if aus not in austritte:
            austritte[aus] = []
        austritte[aus].append(nr)


zeitpunkte = set(list(eintritte.keys()) + list(austritte.keys()))

total_ein = 0
total_aus = 0

datalines = []

for zp in sorted(zeitpunkte):
    einmems = eintritte.get(zp, [])
    ausmems = austritte.get(zp, [])
    total_ein += len(einmems)
    total_aus += len(ausmems)
    total = total_ein - total_aus
    y = int(zp[:4])
    m = int(zp[4:6]) - 1
    d = int(zp[6:8])
    einmems_str = ausmems_str = "undefined"
    if einmems:
        einmems_str = '"Ein: {}"'.format(len(einmems))
    if ausmems:
        ausmems_str = '"Aus: {}"'.format(len(ausmems))

    datalines.append(LINE.format(y=y, m=m, d=d, total_ein=total_ein,
        einmems=einmems_str, total=total, ausmems=ausmems_str,
        total_aus=total_aus))

with open('memberchart.html', 'w') as outfile:
    with open('index.html.in') as template:
        for line in template.readlines():
            if '##DATA##' in line:
                outfile.write('\n'.join(datalines))
            else:
                outfile.write(line)

