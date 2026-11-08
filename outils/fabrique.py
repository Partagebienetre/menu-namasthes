# Fabrique index.html du menu en ligne de la pizzeria Namas'thés à partir de la carte (photo fournie par Agnès, 08/11/2026).
import html
E = html.escape

# (nom, ingrédients, prix enfant, prix M, prix XL, id)  — None = taille non proposée
SECTIONS = [
  ('classic', 'Classic', 'Classic pizza', 'Les incontournables', [
    ('Margherita', 'Base tomate, mozzarella, olive, feuille de basilic', 7.00, 11.00, 13.00),
    ('Reine', 'Base tomate, mozzarella, champignon, jambon, origan', 8.00, 12.00, 14.50),
  ]),
  ('cheesy', 'Cheesy', 'Cheesy pizza', 'Pour les amoureux du fromage', [
    ('Cheez', 'Base tomate, mozzarella, chèvre, gorgonzola, reblochon de Savoie, origan', 8.50, 12.50, 15.00),
    ('Savoyarde', 'Base crème, mozzarella, pomme de terre, reblochon de Savoie, oignon, lardons', 9.00, 13.00, 15.50),
    ('Raclette', 'Base crème, mozzarella, raclette, pomme de terre, jambon de pays', 10.00, 13.00, 16.00, 'saison'),
  ]),
  ('healthy', 'Healthy', 'Healthy pizza', 'Plus légères, toujours gourmandes', [
    ('Norvégienne', 'Base crème, mozzarella, pomme de terre, truite, aneth, citron vert', 10.00, 13.50, 16.50),
    ('Veggie', 'Base tomate, mozzarella, champignon, poivron, olive, origan', 9.00, 12.50, 15.00),
    ('Roco Rico', 'Base crème, mozzarella, champignon, poulet, cantal', 9.00, 13.00, 16.00),
  ]),
  ('original', 'Original', 'Original pizza', 'Sucré-salé', [
    ('Hawaïenne', 'Base tomate, mozzarella, ananas, poulet', 8.00, 12.00, 15.00),
    ('Chèvre miel', 'Base crème, mozzarella, chèvre, poulet, noisette, miel', 10.00, 13.50, 16.00),
  ]),
  ('gourmandes', 'Gourmandes', 'Les gourmandes', 'Les recettes de la maison', [
    ('Le Coup de cœur', 'Base tomate, mozzarella, viande hachée, scamorza fumée, oignon, olive, origan', 10.00, 13.50, 16.00),
    ('Chori’love', 'Base tomate, mozzarella, chorizo, oignon, poivron, origan', 10.00, 14.00, 16.00),
    ('La Coco', 'Base crème, mozzarella, scamorza fumée, olive, burrata, jambon de pays, basilic', None, 14.00, 17.00),
    ('La Pistakia', 'Base crème, mozzarella, pistache, jambon de pays, burrata, roquette, pesto', None, 14.00, 17.00),
    ('Sur mesure', 'Base tomate ou crème, mozzarella. Ingrédients au choix : voir les prix des suppléments', None, 10.00, 13.00, 'mesure'),
  ]),
  ('calzones', 'Calzones', 'Les calzones', 'La pizza pliée, taille M', [
    ('La Rossita', 'Base tomate, mozzarella, champignon, jambon, œuf', None, 10.50, None),
    ('La Dolce Crémita', 'Base crème, mozzarella, poulet, chèvre, miel', None, 10.50, None),
  ]),
]
SUPPLEMENTS = [('Fromage', 1.50), ('Burrata', 2.50), ('Aromate', 1.00), ('Œuf', 1.50), ('Viande', 2.00), ('Légume', 1.50)]
TAILLES = [('Enfant', '20 cm'), ('M', '27 cm'), ('XL', '34 cm')]

def prix(p): return ('%.2f' % p).replace('.', ',') + ' €'

def slug(s):
  import unicodedata, re
  s = unicodedata.normalize('NFD', s).encode('ascii', 'ignore').decode().lower()
  return re.sub(r'[^a-z0-9]+', '-', s).strip('-')

def pizza(sec, p):
  nom, ing, pe, pm, px = p[:5]; drap = p[5] if len(p) > 5 else ''
  did = sec + '-' + slug(nom)
  badge = ''
  if drap == 'saison': badge = '<span class="badge saison" data-saison>D’octobre à février</span>'
  cases = ''
  for (t, cm), v in zip(TAILLES, (pe, pm, px)):
    if v is None: continue
    cases += ('<button type="button" class="taille" data-nom="%s" data-taille="%s" data-cm="%s" data-prix="%.2f">'
              '<small>%s <i>%s</i></small><b>%s</b><span class="plus" aria-hidden="true">+</span><span class="qte" hidden></span></button>') % (E(nom), t, cm, v, t, cm, prix(v))
  return ('<article class="pizza" data-dish-id="%s"><div class="pizza-haut"><h3>%s</h3>%s'
          '<button class="voir-photo" type="button" hidden>Voir la photo</button></div>'
          '<p class="ing">%s</p><div class="prix">%s</div></article>') % (did, E(nom), badge, E(ing), cases)

nav = ''.join('<button class="nav-tab%s" type="button" data-sec="%s">%s</button>' % (' active' if i == 0 else '', s[0], E(s[1])) for i, s in enumerate(SECTIONS))
nav += '<button class="nav-tab" type="button" data-sec="supplements">Suppléments</button><button class="nav-tab" type="button" data-sec="infos">Infos &amp; contact</button>'

secs = ''
for i, (cle, court, titre, sous, items) in enumerate(SECTIONS):
  secs += '<section class="section%s" id="sec-%s"><div class="sec-header"><h2>%s</h2><p>%s</p></div>%s</section>' % (
    ' active' if i == 0 else '', cle, E(titre), E(sous), ''.join(pizza(cle, p) for p in items))

sup = ''.join('<li><span>%s</span><i></i><b>%s</b></li>' % (E(n), prix(v)) for n, v in SUPPLEMENTS)
secs += ('<section class="section" id="sec-supplements"><div class="sec-header"><h2>Extra topping</h2><p>À ajouter sur la pizza de votre choix</p></div>'
         '<ul class="supp">%s</ul><p class="note">La pizza « Sur mesure » se compose avec ces suppléments, à partir d’une base tomate ou crème et de la mozzarella.</p></section>') % sup

modele = open(__file__.replace('fabrique.py', 'modele.html'), encoding='utf-8').read()
out = modele.replace('{{NAV}}', nav).replace('{{SECTIONS}}', secs)
open(__file__.replace('outils/fabrique.py', 'index.html'), 'w', encoding='utf-8').write(out)
print('ok', len(out))
