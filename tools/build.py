"""Generates the inner pages (EN + ES) and the shared header/footer of the home pages.

Run from the repo root:  python tools/build.py
"""
import html
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://fedianin.github.io/pro-clean-redesign/"
LIVE = "https://pro-clean.es/"
WA = "https://wa.me/34621383059"
MAPS = "https://goo.gl/maps/PLRhvR6mAkvvk3kt6"
E = html.escape

TOWNS = ["Málaga", "Torremolinos", "Benalmádena", "Fuengirola", "Marbella", "Estepona", "Benahavís",
         "San Pedro de Alcántara", "Antequera", "Torre del Mar", "Cártama", "Alhaurín de la Torre",
         "Vélez-Málaga", "Nerja"]

UI = {
    "en": dict(
        skip="Skip to content", home="Home", services="Services", gallery="Gallery", reviews="Reviews",
        about="About", contact="Contact", quote="Get a quote", quote_l="Get a free quote",
        other="Ver en español", other_short="ES", other_lang="es", other_aria="Ver en español",
        menu="Open menu", privacy="Privacy policy", cookies="Cookie policy", other_footer="Versión en español",
        footer_desc="Upholstery, mattress and carpet cleaning. 29620 Torremolinos, Málaga, Spain.",
        copy="This site uses no tracking cookies.", wa_aria="Chat on WhatsApp",
        areas_eyebrow="Where we work", areas_h="Across the Costa del Sol",
        areas_p="Based in Torremolinos, we travel along the coast and inland. Not on the list? Message us and we will find a solution.",
        map_alt="Map of the Costa del Sol showing the area we cover",
        cta_h="Ready for a fresh sofa?", cta_p="Send us your list and get a quote on WhatsApp today.",
        wa_btn="Message us on WhatsApp", more="Learn more", why="Why it matters", results="Real results",
        results_h="From our recent jobs", other_services="Other services", crumbs="Breadcrumb",
        ba_note="Before on the left, after on the right.",
    ),
    "es": dict(
        skip="Saltar al contenido", home="Inicio", services="Servicios", gallery="Galería", reviews="Reseñas",
        about="Nosotros", contact="Contacto", quote="Presupuesto", quote_l="Pedir presupuesto gratis",
        other="View in English", other_short="EN", other_lang="en", other_aria="View in English",
        menu="Abrir menú", privacy="Política de privacidad", cookies="Política de cookies", other_footer="English version",
        footer_desc="Limpieza de tapicerías, colchones y alfombras. 29620 Torremolinos, Málaga, España.",
        copy="Esta web no usa cookies de seguimiento.", wa_aria="Escríbenos por WhatsApp",
        areas_eyebrow="Dónde trabajamos", areas_h="En toda la Costa del Sol",
        areas_p="Desde Torremolinos nos desplazamos por la costa y el interior. ¿Tu localidad no aparece? Escríbenos y buscaremos una solución.",
        map_alt="Mapa de la Costa del Sol con la zona en la que trabajamos",
        cta_h="¿Listo para un sofá como nuevo?", cta_p="Envíanos tu lista y recibe el presupuesto por WhatsApp hoy mismo.",
        wa_btn="Escríbenos por WhatsApp", more="Ver más", why="Por qué es importante", results="Resultados reales",
        results_h="De nuestros últimos trabajos", other_services="Otros servicios", crumbs="Ruta de navegación",
        ba_note="Antes a la izquierda, después a la derecha.",
    ),
}

NAV = ["services", "gallery", "reviews", "about", "contact"]

# ---------------------------------------------------------------- services
SERVICES = [
    dict(slug="sofa-cleaning", icon="couch", img="sofa.jpg",
         photos=[("sofa.jpg", "sofa"), ("leather.jpg", "leather"), ("work/leather-2.jpg", "leather"), ("sofa-ba.jpg", "sofa"),
                 ("gallery/g12.jpg", "sofa"), ("work/sofa-1.jpg", "sofa"), ("work/sofa-2.jpg", "sofa"), ("work/sofa-3.jpg", "sofa"),
                 ("work/sofa-4.jpg", "sofa"), ("work/sofa-5.jpg", "sofa")],
         en=dict(name="Sofa cleaning", card="Fabric and leather sofas cleaned deep inside the fibres, at your home.",
                 h1="Sofa cleaning <br>at your home",
                 lead="Fabric and leather sofas cleaned with professional extraction equipment. We remove dust, stains, allergens and odours from inside the cushions, not just the surface.",
                 desc="Fabric and leather sofa cleaning at your home on the Costa del Sol. Stains, allergens and odours removed. Free quote on WhatsApp.",
                 points=[("Hygiene and fewer allergens", "Deep cleaning removes the dirt, dust and allergens that build up in a sofa over time, so the air at home is cleaner."),
                         ("A longer life for your sofa", "Removing grit and surface stains protects the fabric from early wear, so your sofa stays in good shape for years."),
                         ("A sofa that looks fresh again", "Stains, discolouration and marks disappear and the colour comes back."),
                         ("No more lingering odours", "Pets, food and everyday use leave smells in the fabric. Cleaning takes them out instead of covering them."),
                         ("Fabric and leather", "We clean both, using the right method for each material so leather stays soft and fabric stays intact."),
                         ("Peace of mind", "A clean sofa means a clean, comfortable place for your family to relax.")]),
         es=dict(name="Limpieza de sofás", card="Sofás de tela y piel limpios hasta el fondo del tejido, en tu casa.",
                 h1="Limpieza de sofás <br>a domicilio",
                 lead="Limpiamos sofás de tela y piel con maquinaria profesional de extracción. Eliminamos polvo, manchas, alérgenos y olores del interior de los cojines, no solo de la superficie.",
                 desc="Limpieza de sofás de tela y piel a domicilio en la Costa del Sol. Eliminamos manchas, alérgenos y olores. Presupuesto gratis por WhatsApp.",
                 points=[("Higiene y menos alérgenos", "La limpieza profunda elimina la suciedad, el polvo y los alérgenos que se acumulan en el sofá, y el aire de casa queda más limpio."),
                         ("Más vida para tu sofá", "Quitar la arenilla y las manchas protege el tejido del desgaste y el sofá aguanta en buen estado muchos años."),
                         ("Un sofá que vuelve a verse nuevo", "Desaparecen manchas, decoloraciones y marcas, y vuelve el color."),
                         ("Adiós a los malos olores", "Mascotas, comida y el uso diario dejan olor en el tejido. La limpieza lo elimina en lugar de taparlo."),
                         ("Tela y piel", "Limpiamos los dos con el método adecuado para cada material, para que la piel quede suave y la tela intacta."),
                         ("Tranquilidad", "Un sofá limpio es un lugar limpio y cómodo para que tu familia descanse.")])),
    dict(slug="mattress-cleaning", icon="bed", img="mattress-ba.jpg",
         photos=[("mattress-ba.jpg", "mattress"), ("work/mattress-3.jpg", "mattress"), ("work/mattress-1.jpg", "mattress"),
                 ("work/mattress-2.jpg", "mattress")],
         en=dict(name="Mattress cleaning", card="Sweat marks, yellow stains and dust mites removed for a fresh bed.",
                 h1="Mattress cleaning <br>for a fresher sleep",
                 lead="We remove sweat marks, yellow stains, dust mites and allergens from your mattress at your home, so you sleep on a clean, fresh surface again.",
                 desc="Mattress cleaning at your home on the Costa del Sol. Dust mites, stains and odours removed. Free quote on WhatsApp.",
                 points=[("Dust mites and allergens out", "Regular cleaning removes the dust mites, allergens and debris that disturb sleep and trigger allergies."),
                         ("Better sleep", "Without dirt, stains and odours your bed is more inviting and easier to relax in."),
                         ("Early warning for bed bugs", "A professional clean makes it easier to spot early signs of bed bugs and deal with them quickly."),
                         ("A longer mattress life", "Removing sweat, oils and dirt prevents early wear, so your mattress keeps its comfort and support."),
                         ("Better for allergies", "Especially important for anyone with allergies or breathing problems, because a clean mattress has fewer triggers."),
                         ("Better wellbeing", "Good sleep on a clean mattress helps your mood, your energy and your health.")]),
         es=dict(name="Limpieza de colchones", card="Quitamos marcas de sudor, manchas amarillas y ácaros para una cama limpia.",
                 h1="Limpieza de colchones <br>para dormir mejor",
                 lead="Eliminamos marcas de sudor, manchas amarillas, ácaros y alérgenos de tu colchón en tu casa, para que vuelvas a dormir sobre una superficie limpia.",
                 desc="Limpieza de colchones a domicilio en la Costa del Sol. Eliminamos ácaros, manchas y olores. Presupuesto gratis por WhatsApp.",
                 points=[("Sin ácaros ni alérgenos", "La limpieza periódica elimina ácaros, alérgenos y restos que alteran el sueño y provocan alergias."),
                         ("Duermes mejor", "Sin suciedad, manchas ni olores, la cama resulta más agradable y descansas mejor."),
                         ("Detección temprana de chinches", "Una limpieza profesional ayuda a detectar a tiempo señales de chinches y actuar rápido."),
                         ("Más vida para el colchón", "Quitar sudor, grasa y suciedad evita el desgaste y el colchón mantiene su confort."),
                         ("Mejor para las alergias", "Muy importante para personas con alergias o problemas respiratorios, porque un colchón limpio tiene menos desencadenantes."),
                         ("Más bienestar", "Dormir bien en un colchón limpio mejora el ánimo, la energía y la salud.")])),
    dict(slug="carpet-cleaning", icon="square-half-bottom", img="carpet-ba.jpg",
         photos=[("carpet-ba.jpg", "carpet"), ("work/carpet-ba-2.jpg", "carpet"), ("carpet.jpg", "carpet"),
                 ("work/carpet-1.jpg", "carpet"), ("work/carpet-2.jpg", "carpet"), ("work/carpet-3.jpg", "carpet"),
                 ("work/carpet-4.jpg", "carpet"), ("work/carpet-5.jpg", "carpet"), ("work/carpet-6.jpg", "carpet"),
                 ("work/carpet-7.jpg", "carpet")],
         video=[("clip-1.mp4", "work/video-poster.jpg"), ("clip-2.mp4", "work/video-poster.jpg")],
         en=dict(name="Carpet cleaning", card="Rugs and carpets deep cleaned so the pile is soft and fresh again.",
                 h1="Carpet and rug <br>cleaning at home",
                 lead="Deep extraction cleaning for carpets and rugs of every kind, from shaggy rugs to classic Persian style. We lift stains and odours and bring back the original colour.",
                 desc="Carpet and rug cleaning at your home on the Costa del Sol. Stains and odours removed, colour restored. Free quote on WhatsApp.",
                 points=[("Cleaner indoor air", "Carpet cleaning removes dust, allergens and pollutants that would otherwise stay in the air you breathe."),
                         ("Stains and odours removed", "Stubborn stains and unpleasant smells come out, leaving your carpets fresh."),
                         ("A longer carpet life", "Removing the grit that wears down the fibres keeps carpets looking and feeling new for longer."),
                         ("Colour and texture restored", "A deep clean brings back the original colour and texture of the pile."),
                         ("Safer for children and pets", "Fewer allergens and pollutants make the floor a healthier place to play."),
                         ("No damp or mould", "Carpets that are not cleaned can trap moisture. Regular cleaning keeps mould and mildew away.")]),
         es=dict(name="Limpieza de alfombras", card="Alfombras y moquetas limpias a fondo, con el pelo suave otra vez.",
                 h1="Limpieza de alfombras <br>y moquetas a domicilio",
                 lead="Limpieza profunda por extracción para todo tipo de alfombras y moquetas, de pelo largo o de estilo persa. Quitamos manchas y olores y recuperamos el color original.",
                 desc="Limpieza de alfombras y moquetas a domicilio en la Costa del Sol. Eliminamos manchas y olores y recuperamos el color. Presupuesto gratis por WhatsApp.",
                 points=[("Aire más limpio", "La limpieza elimina polvo, alérgenos y contaminantes que de otro modo se quedan en el aire que respiras."),
                         ("Sin manchas ni olores", "Las manchas difíciles y los malos olores desaparecen y la alfombra queda fresca."),
                         ("Más vida para la alfombra", "Quitar la arenilla que desgasta las fibras mantiene la alfombra como nueva más tiempo."),
                         ("Color y textura recuperados", "Una limpieza profunda devuelve el color y la textura originales."),
                         ("Más seguro para niños y mascotas", "Menos alérgenos y contaminantes hacen del suelo un lugar más sano para jugar."),
                         ("Sin humedad ni moho", "Las alfombras sin limpiar retienen humedad. La limpieza periódica evita el moho.")])),
    dict(slug="chair-cleaning", icon="chair", img="chair.jpg",
         photos=[("chair.jpg", "chair"), ("work/chairs-1.jpg", "chair"), ("work/chair-1.jpg", "chair"),
                 ("work/chair-2.jpg", "chair"), ("work/chair-3.jpg", "chair")],
         en=dict(name="Chair cleaning", card="Dining chairs, armchairs and office chairs cleaned on site.",
                 h1="Chair cleaning <br>for homes and offices",
                 lead="Dining chairs, armchairs and office chairs cleaned where they stand. Ideal before guests arrive or between holiday rental stays.",
                 desc="Chair and armchair cleaning at your home or office on the Costa del Sol. Free quote on WhatsApp.",
                 points=[("Hygiene and health", "Cleaning removes bacteria, allergens and germs from the seats you use every day."),
                         ("A longer chair life", "Dust, dirt and stains wear the fabric down. Regular cleaning keeps chairs in good shape."),
                         ("A better looking room", "Clean chairs make a dining room, office or living room look neat and cared for."),
                         ("Fresh, not stale", "Chairs absorb smells from food, pets and use. Cleaning takes them out."),
                         ("A good impression on guests", "Clean seating shows attention to detail, at home or in a holiday rental."),
                         ("Peace of mind", "You know your space is hygienic and well kept.")]),
         es=dict(name="Limpieza de sillas", card="Sillas de comedor, sillones y sillas de oficina limpios in situ.",
                 h1="Limpieza de sillas <br>en casa y oficina",
                 lead="Limpiamos sillas de comedor, sillones y sillas de oficina donde están. Perfecto antes de recibir invitados o entre huéspedes de un alquiler vacacional.",
                 desc="Limpieza de sillas y sillones en tu casa u oficina en la Costa del Sol. Presupuesto gratis por WhatsApp.",
                 points=[("Higiene y salud", "La limpieza elimina bacterias, alérgenos y gérmenes de los asientos que usas a diario."),
                         ("Más vida para las sillas", "El polvo, la suciedad y las manchas desgastan el tejido. La limpieza las mantiene en buen estado."),
                         ("Un espacio más bonito", "Unas sillas limpias hacen que el comedor, la oficina o el salón se vean cuidados."),
                         ("Frescas, sin olores", "Las sillas absorben olores de comida, mascotas y uso. La limpieza los elimina."),
                         ("Buena impresión a tus invitados", "Los asientos limpios demuestran atención al detalle, en casa o en un alquiler vacacional."),
                         ("Tranquilidad", "Sabes que tu espacio está limpio y bien cuidado.")])),
    dict(slug="yacht-furniture-cleaning", icon="anchor", img="work/yacht-3.jpg",
         photos=[("work/yacht-1.jpg", "yacht"), ("work/yacht-2.jpg", "yacht"), ("work/yacht-4.jpg", "yacht"),
                 ("work/yacht-5.jpg", "yacht"), ("work/yacht-6.jpg", "yacht"), ("work/yacht-7.jpg", "yacht")],
         video=[("yacht.mp4", "work/yacht-2.jpg")],
         en=dict(name="Yacht furniture cleaning", card="Fabric and leather seating on board, cleaned to protect your yacht.",
                 h1="Yacht furniture <br>cleaning",
                 lead="We clean fabric and leather furniture on board, from saloon sofas to deck cushions. A practical way to protect the comfort, look and value of your yacht.",
                 desc="Fabric and leather yacht furniture cleaning on the Costa del Sol. Free quote on WhatsApp.",
                 points=[("Fabric and leather", "One team for every type of upholstery on board, each cleaned with the right method."),
                         ("Protect your investment", "Well kept furniture helps maintain the value of your yacht."),
                         ("Comfort for everyone on board", "Clean seating is healthier and more pleasant for owners, guests and crew."),
                         ("A yacht that looks its best", "Stains and marks removed so the interior looks ready for the season.")]),
         es=dict(name="Limpieza de tapicería de yates", card="Asientos de tela y piel a bordo, limpios para proteger tu yate.",
                 h1="Limpieza de tapicería <br>de yates",
                 lead="Limpiamos muebles de tela y piel a bordo, desde los sofás del salón hasta los cojines de cubierta. Una forma práctica de proteger el confort, el aspecto y el valor de tu yate.",
                 desc="Limpieza de tapicería de tela y piel en yates de la Costa del Sol. Presupuesto gratis por WhatsApp.",
                 points=[("Tela y piel", "Un solo equipo para toda la tapicería a bordo, con el método adecuado para cada material."),
                         ("Protege tu inversión", "Unos muebles cuidados ayudan a mantener el valor de tu yate."),
                         ("Confort para todos a bordo", "Los asientos limpios son más sanos y agradables para propietarios, invitados y tripulación."),
                         ("Un yate siempre impecable", "Eliminamos manchas y marcas para que el interior esté listo para la temporada.")])),
    dict(slug="wardrobe-organisation-service", icon="t-shirt", img="work/wardrobe.jpg", wide=True, photos=[],
         en=dict(name="Wardrobe organisation", card="We empty, sort, clean and arrange your wardrobe in one visit.",
                 h1="Wardrobe organisation <br>at your home",
                 lead="We come to your villa or apartment, sort through everything with you and leave your wardrobe clean, calm and easy to use every day.",
                 desc="Wardrobe decluttering and organisation at your home on the Costa del Sol. One visit of 3 to 5 hours. Free quote on WhatsApp.",
                 points=[("Emptied, sorted and restored in one visit", "Every item comes out, gets assessed and goes back in a logical order."),
                         ("Keep, donate or discard", "We go through each item with you and ask the right questions so decisions feel easy."),
                         ("Organised by type, season or colour", "Tops, bottoms, dresses, outerwear, shoes and accessories each get their place."),
                         ("Shelves cleaned before restocking", "Dust removed and the interior freshened before anything goes back."),
                         ("Storage advice included", "Everyday items at eye level, seasonal items stored away."),
                         ("English speaking team", "Clear communication with villa owners and expats across the Costa del Sol.")],
                 steps=[("Book a time slot", "WhatsApp us for a free quote and a date. We allocate 3 to 5 hours depending on the wardrobe size."),
                        ("Empty everything out", "Every item comes out so we start with a clean slate."),
                        ("Sort and decide", "Keep, donate or discard, item by item, together with you."),
                        ("Categorise by type", "Each group is placed logically for daily use."),
                        ("Clean the interior", "Shelves wiped down and dust removed before restocking."),
                        ("Restore and arrange", "Frequent items within reach, seasonal items stored away.")]),
         es=dict(name="Organización de armarios", card="Vaciamos, ordenamos, limpiamos y colocamos tu armario en una visita.",
                 h1="Organización de armarios <br>a domicilio",
                 lead="Vamos a tu villa o piso, revisamos todo contigo y dejamos tu armario limpio, ordenado y fácil de usar cada día.",
                 desc="Orden y organización de armarios a domicilio en la Costa del Sol. Una visita de 3 a 5 horas. Presupuesto gratis por WhatsApp.",
                 points=[("Vaciado, ordenado y colocado en una visita", "Sacamos cada prenda, la revisamos y la colocamos en un orden lógico."),
                         ("Guardar, donar o desechar", "Revisamos cada prenda contigo y te ayudamos a decidir sin esfuerzo."),
                         ("Por tipo, temporada o color", "Camisetas, pantalones, vestidos, abrigos, zapatos y complementos, cada uno en su sitio."),
                         ("Baldas limpias antes de colocar", "Quitamos el polvo y refrescamos el interior antes de guardar nada."),
                         ("Consejos de almacenaje incluidos", "Lo de diario a la altura de los ojos, lo de temporada guardado."),
                         ("Equipo que habla inglés", "Comunicación clara con propietarios de villas y residentes extranjeros.")],
                 steps=[("Reserva una cita", "Escríbenos por WhatsApp para el presupuesto y la fecha. Reservamos de 3 a 5 horas según el tamaño del armario."),
                        ("Vaciamos todo", "Sacamos cada prenda para empezar de cero."),
                        ("Ordenamos y decidimos", "Guardar, donar o desechar, prenda a prenda, contigo."),
                        ("Clasificamos por tipo", "Cada grupo se coloca de forma lógica para el día a día."),
                        ("Limpiamos el interior", "Baldas limpias y sin polvo antes de volver a guardar."),
                        ("Colocamos y organizamos", "Lo que más usas a mano, lo de temporada guardado.")])),
]

# ---------------------------------------------------------------- reviews
GOOGLE = [
    ("Stephen Brooks Brown", "en", "Really brilliant service today from the two hardworking ladies at Pro Clean Oleksandra and Olesia. After 6 months in storage not only did some of our furniture smell bad but was also dirty thanks to be stored next to agricultural land. We were almost ready to throw the furniture in the bin!! But these two professionals restored the upholstery to an almost new condition. To say we are over the moon with the results is an understatement. Also the communication is absolutely fantastic, Oleksandra even sent a live location link so you knew exactly how close to arrival they were. Thoroughly recommend!"),
    ("Aqua de Mar", "en", "Extremely satisfied! The sofa was cleaned quickly, thoroughly, and with great attention to detail. The girl who did the job, Aleksandra, is very kind and works conscientiously and responsibly. Nothing but praise for her and I highly recommend the service. 😊"),
    ("Kimberly Cortus", "nl", "Perfect, vlekken zijn uit de vloerbedekking, vloerbedekking is ook weer fluffy en het ruikt super lekker!"),
    ("Monika Velartová", "en", "Reliable and skilled young lady. Our sofa looks like new after the cleaning. I highly recommend her."),
    ("Аня Мастерова", "ru", "Работа выполнена просто великолепно! Моему дивану подарили вторую жизнь, хотя я думала, что ему давно пора на мусорку 🥹 спасибо большое за ваш труд, я довольна на все 1000% 🙏🏽"),
    ("Yemilia Aranguez", "es", "Muy buen trabajo!"),
    ("Elena Rincon Rodriguez", "es", "Muy eficientes. Dejaron los sofás como nuevos. Muy recomendable"),
    ("Claudia Cazalla Calderón", "es", "Ha sido fácil acordar una cita. Son puntuales y eficientes. Ha sido una buena experiencia, estoy contenta! Los recomiendo."),
]
SITE_REVIEWS = [
    ("Excelente servicio", "28/10/2025", "es", "Muy buen servicio y rápido atendimiento, se recomienda.", "Javi Muller"),
    ("Very happy with result", "24/07/2025", "en", "We got sofa and rugs cleaned. We are very happy with the result.", "Elisabeth Berneblad"),
    ("Sofá clean", "09/05/2025", "en", "Fantastic results, sofá came out great! Looks brand new again!", "Elena"),
    ("Muy profesionales", "02/02/2025", "es", "Resultados excelentes. Son rápidos y muy profesionales. El trato con el cliente es inmejorable.", "Isabel"),
    ("Excellent service", "10/01/2025", "en", "Highly professional service and would recommend them.", "David Ames"),
    ("Melanie", "09/07/2024", "en", "Yet again the best sofa & carpet cleaners, we now use on a regular basis & would not choose anyone else, service is exceptional! 🤩", "Melanie"),
    ("House cleaning", "25/05/2024", "en", "Fantastic team. They cleaned my entire house making everything sparkle and got the pet smells out of my rugs and sofas. Brilliant service", "Daran Little"),
    ("Total professionalism", "14/10/2023", "en", "From the quote to completion, pro-clean lived up to its claims: very efficient, thorough and professional. I'm delighted", "Josephine Melville"),
    ("Cleaning in Sotogrande", "26/08/2023", "en", "Extremely friendly and efficient service. Very happy with the cleaning of mattress, headboard and rugs.", "Sarah Rebeiro"),
    ("Excelente", "12/08/2023", "es", "Todo perfecto. Muy buena limpieza, rápida y práctica. Recomiendo totalmente!!!", "Luciano"),
]

# ---------------------------------------------------------------- gallery
GALLERY = [
    ("sofa.jpg", "sofa", True), ("mattress-ba.jpg", "mattress", True), ("carpet-ba.jpg", "carpet", True),
    ("work/carpet-ba-2.jpg", "carpet", True), ("chair.jpg", "chair", True), ("sofa-ba.jpg", "sofa", True),
    ("gallery/g12.jpg", "sofa", True), ("leather.jpg", "leather", True), ("work/leather-2.jpg", "leather", True),
    ("work/yacht-3.jpg", "yacht", False), ("work/yacht-1.jpg", "yacht", False), ("work/yacht-4.jpg", "yacht", False),
    ("work/yacht-2.jpg", "yacht", False), ("work/yacht-5.jpg", "yacht", False), ("work/yacht-6.jpg", "yacht", False),
    ("work/yacht-7.jpg", "yacht", False),
    ("work/carpet-6.jpg", "carpet", False), ("work/carpet-7.jpg", "carpet", False), ("work/carpet-5.jpg", "carpet", False),
    ("work/carpet-3.jpg", "carpet", False), ("work/carpet-4.jpg", "carpet", False), ("work/carpet-1.jpg", "carpet", False),
    ("work/carpet-2.jpg", "carpet", False), ("carpet.jpg", "carpet", False),
    ("work/sofa-1.jpg", "sofa", False), ("work/sofa-2.jpg", "sofa", False), ("work/sofa-3.jpg", "sofa", False),
    ("work/sofa-4.jpg", "sofa", False), ("work/sofa-5.jpg", "sofa", False),
    ("work/mattress-3.jpg", "mattress", False), ("work/mattress-1.jpg", "mattress", False), ("work/mattress-2.jpg", "mattress", False),
    ("work/chairs-1.jpg", "chair", False), ("work/chair-1.jpg", "chair", False), ("work/chair-2.jpg", "chair", False),
    ("work/chair-3.jpg", "chair", False), ("work/wardrobe.jpg", "wardrobe", False),
]
VIDEOS = [("yacht.mp4", "work/yacht-2.jpg", "yacht"), ("clip-1.mp4", "work/video-poster.jpg", "carpet"),
          ("clip-2.mp4", "work/video-poster.jpg", "carpet")]
CAT = {
    "en": dict(sofa="Fabric sofa", leather="Leather sofa", mattress="Mattress", carpet="Carpet and rug", chair="Chair and armchair",
               yacht="Yacht furniture", wardrobe="Wardrobe", video="Videos",
               ba="before and after cleaning", work="during cleaning", vid="Video of"),
    "es": dict(sofa="Sofá de tela", leather="Sofá de piel", mattress="Colchón", carpet="Alfombra", chair="Silla y sillón",
               yacht="Tapicería de yate", wardrobe="Armario", video="Vídeos",
               ba="antes y después de la limpieza", work="durante la limpieza", vid="Vídeo:"),
}

# ---------------------------------------------------------------- page text
PAGES = {
    "services": dict(
        en=dict(title="Cleaning services on the Costa del Sol | Pro Clean", desc="Sofa, mattress, carpet, chair and yacht furniture cleaning plus wardrobe organisation across the Costa del Sol.",
                eyebrow="Our services", h1="Everything soft in your home, <br>cleaned by one team",
                lead="Pick a service to see what we do and why it matters. Every job is done at your home with professional extraction equipment."),
        es=dict(title="Servicios de limpieza en la Costa del Sol | Pro Clean", desc="Limpieza de sofás, colchones, alfombras, sillas y tapicería de yates, además de organización de armarios en la Costa del Sol.",
                eyebrow="Nuestros servicios", h1="Todos los textiles de tu casa, <br>en manos de un solo equipo",
                lead="Elige un servicio para ver qué hacemos y por qué importa. Todos los trabajos se hacen en tu casa con maquinaria profesional de extracción.")),
    "gallery": dict(
        en=dict(title="Before and after gallery | Pro Clean", desc="Real before and after photos of sofa, mattress, carpet and chair cleaning on the Costa del Sol.",
                eyebrow="Gallery", h1="Before and after, <br>from real homes",
                lead="Every photo is from a client home on the Costa del Sol. No filters and no stock images.", all="All"),
        es=dict(title="Galería de antes y después | Pro Clean", desc="Fotos reales de antes y después de limpieza de sofás, colchones, alfombras y sillas en la Costa del Sol.",
                eyebrow="Galería", h1="Antes y después, <br>en casas reales",
                lead="Todas las fotos son de casas de clientes en la Costa del Sol. Sin filtros y sin imágenes de archivo.", all="Todo")),
    "reviews": dict(
        en=dict(title="Client reviews | Pro Clean", desc="Read what clients say about Pro Clean. Rated Excellent from 85 Google reviews.",
                eyebrow="Reviews", h1="What our clients say",
                lead="Your opinion helps us get better. Here is what clients across the Costa del Sol wrote about us, in their own words and language.",
                g_h="Google reviews", g_sum="Rated <strong>Excellent</strong> from 85 reviews",
                s_h="Reviews on our site", s_sum="<strong>5.0</strong> out of 5 from 28 reviews",
                write="Leave a review on Google", posted="Google review"),
        es=dict(title="Reseñas de clientes | Pro Clean", desc="Lee lo que dicen los clientes de Pro Clean. Valoración Excelente con 85 reseñas en Google.",
                eyebrow="Reseñas", h1="Lo que dicen nuestros clientes",
                lead="Tu opinión nos ayuda a mejorar. Esto es lo que han escrito clientes de toda la Costa del Sol, con sus palabras y en su idioma.",
                g_h="Reseñas en Google", g_sum="Valoración <strong>Excelente</strong> con 85 reseñas",
                s_h="Reseñas en nuestra web", s_sum="<strong>5,0</strong> de 5 con 28 reseñas",
                write="Deja tu reseña en Google", posted="Reseña de Google")),
    "about": dict(
        en=dict(title="About us | Pro Clean", desc="Pro Clean is a locally owned family cleaning business from Torremolinos serving the Costa del Sol.",
                eyebrow="About us", h1="A local family business <br>that cares about results",
                lead="At Pro Clean we are passionate about high quality cleaning. We are locally owned and operated, and proud to serve the Costa del Sol community.",
                body=["We believe in transparency and honesty in everything we do. We keep our pricing competitive and make the whole experience easy, from the first message to the final result.",
                      "We are committed to the highest level of customer service and we go the extra mile to make sure every client is happy with the result.",
                      "Looking for a reliable, professional cleaning company? Message us to book your cleaning and see the difference a professional clean makes."],
                values=[("ph-hand-heart", "Family run", "Locally owned and personally managed from Torremolinos."),
                        ("ph-eye", "Transparent", "Clear quotes in writing and honest advice about what is possible."),
                        ("ph-tag", "Fair pricing", "Competitive prices with automatic discounts on larger jobs."),
                        ("ph-smiley", "Easy from start to finish", "Quote, booking and updates all on WhatsApp or email.")],
                services_h="What we clean"),
        es=dict(title="Sobre nosotros | Pro Clean", desc="Pro Clean es una empresa familiar de limpieza de Torremolinos que trabaja en toda la Costa del Sol.",
                eyebrow="Sobre nosotros", h1="Una empresa familiar <br>que cuida cada resultado",
                lead="En Pro Clean nos apasiona la limpieza de calidad. Somos una empresa local con trato familiar y estamos orgullosos de servir a la Costa del Sol.",
                body=["Creemos en la transparencia y la honestidad en todo lo que hacemos. Mantenemos precios competitivos y hacemos que todo sea sencillo, desde el primer mensaje hasta el resultado final.",
                      "Nos comprometemos con el mejor servicio al cliente y hacemos todo lo posible para que cada cliente quede satisfecho con el resultado.",
                      "¿Buscas una empresa de limpieza fiable y profesional? Escríbenos para reservar tu limpieza y comprueba la diferencia de una limpieza profesional."],
                values=[("ph-hand-heart", "Empresa familiar", "De propiedad local y gestionada personalmente desde Torremolinos."),
                        ("ph-eye", "Transparencia", "Presupuestos claros por escrito y consejos honestos sobre lo que se puede conseguir."),
                        ("ph-tag", "Precios justos", "Precios competitivos con descuentos automáticos en pedidos grandes."),
                        ("ph-smiley", "Fácil de principio a fin", "Presupuesto, reserva y avisos por WhatsApp o email.")],
                services_h="Qué limpiamos")),
    "contact": dict(
        en=dict(title="Contact us | Pro Clean", desc="Contact Pro Clean on WhatsApp +34 621 383 059 or office@pro-clean.es. Based in Torremolinos, serving the Costa del Sol.",
                eyebrow="Contact us", h1="Questions about <br>cleaning services?",
                lead="To avoid interruptions while we work in a client home, we use WhatsApp and email. We reply as soon as we finish the job in progress.",
                wa="WhatsApp", email="Email", loc="Location", loc_v="29620 Torremolinos, Málaga, Spain", follow="Follow our work",
                maps="Open in Google Maps"),
        es=dict(title="Contacto | Pro Clean", desc="Contacta con Pro Clean por WhatsApp +34 621 383 059 o en office@pro-clean.es. En Torremolinos, trabajamos en toda la Costa del Sol.",
                eyebrow="Contacto", h1="¿Preguntas sobre <br>nuestros servicios?",
                lead="Para no interrumpir el trabajo en casa de nuestros clientes, usamos WhatsApp y email. Respondemos en cuanto terminamos el servicio en curso.",
                wa="WhatsApp", email="Email", loc="Ubicación", loc_v="29620 Torremolinos, Málaga, España", follow="Sigue nuestro trabajo",
                maps="Abrir en Google Maps")),
    "privacy-policy": dict(
        en=dict(title="Privacy policy | Pro Clean", desc="How Pro Clean collects and uses personal information.", eyebrow="Legal", h1="Privacy policy",
                lead="How we collect, use and protect personal information.", src="privacy-en.txt"),
        es=dict(title="Política de privacidad | Pro Clean", desc="Cómo recoge y utiliza Pro Clean la información personal.", eyebrow="Legal", h1="Política de privacidad",
                lead="Cómo recogemos, usamos y protegemos la información personal.", src="privacy-es.txt")),
}


# ================================================================ helpers
def paths(lang, slug):
    """R = relative path to site root, L = relative path to language root."""
    depth = (1 if lang == "es" else 0) + (1 if slug else 0)
    R = "../" * depth
    L = "../" if slug else ""
    return R, L


def other_href(lang, slug, R):
    s = f"{slug}/" if slug else ""
    return f"{R}es/{s}" if lang == "en" else f"{R}{s}"


def header(lang, slug, active):
    u = UI[lang]
    R, L = paths(lang, slug)
    quote = "#quote" if not slug else f"{L}#quote"
    home = "#top" if not slug else L
    items = []
    mitems = []
    for key in NAV:
        cur = ' class="title-4 active" aria-current="page"' if key == active else ' class="title-4"'
        items.append(f'      <li><a{cur} href="{L}{key}/">{u[key]}</a></li>')
        mcur = ' aria-current="page"' if key == active else ""
        mitems.append(f'    <li><a class="heading-4" href="{L}{key}/"{mcur}>{u[key]}</a></li>')
    oh = other_href(lang, slug, R)
    return f"""<!--NAV-->
<header class="nav-wrap">
  <nav class="nav" aria-label="Main">
    <a class="brand" href="{home}" aria-label="Pro Clean">
      <img src="{R}assets/img/mark.png" alt="" width="28" height="28">
      <span class="title-3">Pro Clean</span>
    </a>
    <ul class="nav-links">
{chr(10).join(items)}
    </ul>
    <a class="lang title-4" href="{oh}" hreflang="{u['other_lang']}" lang="{u['other_lang']}" aria-label="{u['other_aria']}">{u['other_short']}</a>
    <a class="btn btn-sm btn-primary nav-cta button-sm" href="{quote}">{u['quote']}</a>
    <button class="menu-btn" aria-label="{u['menu']}" aria-expanded="false" aria-controls="mobile-menu">
      <span></span><span></span>
    </button>
  </nav>
</header>

<div class="mobile-menu" id="mobile-menu" hidden>
  <ul>
    <li><a class="heading-4" href="{home}">{u['home']}</a></li>
{chr(10).join(mitems)}
    <li><a class="title-2 lang-m" href="{oh}" hreflang="{u['other_lang']}" lang="{u['other_lang']}"><i class="ph ph-globe-simple"></i> {u['other']}</a></li>
    <li><a class="btn btn-primary button-md" href="{quote}">{u['quote_l']}</a></li>
  </ul>
</div>
<!--/NAV-->"""


def footer(lang, slug):
    u = UI[lang]
    R, L = paths(lang, slug)
    home = "#top" if not slug else L
    oh = other_href(lang, slug, R)
    links = "\n".join(f'      <a href="{L}{k}/">{u[k]}</a>' for k in NAV)
    return f"""<!--FOOTER-->
<footer class="footer">
  <div class="container footer-grid footer-grid-4">
    <div>
      <a class="brand" href="{home}"><img src="{R}assets/img/mark.png" alt="" width="28" height="28"><span class="title-3">Pro Clean</span></a>
      <p class="caption-2 muted">{u['footer_desc']}</p>
    </div>
    <div class="footer-links body-6">
{links}
    </div>
    <div class="footer-links body-6">
      <a href="{WA}"><i class="ph ph-whatsapp-logo"></i> WhatsApp</a>
      <a href="mailto:office@pro-clean.es"><i class="ph ph-envelope-simple"></i> Email</a>
      <a href="https://www.instagram.com/pro_clean_es/"><i class="ph ph-instagram-logo"></i> Instagram</a>
      <a href="https://www.youtube.com/channel/UC67BY-E5Oqxgv9N_-lpzrfA"><i class="ph ph-youtube-logo"></i> YouTube</a>
    </div>
    <div class="footer-links body-6">
      <a href="{L}privacy-policy/">{u['privacy']}</a>
      <a href="{L}privacy-policy/">{u['cookies']}</a>
      <a href="{oh}" hreflang="{u['other_lang']}" lang="{u['other_lang']}">{u['other_footer']}</a>
    </div>
  </div>
  <p class="container caption-5 muted copy">© <span id="year">2026</span> Pro Clean. {u['copy']}</p>
</footer>

<a class="wa-float" href="{WA}" aria-label="{u['wa_aria']}"><i class="ph-fill ph-whatsapp-logo"></i></a>
<!--/FOOTER-->"""


def head(lang, slug, title, desc, extra=""):
    R, _ = paths(lang, slug)
    s = f"{slug}/" if slug else ""
    live = f"{LIVE}{'es/' if lang == 'es' else ''}{s}"
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<meta name="robots" content="noindex, nofollow">
<link rel="canonical" href="{live}">
<link rel="alternate" hreflang="en" href="{SITE}{s}">
<link rel="alternate" hreflang="es" href="{SITE}es/{s}">
<link rel="alternate" hreflang="x-default" href="{SITE}{s}">
<meta property="og:type" content="website">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:image" content="{SITE}assets/img/sofa.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#F6F7F5">
<link rel="icon" href="{R}assets/img/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://unpkg.com/@phosphor-icons/web@2.1.1/src/regular/style.css">
<link rel="stylesheet" href="https://unpkg.com/@phosphor-icons/web@2.1.1/src/fill/style.css">
<link rel="stylesheet" href="{R}assets/style.css">{extra}
</head>
<body>
<a class="skip" href="#main">{UI[lang]['skip']}</a>
"""


def page(lang, slug, active, title, desc, main, extra=""):
    R, _ = paths(lang, slug)
    return (head(lang, slug, title, desc, extra) + "\n" + header(lang, slug, active) +
            f'\n\n<main id="main">\n{main}\n</main>\n\n' + footer(lang, slug) +
            f'\n\n<script src="{R}assets/app.js" defer></script>\n</body>\n</html>\n')


def crumbs(lang, slug, trail):
    u = UI[lang]
    _, L = paths(lang, slug)
    parts = [f'<li><a href="{L}">{u["home"]}</a></li>']
    for label, href in trail[:-1]:
        parts.append(f'<li><a href="{href}">{E(label)}</a></li>')
    parts.append(f'<li aria-current="page">{E(trail[-1][0])}</li>')
    return f'<nav class="crumbs caption-2" aria-label="{u["crumbs"]}"><ol>{"".join(parts)}</ol></nav>'


def page_hero(lang, slug, trail, eyebrow, h1, lead, visual="", cta=True):
    u = UI[lang]
    _, L = paths(lang, slug)
    actions = ""
    if cta:
        actions = f"""
      <div class="hero-actions">
        <a class="btn btn-primary btn-lg button-md" href="{L}#quote"><i class="ph ph-whatsapp-logo"></i> {u['quote_l']}</a>
        <a class="link body-5" href="{WA}">{u['wa_btn']} <i class="ph ph-arrow-up-right"></i></a>
      </div>"""
    grid = " page-hero-grid" if visual else ""
    return f"""<section class="page-hero">
  <div class="container{grid}">
    <div class="hero-copy">
      {crumbs(lang, slug, trail)}
      <p class="eyebrow caption-1">{eyebrow}</p>
      <h1 class="heading-2 grad">{h1}</h1>
      <p class="lead body-3">{lead}</p>{actions}
    </div>{visual}
  </div>
</section>"""


def areas(lang, slug):
    u = UI[lang]
    R, _ = paths(lang, slug)
    towns = "".join(f'<li class="body-5">{t}</li>' for t in TOWNS)
    return f"""<section class="section" id="areas">
  <div class="container areas-grid">
    <div class="reveal">
      <p class="eyebrow caption-1">{u['areas_eyebrow']}</p>
      <h2 class="heading-3">{u['areas_h']}</h2>
      <p class="body-3 muted">{u['areas_p']}</p>
      <ul class="towns">{towns}</ul>
    </div>
    <figure class="map reveal"><img src="{R}assets/img/gallery/g13.jpg" alt="{u['map_alt']}" loading="lazy" width="900" height="664"></figure>
  </div>
</section>"""


def cta_band(lang, slug):
    u = UI[lang]
    _, L = paths(lang, slug)
    return f"""<section class="section final">
  <div class="container final-inner reveal">
    <h2 class="heading-2 grad">{u['cta_h']}</h2>
    <p class="body-3 muted">{u['cta_p']}</p>
    <a class="btn btn-primary btn-lg button-md" href="{L}#quote"><i class="ph ph-whatsapp-logo"></i> {u['quote_l']}</a>
  </div>
</section>"""


def photo_alt(lang, img, cat, ba):
    c = CAT[lang]
    return f"{c[cat]}, {c['ba'] if ba else c['work']}"


BA = {"sofa.jpg", "mattress-ba.jpg", "carpet-ba.jpg", "chair.jpg", "sofa-ba.jpg", "gallery/g12.jpg", "leather.jpg"}


def service_cards(lang, slug, exclude=None, cls="cards"):
    R, L = paths(lang, slug)
    out = []
    for s in SERVICES:
        if s["slug"] == exclude:
            continue
        t = s[lang]
        img = (f'<div class="card-img"><img src="{R}assets/img/{s["img"]}" alt="{E(photo_alt(lang, s["img"], "sofa", True) if False else t["name"])}" loading="lazy"></div>'
               if s["img"] else "")
        plain = "" if s["img"] else " card-plain"
        out.append(f"""      <article class="card card-link{plain} reveal">
        {img}
        <div class="card-body">
          <i class="ph ph-{s['icon']} icon"></i>
          <h3 class="heading-6"><a class="stretched" href="{L}{s['slug']}/">{t['name']}</a></h3>
          <p class="body-6 muted">{t['card']}</p>
          <span class="more body-5">{UI[lang]['more']} <i class="ph ph-arrow-right"></i></span>
        </div>
      </article>""")
    return f'<div class="{cls}">\n' + "\n".join(out) + "\n    </div>"


# ================================================================ page builders
def build_service(lang, s):
    u = UI[lang]
    t = s[lang]
    slug = s["slug"]
    R, L = paths(lang, slug)
    if s["img"]:
        state = CAT[lang]["ba"] if s["img"] in BA else CAT[lang]["work"]
        wide = " ba-frame-wide" if s.get("wide") else ""
        visual = f"""
    <figure class="hero-visual">
      <div class="ba-frame{wide}"><img src="{R}assets/img/{s['img']}" alt="{E(t['name'])}, {state}" fetchpriority="high"></div>
    </figure>"""
    else:
        visual = f"""
    <div class="icon-panel" aria-hidden="true"><i class="ph ph-{s['icon']}"></i></div>"""
    hero = page_hero(lang, slug, [(u["services"], f"{L}services/"), (t["name"], "")], u["services"], t["h1"], t["lead"], visual)
    pts = "\n".join(f"""      <div class="benefit reveal"><i class="ph ph-check-circle icon"></i><p class="body-1">{E(a)}</p><p class="body-6 muted">{E(b)}</p></div>"""
                    for a, b in t["points"])
    why = f"""<section class="section section-alt">
  <div class="container">
    <div class="section-head reveal">
      <p class="eyebrow caption-1">{u['why']}</p>
      <h2 class="heading-3">{t['name']}</h2>
    </div>
    <div class="benefits benefits-3">
{pts}
    </div>
  </div>
</section>"""
    steps = ""
    if "steps" in t:
        st = "\n".join(f"""      <li class="step reveal"><span class="step-n caption-3">{i:02d}</span><p class="title-1">{E(a)}</p><p class="body-6 muted">{E(b)}</p></li>"""
                       for i, (a, b) in enumerate(t["steps"], 1))
        hd = "How it works" if lang == "en" else "Cómo funciona"
        steps = f"""<section class="section">
  <div class="container">
    <div class="section-head reveal"><p class="eyebrow caption-1">{hd}</p><h2 class="heading-3">{'Our 6 step process' if lang == 'en' else 'Nuestro método en 6 pasos'}</h2></div>
    <ol class="steps steps-6">
{st}
    </ol>
  </div>
</section>"""
    photos = ""
    if s["photos"]:
        figs = "\n".join(f"""      <figure class="result reveal"><img src="{R}assets/img/{p}" alt="{E(photo_alt(lang, p, c, p in BA))}" loading="lazy"></figure>"""
                         for p, c in s["photos"])
        photos = f"""<section class="section">
  <div class="container">
    <div class="section-head reveal"><p class="eyebrow caption-1">{u['results']}</p><h2 class="heading-3">{u['results_h']}</h2><p class="body-3 muted">{u['ba_note']}</p></div>
    <div class="results results-auto">
{figs}
    </div>
  </div>
</section>"""
    if s.get("video"):
        vids = "\n".join(video_tag(R, v, p, f"{CAT[lang]['vid']} {t['name']}") for v, p in s["video"])
        photos = photos.replace('    <div class="results results-auto">', f'    <div class="videos">\n{vids}\n    </div>\n    <div class="results results-auto">', 1) if photos else photos
    others = f"""<section class="section section-alt">
  <div class="container">
    <div class="section-head reveal"><p class="eyebrow caption-1">{u['other_services']}</p></div>
    {service_cards(lang, slug, exclude=slug, cls="cards cards-compact")}
  </div>
</section>"""
    main = "\n\n".join([hero, why, steps, photos, others, areas(lang, slug), cta_band(lang, slug)])
    schema = f"""
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"Service","name":{json_str(t['name'])},"areaServed":"Costa del Sol","provider":{{"@type":"HouseCleaningService","name":"Pro Clean","telephone":"+34621383059","address":{{"@type":"PostalAddress","postalCode":"29620","addressLocality":"Torremolinos","addressCountry":"ES"}}}}}}</script>"""
    title = f"{t['name']} Costa del Sol | Pro Clean"
    return page(lang, slug, "services", title, t["desc"], main, schema)


def video_tag(R, v, poster, label):
    long_ = v == "yacht.mp4"
    attrs = 'controls preload="none" playsinline' if long_ else 'autoplay muted loop playsinline preload="metadata"'
    return (f'      <figure class="video reveal{" video-long" if long_ else ""}"><video {attrs} poster="{R}assets/img/{poster}" aria-label="{E(label)}">'
            f'<source src="{R}assets/video/{v}" type="video/mp4"></video></figure>')


def json_str(s):
    import json
    return json.dumps(s, ensure_ascii=False)


def build_services(lang):
    u = UI[lang]
    p = PAGES["services"][lang]
    slug = "services"
    hero = page_hero(lang, slug, [(u["services"], "")], p["eyebrow"], p["h1"], p["lead"])
    grid = f"""<section class="section section-tight">
  <div class="container">
    {service_cards(lang, slug)}
  </div>
</section>"""
    main = "\n\n".join([hero, grid, areas(lang, slug), cta_band(lang, slug)])
    return page(lang, slug, "services", p["title"], p["desc"], main)


def build_gallery(lang):
    u = UI[lang]
    p = PAGES["gallery"][lang]
    slug = "gallery"
    R, _ = paths(lang, slug)
    cats = ["sofa", "leather", "mattress", "carpet", "chair", "yacht", "wardrobe", "video"]
    chips = f'<button class="chip body-5 on" data-filter="all" aria-pressed="true">{p["all"]}</button>' + "".join(
        f'<button class="chip body-5" data-filter="{c}" aria-pressed="false">{CAT[lang][c]}</button>' for c in cats)
    figs = "\n".join(f"""      <figure class="g-item" data-cat="{c}"><img src="{R}assets/img/{img}" alt="{E(photo_alt(lang, img, c, ba))}" loading="lazy"><figcaption class="caption-1">{CAT[lang][c]}</figcaption></figure>"""
                     for img, c, ba in GALLERY)
    figs = "\n".join(
        video_tag(R, v, poster, f"{CAT[lang]['vid']} {CAT[lang][c]}").replace('class="video reveal', 'data-cat="video" class="g-item video')
        .replace("</video></figure>", f'</video><figcaption class="caption-1">{CAT[lang]["video"]} · {CAT[lang][c]}</figcaption></figure>')
        for v, poster, c in VIDEOS) + "\n" + figs
    hero = page_hero(lang, slug, [(u["gallery"], "")], p["eyebrow"], p["h1"], p["lead"] + " " + u["ba_note"])
    body = f"""<section class="section section-tight">
  <div class="container">
    <div class="chips" role="group">{chips}</div>
    <div class="gallery" id="gallery">
{figs}
    </div>
  </div>
</section>"""
    main = "\n\n".join([hero, body, cta_band(lang, slug)])
    return page(lang, slug, "gallery", p["title"], p["desc"], main)


STAR5 = '<div class="stars" aria-label="5/5">' + '<i class="ph-fill ph-star"></i>' * 5 + "</div>"


def build_reviews(lang):
    u = UI[lang]
    p = PAGES["reviews"][lang]
    slug = "reviews"
    hero = page_hero(lang, slug, [(u["reviews"], "")], p["eyebrow"], p["h1"], p["lead"], cta=False)
    g = "\n".join(f"""      <blockquote class="review reveal" lang="{lg}">{STAR5}<p class="body-3">“{E(txt)}”</p><footer class="title-4">{E(n)} <span class="caption-2 muted" lang="{lang}">{p['posted']}</span></footer></blockquote>"""
                  for n, lg, txt in GOOGLE)
    s = "\n".join(f"""      <blockquote class="review reveal" lang="{lg}">{STAR5}<p class="title-3">{E(ti)}</p><p class="body-3">“{E(txt)}”</p><footer class="title-4">{E(n)} <span class="caption-2 muted">{d}</span></footer></blockquote>"""
                  for ti, d, lg, txt, n in SITE_REVIEWS)
    main = f"""{hero}

<section class="section section-tight">
  <div class="container">
    <div class="rev-head reveal">
      <div><h2 class="heading-4">{p['g_h']}</h2><p class="body-5 muted">{STAR5} <span>{p['g_sum']}</span></p></div>
      <a class="btn btn-primary button-md" href="{MAPS}"><i class="ph ph-google-logo"></i> {p['write']}</a>
    </div>
    <div class="reviews reviews-masonry">
{g}
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="container">
    <div class="rev-head reveal">
      <div><h2 class="heading-4">{p['s_h']}</h2><p class="body-5 muted">{STAR5} <span>{p['s_sum']}</span></p></div>
    </div>
    <div class="reviews reviews-masonry">
{s}
    </div>
  </div>
</section>

{cta_band(lang, slug)}"""
    return page(lang, slug, "reviews", p["title"], p["desc"], main)


def build_about(lang):
    u = UI[lang]
    p = PAGES["about"][lang]
    slug = "about"
    R, _ = paths(lang, slug)
    visual = f"""
    <figure class="hero-visual"><div class="ba-frame"><img src="{R}assets/img/carpet.jpg" alt="{E(CAT[lang]['carpet'])}, {CAT[lang]['work']}" width="900" height="957" fetchpriority="high"></div></figure>"""
    hero = page_hero(lang, slug, [(u["about"], "")], p["eyebrow"], p["h1"], p["lead"], visual)
    body = "".join(f'<p class="body-3">{E(x)}</p>' for x in p["body"])
    vals = "\n".join(f"""      <div class="benefit reveal"><i class="ph {ic} icon"></i><p class="body-1">{E(a)}</p><p class="body-6 muted">{E(b)}</p></div>"""
                     for ic, a, b in p["values"])
    main = f"""{hero}

<section class="section section-alt">
  <div class="container">
    <div class="prose reveal">{body}</div>
    <div class="benefits">
{vals}
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-head reveal"><p class="eyebrow caption-1">{p['services_h']}</p></div>
    {service_cards(lang, slug, cls="cards cards-compact")}
  </div>
</section>

{areas(lang, slug)}

{cta_band(lang, slug)}"""
    return page(lang, slug, "about", p["title"], p["desc"], main)


def build_contact(lang):
    u = UI[lang]
    p = PAGES["contact"][lang]
    slug = "contact"
    hero = page_hero(lang, slug, [(u["contact"], "")], p["eyebrow"], p["h1"], p["lead"])
    main = f"""{hero}

<section class="section section-tight">
  <div class="container contact-cards">
    <a class="contact-card reveal" href="{WA}"><i class="ph ph-whatsapp-logo icon"></i><span class="caption-1 muted">{p['wa']}</span><span class="title-1">+34 621 383 059</span></a>
    <a class="contact-card reveal" href="mailto:office@pro-clean.es"><i class="ph ph-envelope-simple icon"></i><span class="caption-1 muted">{p['email']}</span><span class="title-1">office@pro-clean.es</span></a>
    <a class="contact-card reveal" href="{MAPS}"><i class="ph ph-map-pin icon"></i><span class="caption-1 muted">{p['loc']}</span><span class="title-1">{p['loc_v']}</span><span class="body-5 more">{p['maps']} <i class="ph ph-arrow-up-right"></i></span></a>
  </div>
  <div class="container socials reveal">
    <p class="title-3">{p['follow']}</p>
    <div class="social-row">
      <a class="chip body-5" href="https://www.instagram.com/pro_clean_es/"><i class="ph ph-instagram-logo"></i> Instagram</a>
      <a class="chip body-5" href="https://www.youtube.com/channel/UC67BY-E5Oqxgv9N_-lpzrfA"><i class="ph ph-youtube-logo"></i> YouTube</a>
      <a class="chip body-5" href="https://www.facebook.com/profile.php?id=61582204746512"><i class="ph ph-facebook-logo"></i> Facebook</a>
      <a class="chip body-5" href="{MAPS}"><i class="ph ph-google-logo"></i> Google</a>
    </div>
  </div>
</section>

{areas(lang, slug)}"""
    return page(lang, slug, "contact", p["title"], p["desc"], main)


def build_privacy(lang):
    u = UI[lang]
    p = PAGES["privacy-policy"][lang]
    slug = "privacy-policy"
    raw = open(os.path.join(ROOT, "tools", p["src"]), encoding="utf-8").read()
    lines = [l.strip() for l in raw.splitlines() if l.strip()]
    # drop leading chrome and trailing "Contact us" button
    drop = {"Skip to content", "Ir al contenido", "Privacy Policy", "Política de privacidad"}
    while lines and lines[0] in drop:
        lines.pop(0)
    if lines and lines[-1] in ("Contact us", "Contáctenos", "Contacto"):
        lines.pop()
    # merge broken lines: a line that does not end a sentence joins the next one
    merged = []
    for l in lines:
        if merged and not re.search(r"[.!?:”\"]$", merged[-1]) and len(merged[-1]) > 60:
            merged[-1] += " " + l
        else:
            merged.append(l)
    out = []
    for l in merged:
        is_head = (len(l) < 90 and not l.endswith(".")) or l.endswith("?")
        out.append(f'<h2 class="heading-6">{E(l)}</h2>' if is_head else f'<p class="body-3">{E(l)}</p>')
    hero = page_hero(lang, slug, [(u["privacy"], "")], p["eyebrow"], p["h1"], p["lead"], cta=False)
    main = f"""{hero}

<section class="section section-tight">
  <div class="container"><article class="prose legal">
{chr(10).join(out)}
  </article></div>
</section>"""
    return page(lang, slug, None, p["title"], p["desc"], main)


def write(lang, slug, content):
    d = os.path.join(ROOT, *(["es"] if lang == "es" else []), slug)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "index.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print("wrote", os.path.relpath(os.path.join(d, "index.html"), ROOT))


def patch_home(lang):
    path = os.path.join(ROOT, *(["es"] if lang == "es" else []), "index.html")
    s = open(path, encoding="utf-8").read()
    nav = header(lang, "", None)
    foot = footer(lang, "")
    if "<!--NAV-->" in s:
        s = re.sub(r"(?s)<!--NAV-->.*?<!--/NAV-->", lambda m: nav, s)
    else:
        s = re.sub(r'(?s)<header class="nav-wrap">.*?</div>\n(?=\n<main)', lambda m: nav + "\n", s)
    if "<!--FOOTER-->" in s:
        s = re.sub(r"(?s)<!--FOOTER-->.*?<!--/FOOTER-->", lambda m: foot, s)
    else:
        s = re.sub(r'(?s)<footer class="footer">.*?<a class="wa-float"[^\n]*\n', lambda m: foot + "\n", s)
    s = s.replace('content="noindex">', 'content="noindex, nofollow">')
    # link the service cards on the home page to their pages
    names = {s_["slug"]: s_[lang] for s_ in SERVICES}
    home_titles = {
        "en": {"Fabric sofas": "sofa-cleaning", "Leather sofas": "sofa-cleaning", "Mattresses": "mattress-cleaning",
               "Carpets and rugs": "carpet-cleaning", "Chairs": "chair-cleaning", "Yacht furniture": "yacht-furniture-cleaning",
               "Wardrobe organisation": "wardrobe-organisation-service"},
        "es": {"Sofás de tela": "sofa-cleaning", "Sofás de piel": "sofa-cleaning", "Colchones": "mattress-cleaning",
               "Alfombras y moquetas": "carpet-cleaning", "Sillas": "chair-cleaning", "Tapicería de yates": "yacht-furniture-cleaning",
               "Organización de armarios": "wardrobe-organisation-service"},
    }[lang]
    for title, sl in home_titles.items():
        s = s.replace(f'<h3 class="heading-6">{title}</h3>', f'<h3 class="heading-6"><a class="h-link" href="{sl}/">{title} <i class="ph ph-arrow-right"></i></a></h3>')
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(s)
    print("patched", os.path.relpath(path, ROOT))


if __name__ == "__main__":
    for lang in ("en", "es"):
        for s in SERVICES:
            write(lang, s["slug"], build_service(lang, s))
        write(lang, "services", build_services(lang))
        write(lang, "gallery", build_gallery(lang))
        write(lang, "reviews", build_reviews(lang))
        write(lang, "about", build_about(lang))
        write(lang, "contact", build_contact(lang))
        write(lang, "privacy-policy", build_privacy(lang))
        patch_home(lang)
