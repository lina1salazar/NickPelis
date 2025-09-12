from extensions import db
from models.peliculas import Pelicula, Genero, Actor


def llenar_datos_iniciales():
    """Carga datos iniciales solo si no existen registros en la DB."""
    if db.session.query(Genero).count() == 0:
        print("🌱 Ejecutando carga datos iniciales...")

        # 🔹 Generos
        generos_data = [
            (10760,'Acción'),(10750,'Animación'),(10763,'Aventura'),
            (10759,'Ciencia Ficción'),(10752,'Comedia'),(10757,'Crimen'),
            (10751,'Drama'),(10764,'Fantasía'),(10756,'Historia'),
            (10766,'Horror'),(10753,'Melodrama'),(10762,'Misterio'),
            (10754,'Stop Motion'),(10761,'Suspenso'),(10755,'Terror'),
            (10765,'Thiller'),(10758,'Thriller')
        ]
        generos = {id_: Genero(id_genero=id_, nombre=nombre) for id_, nombre in generos_data}
        db.session.add_all(generos.values())

        # 🔹 Actores
        actores_data = [
            (1,'Jacki Weaver'),(2,'Sarah Snook'),(3,'Charlotte Belsey'),(4,'Theo James'),
            (5,'Tatiana Maslany'),(6,'Christian Convery'),(7,'Elijah Wood'),(8,'Adam Scott'),
            (9,'Liam Neeson'),(10,'Ralph Fiennes'),(11,'Ben Kingsley'),(12,'Marlon Brando'),
            (13,'Al Pacino'),(14,'James Caan'),(15,'Jesse Eisenberg'),(16,'Kieran Culkin'),
            (17,'Demi Moore'),(18,'Margaret Qualley'),(19,'Tom Hardy'),(20,'Charlize Theron'),
            (21,'Nicholas Hoult'),(22,'John Travolta'),(23,'Uma Thurman'),(24,'Samuel L. Jackson'),
            (25,'Malcolm McDowell'),(26,'Patrick Magee'),(27,'Michael Bates'),(28,'Anthony Perkins'),
            (29,'Janet Leigh'),(30,'Vera Miles'),(31,'Matthew Broderick'),(32,'James Earl Jones'),
            (33,'Jeremy Irons'),(34,'Scott Weinger'),(35,'Robin Williams'),(36,'Linda Larkin'),
            (37,'Tom Hanks'),(38,'Tim Allen'),(39,'Don Rickles'),(40,'Craig T. Nelson'),
            (41,'Holly Hunter'),(42,'Jodi Benson'),(43,'Samuel E. Wright'),(44,'Pat Carroll'),
            (45,'Mike Myers'),(46,'Eddie Murphy'),(47,'Cameron Diaz'),(48,'Ben Stiller'),
            (49,'Chris Rock'),(50,'David Schwimmer'),(51,'Val Kilmer'),(52,'Michelle Pfeiffer'),
            (53,'Sean Astin'),(54,'Karl Urban'),(55,'Jack Black'),(56,'Jason Momoa'),
            (57,'Sebastian Hansen'),(58,'Rami Malek'),(59,'Rachel Brosnahan'),(60,'Jon Bernthal'),
            (61,'Miles Caton'),(62,'Saul Williams'),(63,'Andrene Ward-Hammond')
        ]
        actores = {id_: Actor(id_actor=id_, nombre=nombre) for id_, nombre in actores_data}
        db.session.add_all(actores.values())

        # 🔹 Películas
        peliculas_data = [
            (
                1,
                'memorias-de-un-caracol',
                'Memorias de un Caracol',
                2025,
                7.9,
                94,
                "Grace Pudel, una niña solitaria apasionada por las figuras de caracoles y las novelas románticas, sufre la pérdida de su padre y la separación de su hermano mellizo, Gilbert, lo que la sumerge en la ansiedad. Su vida cambia cuando conoce a Pinky, una anciana excéntrica y llena de vitalidad, con quien forja una amistad que transforma su destino.",
                False
            ),
            (
                2,
                'the-monkey',
                'The Monkey',
                2025,
                5.8,
                97,
                "Cuando Hal y Bill encuentran en el ático el antiguo mono de juguete de su padre, comienzan a ocurrir extrañas muertes. Asustados, lo desechan y siguen con sus vidas por separado. Años después, las tragedias regresan, obligándolos a reunirse para destruir el siniestro objeto antes de que siga cobrando vidas.",
                False
            ),
            (
                3,
                'la-lista-de-schindler',
                'La Lista de Schindler',
                1993,
                9,
                196,
                "La historia real de Oskar Schindler, un empresario alemán que salvó a más de mil judíos durante el Holocausto al emplearlos en su fábrica.",
                False
            ),
            (
                4,
                'el-padrino',
                'El Padrino',
                1972,
                9.3,
                175,
                "La saga de la familia Corleone, una poderosa dinastía mafiosa en Nueva York, y su lucha por mantener el poder y la influencia en el mundo del crimen organizado.",
                False
            ),
            (
                5,
                'un-dolor-real',
                'Un Dolor Real',
                2024,
                6.4,
                90,
                "Dos primos judíos viajan a Polonia, enfrentando recuerdos familiares y viejas tensiones en un viaje de autodescubrimiento.",
                False
            ),
            (
                6,
                'la-sustancia',
                'La sustancia',
                2024,
                6.5,
                141,
                "Explora las implicaciones éticas y sociales de los avances científicos a través de una narrativa intrigante y provocadora.",
                False
            ),
            (
                7,
                'mad-max-furia-en-la-carretera',
                'Mad Max: Furia en la carretera',
                2015,
                7.6,
                120,
                "En un futuro post-apocalíptico, Max se une a Furiosa para escapar de un tiránico gobernante y su ejército, mientras luchan por la supervivencia en un mundo devastado.",
                False
            ),
            (
                8,
                'tiempos-violentos',
                'Tiempos Violentos',
                1994,
                9.1,
                154,
                "Jules y Vincent, dos asesinos a sueldo con muy pocas luces, trabajan para Marsellus Wallace. Vincent le confiesa a Jules que Marsellus le ha pedido que cuide de Mia, su mujer. Jules le recomienda prudencia porque es muy peligroso sobrepasarse con la novia del jefe. Cuando llega la hora de trabajar, ambos deben ponerse manos a la obra. Su misión: recuperar un misterioso maletín.",
                False
            ),
            (
                9,
                'la-naranja-mecanica',
                'La Naranja Mecánica',
                1971,
                7.9,
                136,
                "En una sociedad distópica, Alex DeLarge, un joven violento y amante de la música clásica, es sometido a una controvertida terapia de rehabilitación conductual.",
                False
            ),
            (
                10,
                'psicosis',
                'Psicosis',
                1960,
                9.2,
                109,
                "Marion Crane, una secretaria que huye tras robar dinero, se hospeda en un motel regentado por el inquietante Norman Bates, desencadenando una serie de eventos aterradores.",
                False
            ),
            (
                11,
                'el-rey-leon',
                'El Rey León',
                1994,
                8.4,
                85,
                "Un joven león llamado Simba debe enfrentarse a su destino y reclamar su lugar como rey de la sabana tras la muerte de su padre, Mufasa.",
                False
            ),
            (
                12,
                'aladdin',
                'Aladdín',
                1992,
                8.2,
                90,
                "Aladdin, un joven humilde, encuentra una lámpara mágica que le concede tres deseos y le permite luchar por el amor de la princesa Jasmine.",
                False
            ),
            (
                13,
                'toy-story',
                'Toy Story',
                1995,
                9.2,
                77,
                "Los juguetes de Andy, un niño de seis años, temen que haya llegado su hora y que un nuevo regalo de cumpleaños les sustituya en el corazón de su dueño. Woody, un vaquero que ha sido hasta ahora el juguete favorito de Andy, trata de tranquilizarlos hasta que aparece Buzz Lightyear, un héroe espacial dotado de todo tipo de avances tecnológicos. Woody es relegado a un segundo plano, pero su constante rivalidad se transformará en una gran amistad cuando ambos se pierden en la ciudad sin saber cómo volver a casa.",
                False
            ),
            (
                14,
                'los-increibles-2',
                'Los Increíbles 2',
                2018,
                8.9,
                120,
                "La familia Parr, una familia de superhéroes, lucha por mantener su identidad secreta mientras enfrentan a un enemigo peligroso que amenaza a la humanidad.",
                False
            ),
            (
                15,
                'la-sirenita',
                'La Sirenita',
                1989,
                8.8,
                83,
                "Ariel, una sirena joven, hace un trato con la malvada bruja Úrsula para convertirse en humana y poder estar con el príncipe Eric.",
                False
            ),
            (
                16,
                'shrek',
                'Shrek',
                2001,
                8.5,
                92,
                "Hace mucho, mucho tiempo, en una lejanísima ciénaga vivía un intratable ogro llamado Shrek. Pero de repente, un día, su absoluta soledad se ve interrumpida por una invasión de sorprendentes personajes de cuento. Hay ratoncitos ciegos en su comida, un enorme y malísimo lobo en su cama, tres cerditos sin hogar y otros muchos seres increíbles que han sido deportados de su reino por el malvado Lord Farquaad...",
                False
            ),
            (
                17,
                'madagascar',
                'Madagascar',
                2005,
                6.4,
                80,
                "Un grupo de animales del zoológico de Central Park escapa y termina en la isla de Madagascar, donde deben adaptarse a la vida en la jungla.",
                False
            ),
            (
                18,
                'el-principe-de-egipto',
                'El Príncipe de Egipto',
                1998,
                7.8,
                99,
                "La historia bíblica de Moisés, quien se convierte en el líder de los hebreos, luchando por liberar a su pueblo de la esclavitud en Egipto.",
                False
            ),
            (
                19,
                'el-senor-de-los-anillos-el-retorno-del-rey',
                'El Señor de los Anillos: El Retorno del Rey',
                2003,
                8.3,
                202,
                "El clímax de la trilogía de ""El Señor de los Anillos"", donde Frodo y Sam luchan por destruir el Anillo Único en el Monte del Destino.",
                False
            ),
            (
                20,
                'una-pelicula-de-minecraft',
                'Una Película de Minecraft',
                2025,
                6.8,
                101,
                "Un portal desconocido atrae a cuatro jóvenes hacia el Supramundo, un reino cúbico y mágico que toma forma a partir de la imaginación. Su única esperanza de regresar es dominar un terreno cambiante y confiar en la ayuda de un artesano inesperado llamado Steve.",
                True
            ),
            (
                21,
                'the-amateur',
                'The Amateur',
                2025,
                6.7,
                123,
                "Charlie Heller es un brillante decodificador de la CIA cuyo mundo se derrumba cuando su esposa muere en un atentado terrorista en Londres.",
                True
            ),
            (
                22,
                'los-pecadores',
                'Los Pecadores',
                2025,
                8.2,
                138,
                "Tratando de descubrir sus problemáticas vidas detrás, los hermanos gemelos regresan a su ciudad natal para comenzar de nuevo, solo para descubrir que un mal aún mayor los espera para darles la bienvenida nuevamente.",
                True
            )
        ]

        peliculas = {}
        for id_, slug, nombre, anio, puntuacion, duracion, sinopsis, destacada in peliculas_data:
            pelicula = Pelicula(
                id_pelicula=id_,
                slug=slug,
                nombre=nombre,
                anio=anio,
                puntuacion=puntuacion,
                duracion=duracion,
                sinopsis=sinopsis,
                poster=f"img/posters/{slug}.webp",
                banner=f"img/banners/{slug}.webp",
                destacada=destacada
            )
            peliculas[id_] = pelicula
            db.session.add(pelicula)

        db.session.commit()

        # 🔹 Relaciones Películas-Actores
        relaciones_actores = [
            (1,1),(1,2),(1,3),(2,4),(2,5),(2,6),(2,7),(19,7),(2,8),(3,9),(3,10),(18,10),(3,11),
            (4,12),(4,13),(4,14),(5,15),(5,16),(6,17),(6,18),(7,19),(7,20),(7,21),(8,22),(8,23),
            (8,24),(14,24),(9,25),(9,26),(9,27),(10,28),(10,29),(10,30),(11,31),(11,32),(11,33),
            (12,34),(12,35),(12,36),(13,37),(13,38),(13,39),(14,40),(14,41),(15,42),(15,43),
            (15,44),(16,45),(16,46),(16,47),(17,48),(17,49),(17,50),(18,51),(18,52),(19,53),
            (19,54),(20,55),(20,56),(20,57),(21,58),(21,59),(21,60),(22,61),(22,62),(22,63)
        ]
        for id_pelicula, id_actor in relaciones_actores:
            peliculas[id_pelicula].actores.append(actores[id_actor])

        # 🔹 Relaciones Películas-Géneros
        relaciones_generos = [
            (1,10750),(11,10750),(12,10750),(13,10750),(14,10750),(15,10750),(16,10750),(17,10750),
            (18,10750),(1,10751),(3,10751),(4,10751),(5,10751),(8,10751),(9,10751),(11,10751),
            (18,10751),(19,10751),(21,10751),(1,10752),(2,10752),(5,10752),(13,10752),(16,10752),
            (17,10752),(20,10752),(1,10753),(1,10754),(2,10755),(10,10755),(3,10756),(4,10757),
            (8,10757),(6,10758),(6,10759),(7,10759),(9,10759),(19,10759),(7,10760),(14,10760),
            (19,10760),(21,10760),(10,10761),(21,10761),(10,10762),(11,10763),(12,10763),
            (13,10763),(14,10763),(15,10763),(16,10763),(17,10763),(18,10763),(19,10763),
            (20,10763),(22,10763),(12,10764),(15,10764),(19,10764),(21,10765),(22,10766)
        ]
        for id_pelicula, id_genero in relaciones_generos:
            peliculas[id_pelicula].generos.append(generos[id_genero])

        db.session.commit()

        print("✅ Datos iniciales cargados.")
    else:
        print("ℹ️ Datos iniciales ya existen, proceso omitido.")

if __name__ == "__main__":
    llenar_datos_iniciales()