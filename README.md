## Semestralni-Prace
Demo 2D hry z vrchního pohledu, střílečka

# Úvod
Výsledkem mé semestrální je demo 2D hry, je to střílečka z vrchního pohledu. Cílem hráče je zabít nepřítele a přežít co nejdéle. Hráč může sbírat dva druhy itemů, životy a náboje.
Itemy a nepřátelé se spawnují na náhodných pozicích v určených intervlech. Interval spawnutí itemů je kratší než interval spawnutí nepřítele.
Nepřítele lze zabít pomocí střelby, nepřítel má určený počet životů a vydrží zásah 10 kulkami.
Nepřítel může hráče zranit, když se k němu přiblíží na určitou vzdálenost. Pokud počet životů hráče klesnou na nulu hra zkočí a hráč dostane možnost hrát znova nebo hru ukončit.
Hráčův progress ve hře zobrazuje počítadlo poražěných nepřátel v pravéh horním rohu.
Podobně i ukazatel hráčových životů a počtu munice je zobrazen v levém horním rohu.
Hráč může hru zastavit a v nastavení změnit velikost herního okna a hlasitosti hudby.

# Herní ovládání a logika
Hráč se pohybuje pomocí tlačítek klávesnice w,s,a,d. Míří pomocí myši a střílí levým tlačítkem nebo pomocí mezerníku.
Míření pomocí myši jsem udělal tak, že se pokaždé spočítá úhel mezi pozicí myši (minulé, a momentální) a pozicí hráče. Pomocí tohoto úhlu se obrázek hráče otočí na požadovanou pozici.

Logika pronásledování hráče nepřátelem je zpracovaná tak že se vezme pozice hráče a pozice nepřítele a ten se pak pohybuje po nejkratší možné trajektorii k hráči. 

Co bych rád dodělal/přidal
I přesto že hra má možnost změny hlasitosti hudby, hra hudbu ještě nemá. Proto bych rád přidal hudbu, která bude hrát během hry a druhou jinou která bude hrát když bude hra pozastavena. Dále mám zvuk výstřelů, který bych se dal do hry přidat také.

Logika nepřítele je velmi nedokonalá, chtělo by ji zlepšit tak, aby nepřítel předpovídal pohyb hráče a pohyboval se směrek k pozici na které hráč teprve bude. Tímto by měl větší šanci hráče dohnat a zranit.

Dále by se dalo přidat více druhů nepřátel, více druhů nových itemů.
Příklady nových nepřatel: nepřítel se z braní co by po hráči střílel, nepřítel co by při kontaktu s hráčem vybuchl.
Příklady nových itemů: vylepšení (vetší demage co hráč způsobuje, vetší rychlost pohybu, vetší vzdálenost dostřelu), nové zbraně např. granáty

Hra by šla rozšířit o levely, a možností vylepšení zbraní a hráčových schopností nebo o různé druhy obtížnosti hry.

# Obsah souborů
Demo obsahuje/používá 3 soubory s kodem a 26 obrázků
V souboru *images/player/player_animations* jsou obrázky pro animaci hráče. Tyto obrázky nevyužívám, ale lze je v budoucnu použít pro vylepšení hry
Podobně v souboru *background* jsou obrázky *background_x* x = 1 - 8, jedná se o obrázky různých pozadí, lze je využít podobně
V souboru *menu* je obrázek *button_generic* jedná se o defaultní obrázek ze kterého jsem vytvořil obrázky ostatních tlačítek, lze ho využít pro budoucí tvorbu dalších tlačítek

