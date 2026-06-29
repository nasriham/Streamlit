
-- ============================================================
USE ROLE R_DATA_ING_DEV;
USE DATABASE DB_REFERENTIEL_DEV;
USE SCHEMA S_REFERENTIEL;
-- ============================================================


-- ============================================================
-- SCRIPTS DE CREATION ET D'ALIMENTATION DES TABLES
-- Schema : DB_REFERENTIEL_DEV.S_REFERENTIEL
-- ============================================================

-- 2. CREATION DES TABLES
-- ============================================================


create or replace TABLE DB_REFERENTIEL_DEV.S_REFERENTIEL.T_F_HISTORIQUE_EVENEMENT (
	CODE_EVENEMENT NUMBER(38,0),
	TITRE_EVENEMENT VARCHAR(500),
	TYPE_EVENEMENT VARCHAR(200),
	CATEGORIE VARCHAR(50),
	DESCRIPTION VARCHAR(1000),
	LIEU VARCHAR(200),
	VILLE VARCHAR(100),
	IMPACT VARCHAR(200),
	NIVEAU_SEVERITE NUMBER(38,0),
	DATE_DEBUT TIMESTAMP_NTZ(9),
	DATE_FIN TIMESTAMP_NTZ(9),
	IS_JOURNEE_PARTIELLE BOOLEAN,
	CRENEAU VARCHAR(50),
	NB_PLACES_IMPACTEES NUMBER(38,0),
	FERMETURE_TOTALE BOOLEAN,
	NB_PISTES_ENTREE_FERMEES NUMBER(38,0),
	NB_PISTES_SORTIE_FERMEES NUMBER(38,0),
	TYPE_TRAVAUX VARCHAR(50),
	CONTACT_INTERNE VARCHAR(200),
	CONTACT_EXTERNE VARCHAR(200),
	IS_TRAVAUX_PHASES BOOLEAN,
	COMMENTAIRE VARCHAR(2000),
	PARKINGS_IMPACTES VARCHAR(2000),
	IS_ACTIVE NUMBER(38,0),
	MODIFIE_PAR VARCHAR(100),
	ACTION VARCHAR(50),
	DATE_DEBUT_VALIDITE TIMESTAMP_NTZ(9),
	DATE_FIN_VALIDITE TIMESTAMP_NTZ(9)
);



create or replace TABLE DB_REFERENTIEL_DEV.S_REFERENTIEL.T_F_PHASE_TRAVAUX (
	CODE_PHASE NUMBER(38,0) NOT NULL autoincrement start 1 increment 1 noorder,
	CODE_EVENEMENT NUMBER(38,0) NOT NULL,
	NUMERO_PHASE NUMBER(38,0),
	DATE_DEBUT TIMESTAMP_NTZ(9),
	DATE_FIN TIMESTAMP_NTZ(9),
	NB_PLACES_IMPACTEES NUMBER(38,0),
	COMMENTAIRE VARCHAR(1000),
	primary key (CODE_PHASE)
);



create or replace TABLE DB_REFERENTIEL_DEV.S_REFERENTIEL.T_R_CONTACT_INTERNE (
	CODE_CONTACT NUMBER(38,0) NOT NULL autoincrement start 1 increment 1 noorder,
	NOM VARCHAR(200) NOT NULL,
	EMAIL VARCHAR(200) NOT NULL,
	SERVICE VARCHAR(100),
	IS_ACTIVE BOOLEAN DEFAULT TRUE,
	DATE_CREATION TIMESTAMP_NTZ(9) DEFAULT CURRENT_TIMESTAMP(),
	PRENOM VARCHAR(200),
	primary key (CODE_CONTACT)
);

-- Insertion des contacts
INSERT INTO S_REFERENTIEL.T_R_CONTACT_INTERNE (NOM, PRENOM, EMAIL)
VALUES
('ABENZOAR', 'Magaly', 'mabenzoar@mtpk.fr'),
('ALANIC', 'Christophe', 'calanic@mtpk.fr'),
('ANDREOTTI', 'Nicolas', 'nandreotti@mtpk.fr'),
('ANONKRE', 'Franck', 'fanonkre@mtpk.fr'),
('ASO', 'Jonathan', 'jaso@mtpk.fr'),
('AUDIGEOS', 'Philippe', 'paudigeos@mtpk.fr'),
('AYELLA', 'Elvis', 'eayella@mtpk.fr'),
('BAGUELIN', 'Steven', 'sbaguelin@mtpk.fr'),
('BEDORA', 'Melanie', 'mbedora@mtpk.fr'),
('BELLAZEREG', 'Nasser', 'nbellazereg@mtpk.fr'),
('BENGRID', 'Aymen', 'abengrid@mtpk.fr'),
('BERGEROT', 'Matthieu', 'mbergerot@mtpk.fr'),
('BIRONNEAU', 'Matthias', 'mbironneau@mtpk.fr'),
('BISCARRO', 'Valérie', 'vbiscarro@mtpk.fr'),
('BOISUMEAU', 'Ludovic', 'lboisumeau@mtpk.fr'),
('BORDAS', 'Laurent', 'lbordas@mtpk.fr'),
('BORDIN-MORA', 'Céline', 'cbordinmora@mtpk.fr'),
('BOUARROUJ', 'Nahed', 'nbouarrouj@mtpk.fr'),
('BOUAT', 'Gaëtan', 'gbouat@mtpk.fr'),
('BOUDET', 'David', 'dboudet@mtpk.fr'),
('BOUDJEMA', 'Samir', 'sboudjema@mtpk.fr'),
('BOYANCE', 'Benoît', 'bboyance@mtpk.fr'),
('BREBINAUD', 'Paul', 'pbrebinaud@mtpk.fr'),
('CAMBON', 'Agathe', 'acambon@mtpk.fr'),
('CAR', 'Christophe', 'ccar@mtpk.fr'),
('CHAKOUH', 'Samy', 'schakouh@mtpk.fr'),
('CHALLEMET', 'Alice', 'achallemet@mtpk.fr'),
('CHERKI', 'Abderrafik', 'rcherki@mtpk.fr'),
('CHEVALIER', 'Mickaël', 'mchevalier@mtpk.fr'),
('CHEVALOT', 'Grégory', 'gchevalot@mtpk.fr'),
('COLLET', 'Patricia', 'pcollet@mtpk.fr'),
('COMBRET', 'Gaëtan', 'gcombret@mtpk.fr'),
('CRUZ', 'Cyril', 'ccruz@mtpk.fr'),
('CUING', 'André', 'acuing@mtpk.fr'),
('CURCI', 'Sabine', 'scurci@mtpk.fr'),
('DAUSSOIR TAUZIN', 'Kevin', 'kdaussoirtauzin@mtpk.fr'),
('DEBOURGE', 'Olivier', 'odebourge@mtpk.fr'),
('DECAUDAIN', 'Jean Jacques', 'jdecaudain@mtpk.fr'),
('DELAGE', 'Romain', 'rdelage@mtpk.fr'),
('DELAMARE', 'Hina', 'hdelamare@mtpk.fr'),
('DELPECH', 'Jean Pierre', 'jdelpech@mtpk.fr'),
('DENONAIN', 'Emma', 'edenonain@mtpk.fr'),
('DESNIOU', 'Jérémy', 'jdesniou@mtpk.fr'),
('DEVYLDER', 'Michaël', 'mdevylder@mtpk.fr'),
('DONINEAUX', 'Maxed', 'mdonineaux@mtpk.fr'),
('DOUET', 'Rémi', 'rdouet@mtpk.fr'),
('DRUILLET', 'Julie', 'jdruillet@mtpk.fr'),
('DUPART', 'Nicolas', 'ndupart@mtpk.fr'),
('ENOUS', 'Véronique', 'venous@mtpk.fr'),
('ETCHEGORRY', 'Jessica', 'jetchegorry@mtpk.fr'),
('EZELIN', 'Nicolas', 'nezelin@mtpk.fr'),
('FAIVRE', 'Frédéric', 'ffaivre@mtpk.fr'),
('FAURE', 'Jean-Baptiste', 'jbfaure@mtpk.fr'),
('FERCHAUT', 'Jérémy-William', 'jferchaut@mtpk.fr'),
('FOUCHER', 'Angélique', 'ahautreux@mtpk.fr'),
('FRICOT-DELAPLANCHE', 'Anthony', 'africotdelaplanche@mtpk.fr'),
('GAIDOT', 'Marianne', 'mgaidot@mtpk.fr'),
('GARCIA', 'Guillaume', 'ggarcia@mtpk.fr'),
('GARELLI', 'Fabienne', 'fgarelli@mtpk.fr'),
('GASO', 'Stéphane', 'sgaso@mtpk.fr'),
('GAUDUCHEAU', 'Francis', 'fgauducheau@mtpk.fr'),
('GAUTHIER', 'Virginie', 'vgauthier@mtpk.fr'),
('GOMBEAU', 'Jean-Michel', 'jgombeau@mtpk.fr'),
('GOMEZ', 'Eduardo', 'egomez@mtpk.fr'),
('GOMEZ', 'Jean-Louis', 'jlgomez@mtpk.fr'),
('GRAND', 'Sébastien', 'sgrand@mtpk.fr'),
('GRAS', 'Rémi', 'rgras@mtpk.fr'),
('GRIS', 'Cécile', 'cgris@mtpk.fr'),
('GUILARD', 'Francois', 'fguilard@mtpk.fr'),
('HAMROUNI', 'Ferid', 'fhamrouni@mtpk.fr'),
('HARZALLAH', 'Vincent', 'vharzallah@mtpk.fr'),
('HATINGUAIS', 'Charline', 'chatinguais@mtpk.fr'),
('HERMELIN', 'Benjamin', 'bhermelin@mtpk.fr'),
('HERVAUD', 'Benoît', 'bhervaud@mtpk.fr'),
('HIRIART', 'Charlotte', 'chiriart@mtpk.fr'),
('HOFFMANN', 'Charline', 'choffmann@mtpk.fr'),
('JACQUES', 'Jérémy', 'jjacques@mtpk.fr'),
('JACQUET', 'Cécile', 'cjacquet@mtpk.fr'),
('JORE', 'Aurélien', 'ajore@mtpk.fr'),
('KAMAL-EDINE', 'Adihamou', 'AKAMALEDINE@mtpk.fr'),
('KIRAT', 'Hinde', 'hkirat@mtpk.fr'),
('KRANITZ', 'Linda', 'lkranitz@mtpk.fr'),
('LABARBE', 'Nathalie', 'nlabarbe@mtpk.fr'),
('LABRUE', 'Sébastien', 'slabrue@mtpk.fr'),
('LACHAUD', 'Jean-Marie', 'jmlachaud@mtpk.fr'),
('LACOMBE', 'Mounira', 'mlacombe@mtpk.fr'),
('LACOMBE', 'Bruno', 'blacombe@mtpk.fr'),
('LAFAYE', 'Sylvie', 'slafaye@mtpk.fr'),
('LAPORT', 'Ludovic', 'llaport@mtpk.fr'),
('LARCEBEAU', 'Nicolas', 'nlarcebeau@mtpk.fr'),
('LARRAUX', 'Alexandre', 'alarraux@mtpk.fr'),
('LARTOT-DA LUZ RIJO', 'Frédéric', 'flartot@mtpk.fr'),
('LAVAUD', 'Julien', 'jlavaud@mtpk.fr'),
('LE QUELLEC', 'Gaëtan', 'glequellec@mtpk.fr'),
('LECUROU', 'Chrystelle', 'clecurou@mtpk.fr'),
('LEGRAS', 'Emma', 'elegras@mtpk.fr'),
('LEPARMENTIER', 'Alexandra', 'aleparmentier@mtpk.fr'),
('LEVEQUE', 'Justine', 'jleveque@mtpk.fr'),
('LEVY', 'Roger', 'rlevy@mtpk.fr'),
('LIMA', 'Daniel', 'dlima@mtpk.fr'),
('LOPEZ', 'Franck', 'flopez@mtpk.fr'),
('LORA', 'Guillaume', 'glora@mtpk.fr'),
('LOUREIRO', 'José Manuel', 'jloureiro@mtpk.fr'),
('MAILLE', 'Linda', 'lmaille@mtpk.fr'),
('MARCHAND', 'Nadège', 'nmarchand@mtpk.fr'),
('M''BARI', 'Emmanuel', 'embari@mtpk.fr'),
('MBENG-ONGOUA', 'Richard Wilfried', 'rmbengongoua@mtpk.fr'),
('MBOCK WENDJEL', 'Jacques', 'jmbockwendjel@mtpk.fr'),
('MICHELLET', 'Eva', 'emichellet@mtpk.fr'),
('M''NEMOSYME', 'Enric Paul', 'em''nemosyme@mtpk.fr'),
('MORISCOT', 'Fabrice', 'fmoriscot@mtpk.fr'),
('NADALIÉ', 'Inès', 'inadalie@mtpk.fr'),
('NAKU', 'Mireille', 'manaku@mtpk.fr'),
('NAWROCKI', 'Julien', 'jnawrocki@mtpk.fr'),
('NOWACKI', 'Pascal', 'pnowacki@mtpk.fr'),
('PAUWELS', 'Kévin', 'kpauwels@mtpk.fr'),
('PECOUT', 'Philippe', 'ppecout@mtpk.fr'),
('PELISSIER-HERMITTE', 'Thierry', 'tpelissierhermitte@mtpk.fr'),
('PERRUCHE', 'Céline', 'cperruche@mtpk.fr'),
('PHELIX', 'Thomas', 'tphelix@mtpk.fr'),
('PIERRIS', 'Jean Francois', 'jfpierris@mtpk.fr'),
('PINNA', 'Marc', 'mpinna@mtpk.fr'),
('PINTO', 'Victor', 'vpinto@mtpk.fr'),
('PLANAS', 'Jean Louis', 'jplanas@mtpk.fr'),
('POTHERAT-KOHLER', 'Jean-françois', 'jfpkohler@mtpk.fr'),
('RAHIMI', 'Saïd', 'srahimi@mtpk.fr'),
('RAQUIN', 'Arnaud', 'araquin@mtpk.fr'),
('RASAMIMANANA', 'Arimisa', 'arasamimanana@mtpk.fr'),
('RASOLOFOMANANA', 'Herilala', 'hrasolofomanana@mtpk.fr'),
('RÉMINY', 'Richard', 'rreminy@mtpk.fr'),
('REY', 'Karine', 'krey@mtpk.fr'),
('RIGAUT', 'Cyril', 'crigaut@mtpk.fr'),
('RIOS', 'Sebastien', 'srios@mtpk.fr'),
('RIVIERE', 'Guillaume', 'griviere@mtpk.fr'),
('ROBIN', 'Pierre', 'probin@mtpk.fr'),
('ROTH', 'Yoann', 'yroth@mtpk.fr'),
('SAAIDIA', 'Ridha', 'rsaaidia@mtpk.fr'),
('SABATINI', 'Samuel', 'ssabatini@mtpk.fr'),
('SAIDI', 'Rachid', 'rsaidi@mtpk.fr'),
('SEGUIN', 'Miguel', 'mseguin@mtpk.fr'),
('SERREIR', 'Mohamed', 'mserreir@mtpk.fr'),
('SICOT', 'Bastien', 'bsicot@mtpk.fr'),
('SIMON', 'Yannick', 'ysimon@mtpk.fr'),
('SLANZI', 'Cristiano', 'cslanzi@mtpk.fr'),
('SYLVESTRE', 'Stéphane', 'ssylvestre@mtpk.fr'),
('TARLEY', 'Jérôme', 'jtarley@mtpk.fr'),
('THEZENAS', 'Annaëlle', 'athezenas@mtpk.fr'),
('THIVET', 'Julien', 'jthivet@mtpk.fr'),
('TOURNAT', 'Adrien', 'atournat@mtpk.fr'),
('VECIANA', 'Olivier', 'oveciana@mtpk.fr'),
('VERDIN', 'Christine', 'cverdin@mtpk.fr'),
('VERZEROLI', 'Pascal', 'pverzeroli@mtpk.fr'),
('VICTOR', 'Jérémy', 'jvictor@mtpk.fr'),
('VILLEGER', 'Solenne', 'svilleger@mtpk.fr'),
('WELE', 'Dahirou', 'dwele@mtpk.fr'),
('YAHIAOUI', 'Nathan', 'nyahiaoui@mtpk.fr');


create or replace TABLE DB_REFERENTIEL_DEV.S_REFERENTIEL.T_R_DESCRIPTION_EVENEMENT (
	CODE_DESCRIPTION NUMBER(38,0) NOT NULL,
	LIBELLE_DESCRIPTION VARCHAR(500),
	CODE_TYPE_EVENEMENT NUMBER(38,0),
	IS_ACTIVE BOOLEAN DEFAULT TRUE,
	primary key (CODE_DESCRIPTION)
);

INSERT INTO DB_REFERENTIEL_DEV.S_REFERENTIEL.T_R_DESCRIPTION_EVENEMENT (CODE_DESCRIPTION, CODE_TYPE_EVENEMENT, LIBELLE_DESCRIPTION, IS_ACTIVE)
VALUES
(1, 1, 'Foire aux vins', TRUE),
(2, 1, 'Foire aux plaisirs', TRUE),
(3, 1, 'Foire internationale de Bordeaux', TRUE),
(4, 1, 'Autre', TRUE),
(5, 2, 'Fête du fleuve - édition annuelle', TRUE),
(6, 2, 'Autre', TRUE),
(7, 3, 'Fête de la musique - 21 juin', TRUE),
(8, 3, 'Autre', TRUE),
(9, 4, 'Manifestation syndicale', TRUE),
(10, 4, 'Manifestation étudiante', TRUE),
(11, 4, 'Gilets jaunes', TRUE),
(12, 4, 'Autre', TRUE),
(13, 5, 'Marathon de Bordeaux', TRUE),
(14, 5, 'Semi-marathon', TRUE),
(15, 5, 'Course caritative', TRUE),
(16, 5, 'Autre', TRUE),
(17, 6, 'Carnaval des 2 rives', TRUE),
(18, 6, 'Autre', TRUE),
(19, 7, 'Concert Arkéa Arena', TRUE),
(20, 7, 'Concert Stade Matmut', TRUE),
(21, 7, 'Spectacle place des Quinconces', TRUE),
(22, 7, 'Autre', TRUE),
(23, 8, 'Match Girondins de Bordeaux', TRUE),
(24, 8, 'Match UBB (Rugby)', TRUE),
(25, 8, 'Autre', TRUE),
(26, 9, 'Marché des Capucins', TRUE),
(27, 9, 'Marché de Noël', TRUE),
(28, 9, 'Autre', TRUE),
(29, 10, 'Autre', TRUE),
(30, 11, 'Coupure fibre', TRUE),
(31, 11, 'Panne réseau opérateur', TRUE),
(32, 11, 'Autre', TRUE),
(33, 12, 'Barrière entrée bloquée', TRUE),
(34, 12, 'Barrière sortie bloquée', TRUE),
(35, 12, 'Lecteur badge HS', TRUE),
(36, 12, 'Autre', TRUE),
(37, 13, 'Peinture sol', TRUE),
(38, 13, 'Réfection éclairage', TRUE),
(39, 13, 'Maintenance ascenseur', TRUE),
(40, 13, 'Réparation ventilation', TRUE),
(41, 13, 'Autre', TRUE),
(42, 14, 'Travaux voirie', TRUE),
(43, 14, 'Travaux réseaux (eau/gaz/électricité)', TRUE),
(44, 14, 'Travaux tramway', TRUE),
(45, 14, 'Autre', TRUE),
(46, 15, 'Réservation exceptionnelle', TRUE),
(47, 15, 'Occupation abusive', TRUE),
(48, 15, 'Autre', TRUE),
(49, 16, 'Panne caisse automatique', TRUE),
(50, 16, 'Panne éclairage', TRUE),
(51, 16, 'Panne ventilation', TRUE),
(52, 16, 'Autre', TRUE),
(53, 17, 'Autre', TRUE);


create or replace TABLE DB_REFERENTIEL_DEV.S_REFERENTIEL.T_R_DISTRICT (
	CODE_DISTRICT VARCHAR(10) NOT NULL,
	LIBELLE_DISTRICT VARCHAR(100),
	primary key (CODE_DISTRICT)
);

INSERT INTO DB_REFERENTIEL_DEV.S_REFERENTIEL.T_R_DISTRICT (CODE_DISTRICT, LIBELLE_DISTRICT)
VALUES
(0, 'Non renseigné'),
(1, 'Centre'),
(2, 'Nord'),
(3, 'Sud');



create or replace TABLE DB_REFERENTIEL_DEV.S_REFERENTIEL.T_R_EQUIPEMENT_ACCES (
	CODE_PARC VARCHAR(20) NOT NULL,
	NB_VOIES_ENTREES NUMBER(10,0),
	NB_VOIES_SORTIES NUMBER(10,0),
	NOM_PEAGEUR VARCHAR(100),
	NB_LECTEURS_PIETONS NUMBER(10,0),
	NB_LECTEURS_METSTATIONS NUMBER(10,0),
	NB_CAISSES NUMBER(10,0),
	NB_BORNES_PEAGE_ENTREES NUMBER(10,0),
	FLAG_DOUBLE_ENTREES VARCHAR(10),
	NB_BORNES_PEAGE_SORTIES NUMBER(10,0),
	FLAG_DOUBLE_SORTIES VARCHAR(10),
	FLAG_LECTURE_PLAQUE VARCHAR(10),
	NB_ASCENSEURS NUMBER(10,0),
	MARQUE_ASCENSEURS VARCHAR(100),
	NB_ESCALIERS NUMBER(10,0),
	NB_PORTAILS NUMBER(10,0),
	NB_PORTES_COULISSANTES NUMBER(10,0),
	NB_RIDEAUX_MOTORISES NUMBER(10,0),
	NB_BORNES_IRVE NUMBER(10,0),
	FLAG_GUIDAGE_PLACE VARCHAR(10),
	GABARIT_STANDARD VARCHAR(50),
	DATE_CREATION TIMESTAMP_NTZ(9),
	NOM_CREATEUR VARCHAR(100),
	DATE_MODIFICATION TIMESTAMP_NTZ(9),
	NOM_MODIFICATEUR VARCHAR(100),
	DATE_DEBUT TIMESTAMP_NTZ(9),
	DATE_FIN VARCHAR(20),
	IS_ACTIVE VARCHAR(10),
	DATE_MISE_SERVICE_ASCENSEUR DATE,
	FLAG_LOCKERS VARCHAR(10)
);

create or replace TABLE DB_REFERENTIEL_DEV.S_REFERENTIEL.T_R_FLAG (
	CODE_FLAG VARCHAR(10) NOT NULL,
	LIBELLE_FLAG VARCHAR(100),
	primary key (CODE_FLAG)
);

INSERT INTO DB_REFERENTIEL_DEV.S_REFERENTIEL.T_R_FLAG (CODE_FLAG, LIBELLE_FLAG)
VALUES
(-1, 'Non'),
(0, 'Non renseigné'),
(1, 'Oui');



create or replace TABLE DB_REFERENTIEL_DEV.S_REFERENTIEL.T_R_GESTION (
	CODE_GESTION VARCHAR(10) NOT NULL,
	LIBELLE_GESTION VARCHAR(100),
	primary key (CODE_GESTION)
);

INSERT INTO DB_REFERENTIEL_DEV.S_REFERENTIEL.T_R_GESTION (CODE_GESTION, LIBELLE_GESTION)
VALUES
(0, 'Non renseigné'),
(1, 'Conv (Cinema)'),
(2, 'Conv (clinique)'),
(3, 'Conv (Ehpad)'),
(4, 'Conv (SNCF)'),
(5, 'Conv (Syndic)'),
(6, 'Indigo'),
(7, 'MTPK');


create or replace TABLE DB_REFERENTIEL_DEV.S_REFERENTIEL.T_R_IMPACT_EVENEMENT (
	CODE_IMPACT NUMBER(38,0) NOT NULL,
	LIBELLE_IMPACT VARCHAR(200),
	NIVEAU_SEVERITE NUMBER(38,0),
	IS_ACTIVE BOOLEAN DEFAULT TRUE,
	primary key (CODE_IMPACT)
);

INSERT INTO DB_REFERENTIEL_DEV.S_REFERENTIEL.T_R_IMPACT_EVENEMENT (CODE_IMPACT, LIBELLE_IMPACT, NIVEAU_SEVERITE, IS_ACTIVE)
VALUES
(1, 'Aucun impact notable', 1, TRUE),
(2, 'Ralentissement', 2, TRUE),
(3, 'Surcharge temporaire', 2, TRUE),
(4, 'Accès restreint', 3, TRUE),
(5, 'Déviation imposée', 3, TRUE),
(6, 'Fermeture partielle', 3, TRUE),
(7, 'Blocage total', 4, TRUE);


create or replace TABLE DB_REFERENTIEL_DEV.S_REFERENTIEL.T_R_NATURE_JURIDIQUE (
	CODE_NATURE_JURIDIQUE VARCHAR(10) NOT NULL,
	LIBELLE_NATURE_JURIDIQUE VARCHAR(200),
	primary key (CODE_NATURE_JURIDIQUE)
);

INSERT INTO S_REFERENTIEL.T_R_NATURE_JURIDIQUE (CODE_NATURE_JURIDIQUE, LIBELLE_NATURE_JURIDIQUE)
VALUES
(0, 'Non renseigné'),
(1, 'Convention'),
(2, 'Mise en affectation'),
(3, 'Pleine Propriété');


create or replace TABLE DB_REFERENTIEL_DEV.S_REFERENTIEL.T_R_PARC (
	CODE_PARC VARCHAR(20) NOT NULL,
	NOM_PARC VARCHAR(200),
	ADRESSE_PARC VARCHAR(500),
	CODE_VILLE VARCHAR(10),
	CODE_SECTEUR VARCHAR(10),
	CODE_DISTRICT VARCHAR(10),
	CODE_TYPE_PARC VARCHAR(10),
	CODE_FLAG_FOURRIERE VARCHAR(10),
	CODE_FLAG_METSTATION VARCHAR(10),
	DATE_CREATION TIMESTAMP_NTZ(9),
	NOM_CREATEUR VARCHAR(100),
	DATE_MODIFICATION TIMESTAMP_NTZ(9),
	NOM_MODIFICATEUR VARCHAR(100),
	DATE_DEBUT TIMESTAMP_NTZ(9),
	DATE_FIN VARCHAR(20),
	IS_ACTIVE VARCHAR(10)
);

INSERT INTO T_R_PARC (CODE_PARC, NOM_PARC, ADRESSE_PARC, CODE_VILLE, CODE_SECTEUR, CODE_DISTRICT, CODE_TYPE_PARC, CODE_FLAG_FOURRIERE, CODE_FLAG_METSTATION, DATE_CREATION, NOM_CREATEUR, DATE_MODIFICATION, NOM_MODIFICATEUR, DATE_DEBUT, DATE_FIN, IS_ACTIVE)
VALUES
('H8MAI', '8 Mai 1985', 'Cours Maréchal Juin', '1', '1', '1', '3', '1', '1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('HACHA', 'Allees de Chartres', 'Allées de Bristol', '1', '1', '1', '2', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('HALOR', 'Alsace Lorraine', '21 Cours d''Alsace-Lorraine', '1', '1', '1', '3', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('CAMED', 'Amedee', '3 rue des échoppes', '1', '2', '3', '2', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('CDUNA', 'Amplitude', '35 rue Renée Buthaud', '2', '2', '3', '1', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('PAREN', 'Arena', 'Rue Pierre Kaldor/ avenue Alfonséa', '3', '3', '3', '1', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('CBEAU', 'Beaujon', 'Impasse des Cossus', '1', '2', '2', '1', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('CBERG', 'Bergonie', '220 cours de l''Argonne', '1', '2', '3', '2', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('HBONN', 'Bonnac', '42 Rue du Château d''eau', '1', '1', '1', '3', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('PBORD', 'Bord''Oh', '14 Rue Andrée Putman', '2', '3', '1', '3', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('PBRAZZ', 'Brazza', '202 rue des Queyries Bdx', '1', '3', '1', '2', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('HCAJU', 'Camille Jullian', '2 Pl. Camille Jullian', '1', '1', '1', '3', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('HCCME', 'CC Meriadeck', 'Rue Révérend Père Dieuzaide', '1', '1', '2', '3', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('HCMON', 'Cite Mondiale', '20 Quai des Chartrons', '1', '1', '1', '3', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('CCSEG', 'Croix de Seguey', '33 rue de la croix de Seguey', '1', '2', '2', '2', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('HFDME', 'Front du Medoc', 'Rue Robert Lateulade', '1', '1', '2', '1', '1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('HGAMB', 'Gambetta', 'Rue Edmond Michelet', '1', '1', '2', '3', '-1', '1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('CGSJE', 'Gare Saint Jean', '36 rue Charles Domercq', '1', '2', '3', '3', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('CGPAR', 'Grand Parc', 'Rue du Docteur Finlay', '1', '2', '2', '1', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('HGHOM', 'Grands Hommes', '3 Place des Grands Hommes', '1', '1', '2', '3', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('PLAHA', 'Laharpe', '59 Avenue d''Eysines', '4', '3', '2', '2', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('HLHOT', 'Lhote', '5-7 Rue Lhôte', '1', '1', '2', '3', '-1', '1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('PLIBE', 'Liberation', '43 Avenue de la Libération', '4', '3', '2', '1', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('PMEGA', 'Megarama', 'Allée Serr', '2', '3', '1', '3', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('PMERI', 'Merignac', 'Place Charles de Gaulle', '5', '3', '2', '3', '-1', '1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('CPALU', 'Paludate', 'Quai de Paludate', '1', '2', '3', '1', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('PPESS', 'Pessac', 'Rue des Poilus', '6', '3', '3', '3', '-1', '1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('HPBER', 'Pey Berland', 'Place Pey Berland', '1', '1', '1', '3', '-1', '1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('CPBDX', 'Porte de Bordeaux', '48 rue Général de Larminat', '1', '2', '3', '3', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('HREPU', 'Republique', 'Place de la République', '1', '1', '1', '3', '-1', '1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('CBEGL', 'Rue de Begles', '120 rue de Bègles', '1', '2', '3', '3', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('PSECH', 'Secheries', '13 Allée de Francs', '7', '3', '3', '1', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('PUGC', 'UGC', 'Allée du 7ème art', '8', '3', '3', '3', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('HVICT', 'Victoire', 'Place de la Victoire', '1', '1', '1', '3', '-1', '1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('HVHUG', 'Victor Hugo', 'Place de la Ferme Richemont', '1', '1', '1', '1', '-1', '1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE');



create or replace TABLE DB_REFERENTIEL_DEV.S_REFERENTIEL.T_R_PARC_EXPLOITATION (
	CODE_PARC VARCHAR(20) NOT NULL,
	NB_CAPACITE_VL_DT_THERMIQUE NUMBER(38,0),
	NB_CAPACITE_VL_DT_ELECTRIQUE NUMBER(38,0),
	NB_CAPACITE_VL_DT_PMR NUMBER(38,0),
	NB_CAPACITE_VL_DT_PMR_ELECTRIQUE NUMBER(38,0),
	NB_CAPACITE_VL_DT_MOTO NUMBER(38,0),
	NB_CAPACITE_VL_DT_VELO NUMBER(38,0),
	NB_CAPACITE_VL_DT_AUTRE NUMBER(38,0),
	COMMENTAIRE_AUTRE VARCHAR(500),
	NB_VOIES_ACCES NUMBER(38,0),
	NB_VOIES_SORTIES NUMBER(38,0),
	NB_ASCENCEUR NUMBER(38,0),
	NB_ESCALIER NUMBER(38,0),
	NB_PORTAIL NUMBER(38,0),
	NB_TRAPPE_EVACUATION_MOTORISEE NUMBER(38,0),
	NB_RIDEAUX_MOTORISEE NUMBER(38,0),
	DATE_CREATION TIMESTAMP_NTZ(9),
	NOM_CREATEUR VARCHAR(100),
	DATE_MODIFICATION TIMESTAMP_NTZ(9),
	NOM_MODIFICATEUR VARCHAR(100),
	DATE_DEBUT TIMESTAMP_NTZ(9),
	DATE_FIN VARCHAR(20),
	IS_ACTIVE BOOLEAN,
	NOM_PEAGEUR VARCHAR(100),
	NB_LECTEURS_PIETONS NUMBER(38,0),
	NB_LECTEURS_METSTATIONS NUMBER(38,0),
	NB_CAISSES NUMBER(38,0),
	NB_BORNES_PEAGES_ENTREES NUMBER(38,0),
	FLAG_DOUBLE_ENTREES VARCHAR(10),
	NB_BORNES_PEAGES_SORTIES NUMBER(38,0),
	FLAG_DOUBLE_SORTIES VARCHAR(10),
	FLAG_LECTURE_PLAQUE VARCHAR(10),
	MARQUE_ASCENCEUR VARCHAR(100),
	NB_PORTES_COULISSANTES NUMBER(38,0),
	NB_BORNES_IRVE NUMBER(38,0),
	NB_LOCKERS NUMBER(38,0),
	FLAG_GUIDAGE_PLACE VARCHAR(10),
	GABARIT_STANDARD VARCHAR(100),
	SURFACE NUMBER(38,0),
	DATE_MISE_EN_SERVICE_ASCENCEUR DATE,
	NIVEAU VARCHAR(50),
	NB_CAPACITE_VL NUMBER(10,0),
	NB_CAPACITE_EXPLOITEE NUMBER(10,0),
	NB_CAPACITE_TOTALE NUMBER(10,0)
);

create or replace TABLE DB_REFERENTIEL_DEV.S_REFERENTIEL.T_R_PARC_JURIDIQUE (
	CODE_PARC VARCHAR(20) NOT NULL,
	MISE_EN_SERVICE VARCHAR(50),
	CODE_NATURE_JURIDIQUE VARCHAR(10),
	SIRET VARCHAR(50),
	CODE_FLAG_COPRO VARCHAR(10),
	DATE_CREATION TIMESTAMP_NTZ(9),
	NOM_CREATEUR VARCHAR(100),
	DATE_MODIFICATION TIMESTAMP_NTZ(9),
	NOM_MODIFICATEUR VARCHAR(100),
	DATE_DEBUT TIMESTAMP_NTZ(9),
	DATE_FIN VARCHAR(20),
	IS_ACTIVE BOOLEAN,
	TYPE_CONVENTION VARCHAR(200),
	NOM_TIERS_ATTENANT VARCHAR(200),
	NOM_COPRO VARCHAR(200)
);

create or replace TABLE DB_REFERENTIEL_DEV.S_REFERENTIEL.T_R_PARC_SECURITE_INCENDIE (
	CODE_PARC VARCHAR(20) NOT NULL,
	EAE_SPRINKLEURS VARCHAR(50),
	NB_POSTES NUMBER(38,0),
	NB_TETES NUMBER(38,0),
	NB_EXTINCTEURS_TOTAL NUMBER(38,0),
	NB_BAC_A_SABLE NUMBER(38,0),
	DATE_CREATION TIMESTAMP_NTZ(9),
	NOM_CREATEUR VARCHAR(100),
	DATE_MODIFICATION TIMESTAMP_NTZ(9),
	NOM_MODIFICATEUR VARCHAR(100),
	DATE_DEBUT TIMESTAMP_NTZ(9),
	DATE_FIN VARCHAR(20),
	IS_ACTIVE BOOLEAN,
	FLAG_SSI VARCHAR(10),
	TYPE_SSI VARCHAR(100),
	MARQUE_SSI VARCHAR(100),
	NB_EXTRACTEURS NUMBER(38,0),
	NB_INSUFFLATEURS NUMBER(38,0),
	NB_COLONNES_SECHES NUMBER(38,0),
	NB_BAES NUMBER(38,0),
	TYPE_ALIMENTATION_BAES VARCHAR(100),
	NB_TRAPPE_EVACUATION_MOTORISEE NUMBER(38,0),
	TYPE_TARIFS_ELEC VARCHAR(100),
	FLAG_CELLULES_HT VARCHAR(10),
	FLAG_GROUPE_ELECTROGENE VARCHAR(10),
	CAPACITE_CUVE_FIOUL NUMBER(38,0),
	AVIS_COMMISSION VARCHAR(100),
	DATE_MISE_EN_SERVICE_SSI DATE,
	DATE_DERNIERE_COMMISSION DATE,
	FLAG_TGS VARCHAR(10),
	NB_PORTE_COMPARTIMENTAGE NUMBER(38,0),
	NB_DAI NUMBER(38,0),
	NB_DETECTION_CO_NO NUMBER(38,0)
);

create or replace TABLE DB_REFERENTIEL_DEV.S_REFERENTIEL.T_R_PEAGEUR (
	CODE_PEAGEUR VARCHAR(10) NOT NULL,
	LIBELLE_PEAGEUR VARCHAR(100),
	primary key (CODE_PEAGEUR)
);

INSERT INTO S_REFERENTIEL.T_R_PEAGEUR (CODE_PEAGEUR, LIBELLE_PEAGEUR)
VALUES
(1, 'DESIGNA'),
(2, 'HITACHI'),
(3, 'ORBILITY'),
(4, 'SKIDATA');


create or replace TABLE DB_REFERENTIEL_DEV.S_REFERENTIEL.T_R_SECTEUR (
	CODE_SECTEUR VARCHAR(10) NOT NULL,
	LIBELLE_SECTEUR VARCHAR(100),
	primary key (CODE_SECTEUR)
);


INSERT INTO S_REFERENTIEL.T_R_SECTEUR (CODE_SECTEUR, LIBELLE_SECTEUR)
VALUES
(0, 'Non renseigné'),
(1, 'Hypercentre'),
(2, 'Centre'),
(3, 'Periphérie');


create or replace TABLE DB_REFERENTIEL_DEV.S_REFERENTIEL.T_R_TYPE_EVENEMENT (
	CODE_TYPE_EVENEMENT NUMBER(38,0) NOT NULL,
	LIBELLE_TYPE_EVENEMENT VARCHAR(200) NOT NULL,
	CATEGORIE VARCHAR(100) NOT NULL,
	IS_TRAVAUX BOOLEAN DEFAULT FALSE,
	IS_ACTIVE BOOLEAN DEFAULT TRUE,
	primary key (CODE_TYPE_EVENEMENT)
);


INSERT INTO S_REFERENTIEL.T_R_TYPE_EVENEMENT (CODE_TYPE_EVENEMENT, LIBELLE_TYPE_EVENEMENT, CATEGORIE, IS_TRAVAUX, IS_ACTIVE)
VALUES
(1, 'Foire', 'Externe', FALSE, TRUE),
(2, 'Fête du fleuve', 'Externe', FALSE, TRUE),
(3, 'Fête de la musique', 'Externe', FALSE, TRUE),
(4, 'Manifestation', 'Externe', FALSE, TRUE),
(5, 'Marathon', 'Externe', FALSE, TRUE),
(6, 'Carnaval', 'Externe', FALSE, TRUE),
(7, 'Concert / Spectacle', 'Externe', FALSE, TRUE),
(8, 'Match / Événement sportif', 'Externe', FALSE, TRUE),
(9, 'Marché', 'Externe', FALSE, TRUE),
(10, 'Autre événement externe', 'Externe', FALSE, TRUE),
(11, 'Coupure internet', 'Technique', FALSE, TRUE),
(12, 'Barrière défectueuse', 'Technique', FALSE, TRUE),
(13, 'Travaux internes', 'Technique', TRUE, TRUE),
(14, 'Travaux externes', 'Technique', TRUE, TRUE),
(15, 'Indisponibilité de places', 'Technique', FALSE, TRUE),
(16, 'Panne équipement', 'Technique', FALSE, TRUE),
(17, 'Autre incident technique', 'Technique', FALSE, TRUE),
(18, 'Traveaux externes ville de Bordeaux', 'Technique', FALSE, TRUE);


create or replace TABLE DB_REFERENTIEL_DEV.S_REFERENTIEL.T_R_TYPE_PARC (
	CODE_TYPE_PARC VARCHAR(10) NOT NULL,
	LIBELLE_TYPE_PARC VARCHAR(100),
	primary key (CODE_TYPE_PARC)
);



INSERT INTO DB_REFERENTIEL_DEV.S_REFERENTIEL.T_R_TYPE_PARC (CODE_TYPE_PARC, LIBELLE_TYPE_PARC)
VALUES
(1, 'Infrastructure'),
(2, 'Superstructure'),
(3, 'Exterieur'),
(4, 'Infra et Superstructure');


create or replace TABLE DB_REFERENTIEL_DEV.S_REFERENTIEL.T_R_VILLE (
	CODE_VILLE VARCHAR(10) NOT NULL,
	CODE_POSTAL VARCHAR(10),
	LIBELLE_VILLE VARCHAR(100),
	primary key (CODE_VILLE)
);

INSERT INTO S_REFERENTIEL.T_R_VILLE (CODE_VILLE, CODE_POSTAL, LIBELLE_VILLE)
VALUES
(0, 'NR', 'Non renseigné'),
(1, '33000', 'Bordeaux'),
(2, '33100', 'Bordeaux'),
(3, '33270', 'Floirac'),
(4, '33110', 'Le Bouscat'),
(5, '33700', 'Merignac'),
(6, '33600', 'Pessac'),
(7, '33130', 'Bègles'),
(8, '33400', 'Talence');



-- ============================================================
USE ROLE R_DATA_ING_QUA;
USE DATABASE DB_REFERENTIEL_QUA;
USE SCHEMA S_REFERENTIEL;
-- ============================================================


-- ============================================================
-- SCRIPTS DE CREATION ET D'ALIMENTATION DES TABLES
-- Schema : DB_REFERENTIEL_QUA.S_REFERENTIEL
-- ============================================================

-- 2. CREATION DES TABLES
-- ============================================================



create or replace TABLE T_F_HISTORIQUE_EVENEMENT (
	CODE_EVENEMENT NUMBER(38,0),
	TITRE_EVENEMENT VARCHAR(500),
	TYPE_EVENEMENT VARCHAR(200),
	CATEGORIE VARCHAR(50),
	DESCRIPTION VARCHAR(1000),
	LIEU VARCHAR(200),
	VILLE VARCHAR(100),
	IMPACT VARCHAR(200),
	NIVEAU_SEVERITE NUMBER(38,0),
	DATE_DEBUT TIMESTAMP_NTZ(9),
	DATE_FIN TIMESTAMP_NTZ(9),
	IS_JOURNEE_PARTIELLE BOOLEAN,
	CRENEAU VARCHAR(50),
	NB_PLACES_IMPACTEES NUMBER(38,0),
	FERMETURE_TOTALE BOOLEAN,
	NB_PISTES_ENTREE_FERMEES NUMBER(38,0),
	NB_PISTES_SORTIE_FERMEES NUMBER(38,0),
	TYPE_TRAVAUX VARCHAR(50),
	CONTACT_INTERNE VARCHAR(200),
	CONTACT_EXTERNE VARCHAR(200),
	IS_TRAVAUX_PHASES BOOLEAN,
	COMMENTAIRE VARCHAR(2000),
	PARKINGS_IMPACTES VARCHAR(2000),
	IS_ACTIVE NUMBER(38,0),
	MODIFIE_PAR VARCHAR(100),
	ACTION VARCHAR(50),
	DATE_DEBUT_VALIDITE TIMESTAMP_NTZ(9),
	DATE_FIN_VALIDITE TIMESTAMP_NTZ(9)
);



create or replace TABLE T_F_PHASE_TRAVAUX (
	CODE_PHASE NUMBER(38,0) NOT NULL autoincrement start 1 increment 1 noorder,
	CODE_EVENEMENT NUMBER(38,0) NOT NULL,
	NUMERO_PHASE NUMBER(38,0),
	DATE_DEBUT TIMESTAMP_NTZ(9),
	DATE_FIN TIMESTAMP_NTZ(9),
	NB_PLACES_IMPACTEES NUMBER(38,0),
	COMMENTAIRE VARCHAR(1000),
	primary key (CODE_PHASE)
);



create or replace TABLE T_R_CONTACT_INTERNE (
	CODE_CONTACT NUMBER(38,0) NOT NULL autoincrement start 1 increment 1 noorder,
	NOM VARCHAR(200) NOT NULL,
	EMAIL VARCHAR(200) NOT NULL,
	SERVICE VARCHAR(100),
	IS_ACTIVE BOOLEAN DEFAULT TRUE,
	DATE_CREATION TIMESTAMP_NTZ(9) DEFAULT CURRENT_TIMESTAMP(),
	PRENOM VARCHAR(200),
	primary key (CODE_CONTACT)
);

-- Insertion des contacts
INSERT INTO T_R_CONTACT_INTERNE (NOM, PRENOM, EMAIL)
VALUES
('ABENZOAR', 'Magaly', 'mabenzoar@mtpk.fr'),
('ALANIC', 'Christophe', 'calanic@mtpk.fr'),
('ANDREOTTI', 'Nicolas', 'nandreotti@mtpk.fr'),
('ANONKRE', 'Franck', 'fanonkre@mtpk.fr'),
('ASO', 'Jonathan', 'jaso@mtpk.fr'),
('AUDIGEOS', 'Philippe', 'paudigeos@mtpk.fr'),
('AYELLA', 'Elvis', 'eayella@mtpk.fr'),
('BAGUELIN', 'Steven', 'sbaguelin@mtpk.fr'),
('BEDORA', 'Melanie', 'mbedora@mtpk.fr'),
('BELLAZEREG', 'Nasser', 'nbellazereg@mtpk.fr'),
('BENGRID', 'Aymen', 'abengrid@mtpk.fr'),
('BERGEROT', 'Matthieu', 'mbergerot@mtpk.fr'),
('BIRONNEAU', 'Matthias', 'mbironneau@mtpk.fr'),
('BISCARRO', 'Valérie', 'vbiscarro@mtpk.fr'),
('BOISUMEAU', 'Ludovic', 'lboisumeau@mtpk.fr'),
('BORDAS', 'Laurent', 'lbordas@mtpk.fr'),
('BORDIN-MORA', 'Céline', 'cbordinmora@mtpk.fr'),
('BOUARROUJ', 'Nahed', 'nbouarrouj@mtpk.fr'),
('BOUAT', 'Gaëtan', 'gbouat@mtpk.fr'),
('BOUDET', 'David', 'dboudet@mtpk.fr'),
('BOUDJEMA', 'Samir', 'sboudjema@mtpk.fr'),
('BOYANCE', 'Benoît', 'bboyance@mtpk.fr'),
('BREBINAUD', 'Paul', 'pbrebinaud@mtpk.fr'),
('CAMBON', 'Agathe', 'acambon@mtpk.fr'),
('CAR', 'Christophe', 'ccar@mtpk.fr'),
('CHAKOUH', 'Samy', 'schakouh@mtpk.fr'),
('CHALLEMET', 'Alice', 'achallemet@mtpk.fr'),
('CHERKI', 'Abderrafik', 'rcherki@mtpk.fr'),
('CHEVALIER', 'Mickaël', 'mchevalier@mtpk.fr'),
('CHEVALOT', 'Grégory', 'gchevalot@mtpk.fr'),
('COLLET', 'Patricia', 'pcollet@mtpk.fr'),
('COMBRET', 'Gaëtan', 'gcombret@mtpk.fr'),
('CRUZ', 'Cyril', 'ccruz@mtpk.fr'),
('CUING', 'André', 'acuing@mtpk.fr'),
('CURCI', 'Sabine', 'scurci@mtpk.fr'),
('DAUSSOIR TAUZIN', 'Kevin', 'kdaussoirtauzin@mtpk.fr'),
('DEBOURGE', 'Olivier', 'odebourge@mtpk.fr'),
('DECAUDAIN', 'Jean Jacques', 'jdecaudain@mtpk.fr'),
('DELAGE', 'Romain', 'rdelage@mtpk.fr'),
('DELAMARE', 'Hina', 'hdelamare@mtpk.fr'),
('DELPECH', 'Jean Pierre', 'jdelpech@mtpk.fr'),
('DENONAIN', 'Emma', 'edenonain@mtpk.fr'),
('DESNIOU', 'Jérémy', 'jdesniou@mtpk.fr'),
('DEVYLDER', 'Michaël', 'mdevylder@mtpk.fr'),
('DONINEAUX', 'Maxed', 'mdonineaux@mtpk.fr'),
('DOUET', 'Rémi', 'rdouet@mtpk.fr'),
('DRUILLET', 'Julie', 'jdruillet@mtpk.fr'),
('DUPART', 'Nicolas', 'ndupart@mtpk.fr'),
('ENOUS', 'Véronique', 'venous@mtpk.fr'),
('ETCHEGORRY', 'Jessica', 'jetchegorry@mtpk.fr'),
('EZELIN', 'Nicolas', 'nezelin@mtpk.fr'),
('FAIVRE', 'Frédéric', 'ffaivre@mtpk.fr'),
('FAURE', 'Jean-Baptiste', 'jbfaure@mtpk.fr'),
('FERCHAUT', 'Jérémy-William', 'jferchaut@mtpk.fr'),
('FOUCHER', 'Angélique', 'ahautreux@mtpk.fr'),
('FRICOT-DELAPLANCHE', 'Anthony', 'africotdelaplanche@mtpk.fr'),
('GAIDOT', 'Marianne', 'mgaidot@mtpk.fr'),
('GARCIA', 'Guillaume', 'ggarcia@mtpk.fr'),
('GARELLI', 'Fabienne', 'fgarelli@mtpk.fr'),
('GASO', 'Stéphane', 'sgaso@mtpk.fr'),
('GAUDUCHEAU', 'Francis', 'fgauducheau@mtpk.fr'),
('GAUTHIER', 'Virginie', 'vgauthier@mtpk.fr'),
('GOMBEAU', 'Jean-Michel', 'jgombeau@mtpk.fr'),
('GOMEZ', 'Eduardo', 'egomez@mtpk.fr'),
('GOMEZ', 'Jean-Louis', 'jlgomez@mtpk.fr'),
('GRAND', 'Sébastien', 'sgrand@mtpk.fr'),
('GRAS', 'Rémi', 'rgras@mtpk.fr'),
('GRIS', 'Cécile', 'cgris@mtpk.fr'),
('GUILARD', 'Francois', 'fguilard@mtpk.fr'),
('HAMROUNI', 'Ferid', 'fhamrouni@mtpk.fr'),
('HARZALLAH', 'Vincent', 'vharzallah@mtpk.fr'),
('HATINGUAIS', 'Charline', 'chatinguais@mtpk.fr'),
('HERMELIN', 'Benjamin', 'bhermelin@mtpk.fr'),
('HERVAUD', 'Benoît', 'bhervaud@mtpk.fr'),
('HIRIART', 'Charlotte', 'chiriart@mtpk.fr'),
('HOFFMANN', 'Charline', 'choffmann@mtpk.fr'),
('JACQUES', 'Jérémy', 'jjacques@mtpk.fr'),
('JACQUET', 'Cécile', 'cjacquet@mtpk.fr'),
('JORE', 'Aurélien', 'ajore@mtpk.fr'),
('KAMAL-EDINE', 'Adihamou', 'AKAMALEDINE@mtpk.fr'),
('KIRAT', 'Hinde', 'hkirat@mtpk.fr'),
('KRANITZ', 'Linda', 'lkranitz@mtpk.fr'),
('LABARBE', 'Nathalie', 'nlabarbe@mtpk.fr'),
('LABRUE', 'Sébastien', 'slabrue@mtpk.fr'),
('LACHAUD', 'Jean-Marie', 'jmlachaud@mtpk.fr'),
('LACOMBE', 'Mounira', 'mlacombe@mtpk.fr'),
('LACOMBE', 'Bruno', 'blacombe@mtpk.fr'),
('LAFAYE', 'Sylvie', 'slafaye@mtpk.fr'),
('LAPORT', 'Ludovic', 'llaport@mtpk.fr'),
('LARCEBEAU', 'Nicolas', 'nlarcebeau@mtpk.fr'),
('LARRAUX', 'Alexandre', 'alarraux@mtpk.fr'),
('LARTOT-DA LUZ RIJO', 'Frédéric', 'flartot@mtpk.fr'),
('LAVAUD', 'Julien', 'jlavaud@mtpk.fr'),
('LE QUELLEC', 'Gaëtan', 'glequellec@mtpk.fr'),
('LECUROU', 'Chrystelle', 'clecurou@mtpk.fr'),
('LEGRAS', 'Emma', 'elegras@mtpk.fr'),
('LEPARMENTIER', 'Alexandra', 'aleparmentier@mtpk.fr'),
('LEVEQUE', 'Justine', 'jleveque@mtpk.fr'),
('LEVY', 'Roger', 'rlevy@mtpk.fr'),
('LIMA', 'Daniel', 'dlima@mtpk.fr'),
('LOPEZ', 'Franck', 'flopez@mtpk.fr'),
('LORA', 'Guillaume', 'glora@mtpk.fr'),
('LOUREIRO', 'José Manuel', 'jloureiro@mtpk.fr'),
('MAILLE', 'Linda', 'lmaille@mtpk.fr'),
('MARCHAND', 'Nadège', 'nmarchand@mtpk.fr'),
('M''BARI', 'Emmanuel', 'embari@mtpk.fr'),
('MBENG-ONGOUA', 'Richard Wilfried', 'rmbengongoua@mtpk.fr'),
('MBOCK WENDJEL', 'Jacques', 'jmbockwendjel@mtpk.fr'),
('MICHELLET', 'Eva', 'emichellet@mtpk.fr'),
('M''NEMOSYME', 'Enric Paul', 'em''nemosyme@mtpk.fr'),
('MORISCOT', 'Fabrice', 'fmoriscot@mtpk.fr'),
('NADALIÉ', 'Inès', 'inadalie@mtpk.fr'),
('NAKU', 'Mireille', 'manaku@mtpk.fr'),
('NAWROCKI', 'Julien', 'jnawrocki@mtpk.fr'),
('NOWACKI', 'Pascal', 'pnowacki@mtpk.fr'),
('PAUWELS', 'Kévin', 'kpauwels@mtpk.fr'),
('PECOUT', 'Philippe', 'ppecout@mtpk.fr'),
('PELISSIER-HERMITTE', 'Thierry', 'tpelissierhermitte@mtpk.fr'),
('PERRUCHE', 'Céline', 'cperruche@mtpk.fr'),
('PHELIX', 'Thomas', 'tphelix@mtpk.fr'),
('PIERRIS', 'Jean Francois', 'jfpierris@mtpk.fr'),
('PINNA', 'Marc', 'mpinna@mtpk.fr'),
('PINTO', 'Victor', 'vpinto@mtpk.fr'),
('PLANAS', 'Jean Louis', 'jplanas@mtpk.fr'),
('POTHERAT-KOHLER', 'Jean-françois', 'jfpkohler@mtpk.fr'),
('RAHIMI', 'Saïd', 'srahimi@mtpk.fr'),
('RAQUIN', 'Arnaud', 'araquin@mtpk.fr'),
('RASAMIMANANA', 'Arimisa', 'arasamimanana@mtpk.fr'),
('RASOLOFOMANANA', 'Herilala', 'hrasolofomanana@mtpk.fr'),
('RÉMINY', 'Richard', 'rreminy@mtpk.fr'),
('REY', 'Karine', 'krey@mtpk.fr'),
('RIGAUT', 'Cyril', 'crigaut@mtpk.fr'),
('RIOS', 'Sebastien', 'srios@mtpk.fr'),
('RIVIERE', 'Guillaume', 'griviere@mtpk.fr'),
('ROBIN', 'Pierre', 'probin@mtpk.fr'),
('ROTH', 'Yoann', 'yroth@mtpk.fr'),
('SAAIDIA', 'Ridha', 'rsaaidia@mtpk.fr'),
('SABATINI', 'Samuel', 'ssabatini@mtpk.fr'),
('SAIDI', 'Rachid', 'rsaidi@mtpk.fr'),
('SEGUIN', 'Miguel', 'mseguin@mtpk.fr'),
('SERREIR', 'Mohamed', 'mserreir@mtpk.fr'),
('SICOT', 'Bastien', 'bsicot@mtpk.fr'),
('SIMON', 'Yannick', 'ysimon@mtpk.fr'),
('SLANZI', 'Cristiano', 'cslanzi@mtpk.fr'),
('SYLVESTRE', 'Stéphane', 'ssylvestre@mtpk.fr'),
('TARLEY', 'Jérôme', 'jtarley@mtpk.fr'),
('THEZENAS', 'Annaëlle', 'athezenas@mtpk.fr'),
('THIVET', 'Julien', 'jthivet@mtpk.fr'),
('TOURNAT', 'Adrien', 'atournat@mtpk.fr'),
('VECIANA', 'Olivier', 'oveciana@mtpk.fr'),
('VERDIN', 'Christine', 'cverdin@mtpk.fr'),
('VERZEROLI', 'Pascal', 'pverzeroli@mtpk.fr'),
('VICTOR', 'Jérémy', 'jvictor@mtpk.fr'),
('VILLEGER', 'Solenne', 'svilleger@mtpk.fr'),
('WELE', 'Dahirou', 'dwele@mtpk.fr'),
('YAHIAOUI', 'Nathan', 'nyahiaoui@mtpk.fr');


create or replace TABLE T_R_DESCRIPTION_EVENEMENT (
	CODE_DESCRIPTION NUMBER(38,0) NOT NULL,
	LIBELLE_DESCRIPTION VARCHAR(500),
	CODE_TYPE_EVENEMENT NUMBER(38,0),
	IS_ACTIVE BOOLEAN DEFAULT TRUE,
	primary key (CODE_DESCRIPTION)
);

INSERT INTO T_R_DESCRIPTION_EVENEMENT (CODE_DESCRIPTION, CODE_TYPE_EVENEMENT, LIBELLE_DESCRIPTION, IS_ACTIVE)
VALUES
(1, 1, 'Foire aux vins', TRUE),
(2, 1, 'Foire aux plaisirs', TRUE),
(3, 1, 'Foire internationale de Bordeaux', TRUE),
(4, 1, 'Autre', TRUE),
(5, 2, 'Fête du fleuve - édition annuelle', TRUE),
(6, 2, 'Autre', TRUE),
(7, 3, 'Fête de la musique - 21 juin', TRUE),
(8, 3, 'Autre', TRUE),
(9, 4, 'Manifestation syndicale', TRUE),
(10, 4, 'Manifestation étudiante', TRUE),
(11, 4, 'Gilets jaunes', TRUE),
(12, 4, 'Autre', TRUE),
(13, 5, 'Marathon de Bordeaux', TRUE),
(14, 5, 'Semi-marathon', TRUE),
(15, 5, 'Course caritative', TRUE),
(16, 5, 'Autre', TRUE),
(17, 6, 'Carnaval des 2 rives', TRUE),
(18, 6, 'Autre', TRUE),
(19, 7, 'Concert Arkéa Arena', TRUE),
(20, 7, 'Concert Stade Matmut', TRUE),
(21, 7, 'Spectacle place des Quinconces', TRUE),
(22, 7, 'Autre', TRUE),
(23, 8, 'Match Girondins de Bordeaux', TRUE),
(24, 8, 'Match UBB (Rugby)', TRUE),
(25, 8, 'Autre', TRUE),
(26, 9, 'Marché des Capucins', TRUE),
(27, 9, 'Marché de Noël', TRUE),
(28, 9, 'Autre', TRUE),
(29, 10, 'Autre', TRUE),
(30, 11, 'Coupure fibre', TRUE),
(31, 11, 'Panne réseau opérateur', TRUE),
(32, 11, 'Autre', TRUE),
(33, 12, 'Barrière entrée bloquée', TRUE),
(34, 12, 'Barrière sortie bloquée', TRUE),
(35, 12, 'Lecteur badge HS', TRUE),
(36, 12, 'Autre', TRUE),
(37, 13, 'Peinture sol', TRUE),
(38, 13, 'Réfection éclairage', TRUE),
(39, 13, 'Maintenance ascenseur', TRUE),
(40, 13, 'Réparation ventilation', TRUE),
(41, 13, 'Autre', TRUE),
(42, 14, 'Travaux voirie', TRUE),
(43, 14, 'Travaux réseaux (eau/gaz/électricité)', TRUE),
(44, 14, 'Travaux tramway', TRUE),
(45, 14, 'Autre', TRUE),
(46, 15, 'Réservation exceptionnelle', TRUE),
(47, 15, 'Occupation abusive', TRUE),
(48, 15, 'Autre', TRUE),
(49, 16, 'Panne caisse automatique', TRUE),
(50, 16, 'Panne éclairage', TRUE),
(51, 16, 'Panne ventilation', TRUE),
(52, 16, 'Autre', TRUE),
(53, 17, 'Autre', TRUE);


create or replace TABLE T_R_DISTRICT (
	CODE_DISTRICT VARCHAR(10) NOT NULL,
	LIBELLE_DISTRICT VARCHAR(100),
	primary key (CODE_DISTRICT)
);

INSERT INTO T_R_DISTRICT (CODE_DISTRICT, LIBELLE_DISTRICT)
VALUES
(0, 'Non renseigné'),
(1, 'Centre'),
(2, 'Nord'),
(3, 'Sud');



create or replace TABLE T_R_EQUIPEMENT_ACCES (
	CODE_PARC VARCHAR(20) NOT NULL,
	NB_VOIES_ENTREES NUMBER(10,0),
	NB_VOIES_SORTIES NUMBER(10,0),
	NOM_PEAGEUR VARCHAR(100),
	NB_LECTEURS_PIETONS NUMBER(10,0),
	NB_LECTEURS_METSTATIONS NUMBER(10,0),
	NB_CAISSES NUMBER(10,0),
	NB_BORNES_PEAGE_ENTREES NUMBER(10,0),
	FLAG_DOUBLE_ENTREES VARCHAR(10),
	NB_BORNES_PEAGE_SORTIES NUMBER(10,0),
	FLAG_DOUBLE_SORTIES VARCHAR(10),
	FLAG_LECTURE_PLAQUE VARCHAR(10),
	NB_ASCENSEURS NUMBER(10,0),
	MARQUE_ASCENSEURS VARCHAR(100),
	NB_ESCALIERS NUMBER(10,0),
	NB_PORTAILS NUMBER(10,0),
	NB_PORTES_COULISSANTES NUMBER(10,0),
	NB_RIDEAUX_MOTORISES NUMBER(10,0),
	NB_BORNES_IRVE NUMBER(10,0),
	FLAG_GUIDAGE_PLACE VARCHAR(10),
	GABARIT_STANDARD VARCHAR(50),
	DATE_CREATION TIMESTAMP_NTZ(9),
	NOM_CREATEUR VARCHAR(100),
	DATE_MODIFICATION TIMESTAMP_NTZ(9),
	NOM_MODIFICATEUR VARCHAR(100),
	DATE_DEBUT TIMESTAMP_NTZ(9),
	DATE_FIN VARCHAR(20),
	IS_ACTIVE VARCHAR(10),
	DATE_MISE_SERVICE_ASCENSEUR DATE,
	FLAG_LOCKERS VARCHAR(10)
);

create or replace TABLE T_R_FLAG (
	CODE_FLAG VARCHAR(10) NOT NULL,
	LIBELLE_FLAG VARCHAR(100),
	primary key (CODE_FLAG)
);

INSERT INTO T_R_FLAG (CODE_FLAG, LIBELLE_FLAG)
VALUES
(-1, 'Non'),
(0, 'Non renseigné'),
(1, 'Oui');



create or replace TABLE T_R_GESTION (
	CODE_GESTION VARCHAR(10) NOT NULL,
	LIBELLE_GESTION VARCHAR(100),
	primary key (CODE_GESTION)
);

INSERT INTO T_R_GESTION (CODE_GESTION, LIBELLE_GESTION)
VALUES
(0, 'Non renseigné'),
(1, 'Conv (Cinema)'),
(2, 'Conv (clinique)'),
(3, 'Conv (Ehpad)'),
(4, 'Conv (SNCF)'),
(5, 'Conv (Syndic)'),
(6, 'Indigo'),
(7, 'MTPK');


create or replace TABLE T_R_IMPACT_EVENEMENT (
	CODE_IMPACT NUMBER(38,0) NOT NULL,
	LIBELLE_IMPACT VARCHAR(200),
	NIVEAU_SEVERITE NUMBER(38,0),
	IS_ACTIVE BOOLEAN DEFAULT TRUE,
	primary key (CODE_IMPACT)
);

INSERT INTO T_R_IMPACT_EVENEMENT (CODE_IMPACT, LIBELLE_IMPACT, NIVEAU_SEVERITE, IS_ACTIVE)
VALUES
(1, 'Aucun impact notable', 1, TRUE),
(2, 'Ralentissement', 2, TRUE),
(3, 'Surcharge temporaire', 2, TRUE),
(4, 'Accès restreint', 3, TRUE),
(5, 'Déviation imposée', 3, TRUE),
(6, 'Fermeture partielle', 3, TRUE),
(7, 'Blocage total', 4, TRUE);


create or replace TABLE T_R_NATURE_JURIDIQUE (
	CODE_NATURE_JURIDIQUE VARCHAR(10) NOT NULL,
	LIBELLE_NATURE_JURIDIQUE VARCHAR(200),
	primary key (CODE_NATURE_JURIDIQUE)
);

INSERT INTO T_R_NATURE_JURIDIQUE (CODE_NATURE_JURIDIQUE, LIBELLE_NATURE_JURIDIQUE)
VALUES
(0, 'Non renseigné'),
(1, 'Convention'),
(2, 'Mise en affectation'),
(3, 'Pleine Propriété');


create or replace TABLE T_R_PARC (
	CODE_PARC VARCHAR(20) NOT NULL,
	NOM_PARC VARCHAR(200),
	ADRESSE_PARC VARCHAR(500),
	CODE_VILLE VARCHAR(10),
	CODE_SECTEUR VARCHAR(10),
	CODE_DISTRICT VARCHAR(10),
	CODE_TYPE_PARC VARCHAR(10),
	CODE_FLAG_FOURRIERE VARCHAR(10),
	CODE_FLAG_METSTATION VARCHAR(10),
	DATE_CREATION TIMESTAMP_NTZ(9),
	NOM_CREATEUR VARCHAR(100),
	DATE_MODIFICATION TIMESTAMP_NTZ(9),
	NOM_MODIFICATEUR VARCHAR(100),
	DATE_DEBUT TIMESTAMP_NTZ(9),
	DATE_FIN VARCHAR(20),
	IS_ACTIVE VARCHAR(10)
);

INSERT INTO T_R_PARC (CODE_PARC, NOM_PARC, ADRESSE_PARC, CODE_VILLE, CODE_SECTEUR, CODE_DISTRICT, CODE_TYPE_PARC, CODE_FLAG_FOURRIERE, CODE_FLAG_METSTATION, DATE_CREATION, NOM_CREATEUR, DATE_MODIFICATION, NOM_MODIFICATEUR, DATE_DEBUT, DATE_FIN, IS_ACTIVE)
VALUES
('H8MAI', '8 Mai 1985', 'Cours Maréchal Juin', '1', '1', '1', '3', '1', '1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('HACHA', 'Allees de Chartres', 'Allées de Bristol', '1', '1', '1', '2', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('HALOR', 'Alsace Lorraine', '21 Cours d''Alsace-Lorraine', '1', '1', '1', '3', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('CAMED', 'Amedee', '3 rue des échoppes', '1', '2', '3', '2', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('CDUNA', 'Amplitude', '35 rue Renée Buthaud', '2', '2', '3', '1', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('PAREN', 'Arena', 'Rue Pierre Kaldor/ avenue Alfonséa', '3', '3', '3', '1', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('CBEAU', 'Beaujon', 'Impasse des Cossus', '1', '2', '2', '1', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('CBERG', 'Bergonie', '220 cours de l''Argonne', '1', '2', '3', '2', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('HBONN', 'Bonnac', '42 Rue du Château d''eau', '1', '1', '1', '3', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('PBORD', 'Bord''Oh', '14 Rue Andrée Putman', '2', '3', '1', '3', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('PBRAZZ', 'Brazza', '202 rue des Queyries Bdx', '1', '3', '1', '2', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('HCAJU', 'Camille Jullian', '2 Pl. Camille Jullian', '1', '1', '1', '3', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('HCCME', 'CC Meriadeck', 'Rue Révérend Père Dieuzaide', '1', '1', '2', '3', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('HCMON', 'Cite Mondiale', '20 Quai des Chartrons', '1', '1', '1', '3', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('CCSEG', 'Croix de Seguey', '33 rue de la croix de Seguey', '1', '2', '2', '2', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('HFDME', 'Front du Medoc', 'Rue Robert Lateulade', '1', '1', '2', '1', '1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('HGAMB', 'Gambetta', 'Rue Edmond Michelet', '1', '1', '2', '3', '-1', '1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('CGSJE', 'Gare Saint Jean', '36 rue Charles Domercq', '1', '2', '3', '3', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('CGPAR', 'Grand Parc', 'Rue du Docteur Finlay', '1', '2', '2', '1', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('HGHOM', 'Grands Hommes', '3 Place des Grands Hommes', '1', '1', '2', '3', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('PLAHA', 'Laharpe', '59 Avenue d''Eysines', '4', '3', '2', '2', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('HLHOT', 'Lhote', '5-7 Rue Lhôte', '1', '1', '2', '3', '-1', '1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('PLIBE', 'Liberation', '43 Avenue de la Libération', '4', '3', '2', '1', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('PMEGA', 'Megarama', 'Allée Serr', '2', '3', '1', '3', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('PMERI', 'Merignac', 'Place Charles de Gaulle', '5', '3', '2', '3', '-1', '1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('CPALU', 'Paludate', 'Quai de Paludate', '1', '2', '3', '1', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('PPESS', 'Pessac', 'Rue des Poilus', '6', '3', '3', '3', '-1', '1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('HPBER', 'Pey Berland', 'Place Pey Berland', '1', '1', '1', '3', '-1', '1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('CPBDX', 'Porte de Bordeaux', '48 rue Général de Larminat', '1', '2', '3', '3', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('HREPU', 'Republique', 'Place de la République', '1', '1', '1', '3', '-1', '1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('CBEGL', 'Rue de Begles', '120 rue de Bègles', '1', '2', '3', '3', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('PSECH', 'Secheries', '13 Allée de Francs', '7', '3', '3', '1', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('PUGC', 'UGC', 'Allée du 7ème art', '8', '3', '3', '3', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('HVICT', 'Victoire', 'Place de la Victoire', '1', '1', '1', '3', '-1', '1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('HVHUG', 'Victor Hugo', 'Place de la Ferme Richemont', '1', '1', '1', '1', '-1', '1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE');



create or replace TABLE T_R_PARC_EXPLOITATION (
	CODE_PARC VARCHAR(20) NOT NULL,
	NB_CAPACITE_VL_DT_THERMIQUE NUMBER(38,0),
	NB_CAPACITE_VL_DT_ELECTRIQUE NUMBER(38,0),
	NB_CAPACITE_VL_DT_PMR NUMBER(38,0),
	NB_CAPACITE_VL_DT_PMR_ELECTRIQUE NUMBER(38,0),
	NB_CAPACITE_VL_DT_MOTO NUMBER(38,0),
	NB_CAPACITE_VL_DT_VELO NUMBER(38,0),
	NB_CAPACITE_VL_DT_AUTRE NUMBER(38,0),
	COMMENTAIRE_AUTRE VARCHAR(500),
	NB_VOIES_ACCES NUMBER(38,0),
	NB_VOIES_SORTIES NUMBER(38,0),
	NB_ASCENCEUR NUMBER(38,0),
	NB_ESCALIER NUMBER(38,0),
	NB_PORTAIL NUMBER(38,0),
	NB_TRAPPE_EVACUATION_MOTORISEE NUMBER(38,0),
	NB_RIDEAUX_MOTORISEE NUMBER(38,0),
	DATE_CREATION TIMESTAMP_NTZ(9),
	NOM_CREATEUR VARCHAR(100),
	DATE_MODIFICATION TIMESTAMP_NTZ(9),
	NOM_MODIFICATEUR VARCHAR(100),
	DATE_DEBUT TIMESTAMP_NTZ(9),
	DATE_FIN VARCHAR(20),
	IS_ACTIVE BOOLEAN,
	NOM_PEAGEUR VARCHAR(100),
	NB_LECTEURS_PIETONS NUMBER(38,0),
	NB_LECTEURS_METSTATIONS NUMBER(38,0),
	NB_CAISSES NUMBER(38,0),
	NB_BORNES_PEAGES_ENTREES NUMBER(38,0),
	FLAG_DOUBLE_ENTREES VARCHAR(10),
	NB_BORNES_PEAGES_SORTIES NUMBER(38,0),
	FLAG_DOUBLE_SORTIES VARCHAR(10),
	FLAG_LECTURE_PLAQUE VARCHAR(10),
	MARQUE_ASCENCEUR VARCHAR(100),
	NB_PORTES_COULISSANTES NUMBER(38,0),
	NB_BORNES_IRVE NUMBER(38,0),
	NB_LOCKERS NUMBER(38,0),
	FLAG_GUIDAGE_PLACE VARCHAR(10),
	GABARIT_STANDARD VARCHAR(100),
	SURFACE NUMBER(38,0),
	DATE_MISE_EN_SERVICE_ASCENCEUR DATE,
	NIVEAU VARCHAR(50),
	NB_CAPACITE_VL NUMBER(10,0),
	NB_CAPACITE_EXPLOITEE NUMBER(10,0),
	NB_CAPACITE_TOTALE NUMBER(10,0)
);

create or replace TABLE T_R_PARC_JURIDIQUE (
	CODE_PARC VARCHAR(20) NOT NULL,
	MISE_EN_SERVICE VARCHAR(50),
	CODE_NATURE_JURIDIQUE VARCHAR(10),
	SIRET VARCHAR(50),
	CODE_FLAG_COPRO VARCHAR(10),
	DATE_CREATION TIMESTAMP_NTZ(9),
	NOM_CREATEUR VARCHAR(100),
	DATE_MODIFICATION TIMESTAMP_NTZ(9),
	NOM_MODIFICATEUR VARCHAR(100),
	DATE_DEBUT TIMESTAMP_NTZ(9),
	DATE_FIN VARCHAR(20),
	IS_ACTIVE BOOLEAN,
	TYPE_CONVENTION VARCHAR(200),
	NOM_TIERS_ATTENANT VARCHAR(200),
	NOM_COPRO VARCHAR(200)
);

create or replace TABLE T_R_PARC_SECURITE_INCENDIE (
	CODE_PARC VARCHAR(20) NOT NULL,
	EAE_SPRINKLEURS VARCHAR(50),
	NB_POSTES NUMBER(38,0),
	NB_TETES NUMBER(38,0),
	NB_EXTINCTEURS_TOTAL NUMBER(38,0),
	NB_BAC_A_SABLE NUMBER(38,0),
	DATE_CREATION TIMESTAMP_NTZ(9),
	NOM_CREATEUR VARCHAR(100),
	DATE_MODIFICATION TIMESTAMP_NTZ(9),
	NOM_MODIFICATEUR VARCHAR(100),
	DATE_DEBUT TIMESTAMP_NTZ(9),
	DATE_FIN VARCHAR(20),
	IS_ACTIVE BOOLEAN,
	FLAG_SSI VARCHAR(10),
	TYPE_SSI VARCHAR(100),
	MARQUE_SSI VARCHAR(100),
	NB_EXTRACTEURS NUMBER(38,0),
	NB_INSUFFLATEURS NUMBER(38,0),
	NB_COLONNES_SECHES NUMBER(38,0),
	NB_BAES NUMBER(38,0),
	TYPE_ALIMENTATION_BAES VARCHAR(100),
	NB_TRAPPE_EVACUATION_MOTORISEE NUMBER(38,0),
	TYPE_TARIFS_ELEC VARCHAR(100),
	FLAG_CELLULES_HT VARCHAR(10),
	FLAG_GROUPE_ELECTROGENE VARCHAR(10),
	CAPACITE_CUVE_FIOUL NUMBER(38,0),
	AVIS_COMMISSION VARCHAR(100),
	DATE_MISE_EN_SERVICE_SSI DATE,
	DATE_DERNIERE_COMMISSION DATE,
	FLAG_TGS VARCHAR(10),
	NB_PORTE_COMPARTIMENTAGE NUMBER(38,0),
	NB_DAI NUMBER(38,0),
	NB_DETECTION_CO_NO NUMBER(38,0)
);

create or replace TABLE T_R_PEAGEUR (
	CODE_PEAGEUR VARCHAR(10) NOT NULL,
	LIBELLE_PEAGEUR VARCHAR(100),
	primary key (CODE_PEAGEUR)
);

INSERT INTO T_R_PEAGEUR (CODE_PEAGEUR, LIBELLE_PEAGEUR)
VALUES
(1, 'DESIGNA'),
(2, 'HITACHI'),
(3, 'ORBILITY'),
(4, 'SKIDATA');


create or replace TABLE T_R_SECTEUR (
	CODE_SECTEUR VARCHAR(10) NOT NULL,
	LIBELLE_SECTEUR VARCHAR(100),
	primary key (CODE_SECTEUR)
);


INSERT INTO T_R_SECTEUR (CODE_SECTEUR, LIBELLE_SECTEUR)
VALUES
(0, 'Non renseigné'),
(1, 'Hypercentre'),
(2, 'Centre'),
(3, 'Periphérie');


create or replace TABLE T_R_TYPE_EVENEMENT (
	CODE_TYPE_EVENEMENT NUMBER(38,0) NOT NULL,
	LIBELLE_TYPE_EVENEMENT VARCHAR(200) NOT NULL,
	CATEGORIE VARCHAR(100) NOT NULL,
	IS_TRAVAUX BOOLEAN DEFAULT FALSE,
	IS_ACTIVE BOOLEAN DEFAULT TRUE,
	primary key (CODE_TYPE_EVENEMENT)
);


INSERT INTO T_R_TYPE_EVENEMENT (CODE_TYPE_EVENEMENT, LIBELLE_TYPE_EVENEMENT, CATEGORIE, IS_TRAVAUX, IS_ACTIVE)
VALUES
(1, 'Foire', 'Externe', FALSE, TRUE),
(2, 'Fête du fleuve', 'Externe', FALSE, TRUE),
(3, 'Fête de la musique', 'Externe', FALSE, TRUE),
(4, 'Manifestation', 'Externe', FALSE, TRUE),
(5, 'Marathon', 'Externe', FALSE, TRUE),
(6, 'Carnaval', 'Externe', FALSE, TRUE),
(7, 'Concert / Spectacle', 'Externe', FALSE, TRUE),
(8, 'Match / Événement sportif', 'Externe', FALSE, TRUE),
(9, 'Marché', 'Externe', FALSE, TRUE),
(10, 'Autre événement externe', 'Externe', FALSE, TRUE),
(11, 'Coupure internet', 'Technique', FALSE, TRUE),
(12, 'Barrière défectueuse', 'Technique', FALSE, TRUE),
(13, 'Travaux internes', 'Technique', TRUE, TRUE),
(14, 'Travaux externes', 'Technique', TRUE, TRUE),
(15, 'Indisponibilité de places', 'Technique', FALSE, TRUE),
(16, 'Panne équipement', 'Technique', FALSE, TRUE),
(17, 'Autre incident technique', 'Technique', FALSE, TRUE),
(18, 'Traveaux externes ville de Bordeaux', 'Technique', FALSE, TRUE);


create or replace TABLE T_R_TYPE_PARC (
	CODE_TYPE_PARC VARCHAR(10) NOT NULL,
	LIBELLE_TYPE_PARC VARCHAR(100),
	primary key (CODE_TYPE_PARC)
);



INSERT INTO T_R_TYPE_PARC (CODE_TYPE_PARC, LIBELLE_TYPE_PARC)
VALUES
(1, 'Infrastructure'),
(2, 'Superstructure'),
(3, 'Exterieur'),
(4, 'Infra et Superstructure');


create or replace TABLE T_R_VILLE (
	CODE_VILLE VARCHAR(10) NOT NULL,
	CODE_POSTAL VARCHAR(10),
	LIBELLE_VILLE VARCHAR(100),
	primary key (CODE_VILLE)
);

INSERT INTO T_R_VILLE (CODE_VILLE, CODE_POSTAL, LIBELLE_VILLE)
VALUES
(0, 'NR', 'Non renseigné'),
(1, '33000', 'Bordeaux'),
(2, '33100', 'Bordeaux'),
(3, '33270', 'Floirac'),
(4, '33110', 'Le Bouscat'),
(5, '33700', 'Merignac'),
(6, '33600', 'Pessac'),
(7, '33130', 'Bègles'),
(8, '33400', 'Talence');


-- ============================================================
USE ROLE R_DATA_ING_PPD;
USE DATABASE DB_REFERENTIEL_PPD;
USE SCHEMA S_REFERENTIEL;
-- ============================================================


-- ============================================================
-- SCRIPTS DE CREATION ET D'ALIMENTATION DES TABLES
-- Schema : DB_REFERENTIEL_PPD.S_REFERENTIEL
-- ============================================================

-- 2. CREATION DES TABLES
-- ============================================================


create or replace TABLE T_F_HISTORIQUE_EVENEMENT (
	CODE_EVENEMENT NUMBER(38,0),
	TITRE_EVENEMENT VARCHAR(500),
	TYPE_EVENEMENT VARCHAR(200),
	CATEGORIE VARCHAR(50),
	DESCRIPTION VARCHAR(1000),
	LIEU VARCHAR(200),
	VILLE VARCHAR(100),
	IMPACT VARCHAR(200),
	NIVEAU_SEVERITE NUMBER(38,0),
	DATE_DEBUT TIMESTAMP_NTZ(9),
	DATE_FIN TIMESTAMP_NTZ(9),
	IS_JOURNEE_PARTIELLE BOOLEAN,
	CRENEAU VARCHAR(50),
	NB_PLACES_IMPACTEES NUMBER(38,0),
	FERMETURE_TOTALE BOOLEAN,
	NB_PISTES_ENTREE_FERMEES NUMBER(38,0),
	NB_PISTES_SORTIE_FERMEES NUMBER(38,0),
	TYPE_TRAVAUX VARCHAR(50),
	CONTACT_INTERNE VARCHAR(200),
	CONTACT_EXTERNE VARCHAR(200),
	IS_TRAVAUX_PHASES BOOLEAN,
	COMMENTAIRE VARCHAR(2000),
	PARKINGS_IMPACTES VARCHAR(2000),
	IS_ACTIVE NUMBER(38,0),
	MODIFIE_PAR VARCHAR(100),
	ACTION VARCHAR(50),
	DATE_DEBUT_VALIDITE TIMESTAMP_NTZ(9),
	DATE_FIN_VALIDITE TIMESTAMP_NTZ(9)
);



create or replace TABLE T_F_PHASE_TRAVAUX (
	CODE_PHASE NUMBER(38,0) NOT NULL autoincrement start 1 increment 1 noorder,
	CODE_EVENEMENT NUMBER(38,0) NOT NULL,
	NUMERO_PHASE NUMBER(38,0),
	DATE_DEBUT TIMESTAMP_NTZ(9),
	DATE_FIN TIMESTAMP_NTZ(9),
	NB_PLACES_IMPACTEES NUMBER(38,0),
	COMMENTAIRE VARCHAR(1000),
	primary key (CODE_PHASE)
);



create or replace TABLE T_R_CONTACT_INTERNE (
	CODE_CONTACT NUMBER(38,0) NOT NULL autoincrement start 1 increment 1 noorder,
	NOM VARCHAR(200) NOT NULL,
	EMAIL VARCHAR(200) NOT NULL,
	SERVICE VARCHAR(100),
	IS_ACTIVE BOOLEAN DEFAULT TRUE,
	DATE_CREATION TIMESTAMP_NTZ(9) DEFAULT CURRENT_TIMESTAMP(),
	PRENOM VARCHAR(200),
	primary key (CODE_CONTACT)
);

-- Insertion des contacts
INSERT INTO T_R_CONTACT_INTERNE (NOM, PRENOM, EMAIL)
VALUES
('ABENZOAR', 'Magaly', 'mabenzoar@mtpk.fr'),
('ALANIC', 'Christophe', 'calanic@mtpk.fr'),
('ANDREOTTI', 'Nicolas', 'nandreotti@mtpk.fr'),
('ANONKRE', 'Franck', 'fanonkre@mtpk.fr'),
('ASO', 'Jonathan', 'jaso@mtpk.fr'),
('AUDIGEOS', 'Philippe', 'paudigeos@mtpk.fr'),
('AYELLA', 'Elvis', 'eayella@mtpk.fr'),
('BAGUELIN', 'Steven', 'sbaguelin@mtpk.fr'),
('BEDORA', 'Melanie', 'mbedora@mtpk.fr'),
('BELLAZEREG', 'Nasser', 'nbellazereg@mtpk.fr'),
('BENGRID', 'Aymen', 'abengrid@mtpk.fr'),
('BERGEROT', 'Matthieu', 'mbergerot@mtpk.fr'),
('BIRONNEAU', 'Matthias', 'mbironneau@mtpk.fr'),
('BISCARRO', 'Valérie', 'vbiscarro@mtpk.fr'),
('BOISUMEAU', 'Ludovic', 'lboisumeau@mtpk.fr'),
('BORDAS', 'Laurent', 'lbordas@mtpk.fr'),
('BORDIN-MORA', 'Céline', 'cbordinmora@mtpk.fr'),
('BOUARROUJ', 'Nahed', 'nbouarrouj@mtpk.fr'),
('BOUAT', 'Gaëtan', 'gbouat@mtpk.fr'),
('BOUDET', 'David', 'dboudet@mtpk.fr'),
('BOUDJEMA', 'Samir', 'sboudjema@mtpk.fr'),
('BOYANCE', 'Benoît', 'bboyance@mtpk.fr'),
('BREBINAUD', 'Paul', 'pbrebinaud@mtpk.fr'),
('CAMBON', 'Agathe', 'acambon@mtpk.fr'),
('CAR', 'Christophe', 'ccar@mtpk.fr'),
('CHAKOUH', 'Samy', 'schakouh@mtpk.fr'),
('CHALLEMET', 'Alice', 'achallemet@mtpk.fr'),
('CHERKI', 'Abderrafik', 'rcherki@mtpk.fr'),
('CHEVALIER', 'Mickaël', 'mchevalier@mtpk.fr'),
('CHEVALOT', 'Grégory', 'gchevalot@mtpk.fr'),
('COLLET', 'Patricia', 'pcollet@mtpk.fr'),
('COMBRET', 'Gaëtan', 'gcombret@mtpk.fr'),
('CRUZ', 'Cyril', 'ccruz@mtpk.fr'),
('CUING', 'André', 'acuing@mtpk.fr'),
('CURCI', 'Sabine', 'scurci@mtpk.fr'),
('DAUSSOIR TAUZIN', 'Kevin', 'kdaussoirtauzin@mtpk.fr'),
('DEBOURGE', 'Olivier', 'odebourge@mtpk.fr'),
('DECAUDAIN', 'Jean Jacques', 'jdecaudain@mtpk.fr'),
('DELAGE', 'Romain', 'rdelage@mtpk.fr'),
('DELAMARE', 'Hina', 'hdelamare@mtpk.fr'),
('DELPECH', 'Jean Pierre', 'jdelpech@mtpk.fr'),
('DENONAIN', 'Emma', 'edenonain@mtpk.fr'),
('DESNIOU', 'Jérémy', 'jdesniou@mtpk.fr'),
('DEVYLDER', 'Michaël', 'mdevylder@mtpk.fr'),
('DONINEAUX', 'Maxed', 'mdonineaux@mtpk.fr'),
('DOUET', 'Rémi', 'rdouet@mtpk.fr'),
('DRUILLET', 'Julie', 'jdruillet@mtpk.fr'),
('DUPART', 'Nicolas', 'ndupart@mtpk.fr'),
('ENOUS', 'Véronique', 'venous@mtpk.fr'),
('ETCHEGORRY', 'Jessica', 'jetchegorry@mtpk.fr'),
('EZELIN', 'Nicolas', 'nezelin@mtpk.fr'),
('FAIVRE', 'Frédéric', 'ffaivre@mtpk.fr'),
('FAURE', 'Jean-Baptiste', 'jbfaure@mtpk.fr'),
('FERCHAUT', 'Jérémy-William', 'jferchaut@mtpk.fr'),
('FOUCHER', 'Angélique', 'ahautreux@mtpk.fr'),
('FRICOT-DELAPLANCHE', 'Anthony', 'africotdelaplanche@mtpk.fr'),
('GAIDOT', 'Marianne', 'mgaidot@mtpk.fr'),
('GARCIA', 'Guillaume', 'ggarcia@mtpk.fr'),
('GARELLI', 'Fabienne', 'fgarelli@mtpk.fr'),
('GASO', 'Stéphane', 'sgaso@mtpk.fr'),
('GAUDUCHEAU', 'Francis', 'fgauducheau@mtpk.fr'),
('GAUTHIER', 'Virginie', 'vgauthier@mtpk.fr'),
('GOMBEAU', 'Jean-Michel', 'jgombeau@mtpk.fr'),
('GOMEZ', 'Eduardo', 'egomez@mtpk.fr'),
('GOMEZ', 'Jean-Louis', 'jlgomez@mtpk.fr'),
('GRAND', 'Sébastien', 'sgrand@mtpk.fr'),
('GRAS', 'Rémi', 'rgras@mtpk.fr'),
('GRIS', 'Cécile', 'cgris@mtpk.fr'),
('GUILARD', 'Francois', 'fguilard@mtpk.fr'),
('HAMROUNI', 'Ferid', 'fhamrouni@mtpk.fr'),
('HARZALLAH', 'Vincent', 'vharzallah@mtpk.fr'),
('HATINGUAIS', 'Charline', 'chatinguais@mtpk.fr'),
('HERMELIN', 'Benjamin', 'bhermelin@mtpk.fr'),
('HERVAUD', 'Benoît', 'bhervaud@mtpk.fr'),
('HIRIART', 'Charlotte', 'chiriart@mtpk.fr'),
('HOFFMANN', 'Charline', 'choffmann@mtpk.fr'),
('JACQUES', 'Jérémy', 'jjacques@mtpk.fr'),
('JACQUET', 'Cécile', 'cjacquet@mtpk.fr'),
('JORE', 'Aurélien', 'ajore@mtpk.fr'),
('KAMAL-EDINE', 'Adihamou', 'AKAMALEDINE@mtpk.fr'),
('KIRAT', 'Hinde', 'hkirat@mtpk.fr'),
('KRANITZ', 'Linda', 'lkranitz@mtpk.fr'),
('LABARBE', 'Nathalie', 'nlabarbe@mtpk.fr'),
('LABRUE', 'Sébastien', 'slabrue@mtpk.fr'),
('LACHAUD', 'Jean-Marie', 'jmlachaud@mtpk.fr'),
('LACOMBE', 'Mounira', 'mlacombe@mtpk.fr'),
('LACOMBE', 'Bruno', 'blacombe@mtpk.fr'),
('LAFAYE', 'Sylvie', 'slafaye@mtpk.fr'),
('LAPORT', 'Ludovic', 'llaport@mtpk.fr'),
('LARCEBEAU', 'Nicolas', 'nlarcebeau@mtpk.fr'),
('LARRAUX', 'Alexandre', 'alarraux@mtpk.fr'),
('LARTOT-DA LUZ RIJO', 'Frédéric', 'flartot@mtpk.fr'),
('LAVAUD', 'Julien', 'jlavaud@mtpk.fr'),
('LE QUELLEC', 'Gaëtan', 'glequellec@mtpk.fr'),
('LECUROU', 'Chrystelle', 'clecurou@mtpk.fr'),
('LEGRAS', 'Emma', 'elegras@mtpk.fr'),
('LEPARMENTIER', 'Alexandra', 'aleparmentier@mtpk.fr'),
('LEVEQUE', 'Justine', 'jleveque@mtpk.fr'),
('LEVY', 'Roger', 'rlevy@mtpk.fr'),
('LIMA', 'Daniel', 'dlima@mtpk.fr'),
('LOPEZ', 'Franck', 'flopez@mtpk.fr'),
('LORA', 'Guillaume', 'glora@mtpk.fr'),
('LOUREIRO', 'José Manuel', 'jloureiro@mtpk.fr'),
('MAILLE', 'Linda', 'lmaille@mtpk.fr'),
('MARCHAND', 'Nadège', 'nmarchand@mtpk.fr'),
('M''BARI', 'Emmanuel', 'embari@mtpk.fr'),
('MBENG-ONGOUA', 'Richard Wilfried', 'rmbengongoua@mtpk.fr'),
('MBOCK WENDJEL', 'Jacques', 'jmbockwendjel@mtpk.fr'),
('MICHELLET', 'Eva', 'emichellet@mtpk.fr'),
('M''NEMOSYME', 'Enric Paul', 'em''nemosyme@mtpk.fr'),
('MORISCOT', 'Fabrice', 'fmoriscot@mtpk.fr'),
('NADALIÉ', 'Inès', 'inadalie@mtpk.fr'),
('NAKU', 'Mireille', 'manaku@mtpk.fr'),
('NAWROCKI', 'Julien', 'jnawrocki@mtpk.fr'),
('NOWACKI', 'Pascal', 'pnowacki@mtpk.fr'),
('PAUWELS', 'Kévin', 'kpauwels@mtpk.fr'),
('PECOUT', 'Philippe', 'ppecout@mtpk.fr'),
('PELISSIER-HERMITTE', 'Thierry', 'tpelissierhermitte@mtpk.fr'),
('PERRUCHE', 'Céline', 'cperruche@mtpk.fr'),
('PHELIX', 'Thomas', 'tphelix@mtpk.fr'),
('PIERRIS', 'Jean Francois', 'jfpierris@mtpk.fr'),
('PINNA', 'Marc', 'mpinna@mtpk.fr'),
('PINTO', 'Victor', 'vpinto@mtpk.fr'),
('PLANAS', 'Jean Louis', 'jplanas@mtpk.fr'),
('POTHERAT-KOHLER', 'Jean-françois', 'jfpkohler@mtpk.fr'),
('RAHIMI', 'Saïd', 'srahimi@mtpk.fr'),
('RAQUIN', 'Arnaud', 'araquin@mtpk.fr'),
('RASAMIMANANA', 'Arimisa', 'arasamimanana@mtpk.fr'),
('RASOLOFOMANANA', 'Herilala', 'hrasolofomanana@mtpk.fr'),
('RÉMINY', 'Richard', 'rreminy@mtpk.fr'),
('REY', 'Karine', 'krey@mtpk.fr'),
('RIGAUT', 'Cyril', 'crigaut@mtpk.fr'),
('RIOS', 'Sebastien', 'srios@mtpk.fr'),
('RIVIERE', 'Guillaume', 'griviere@mtpk.fr'),
('ROBIN', 'Pierre', 'probin@mtpk.fr'),
('ROTH', 'Yoann', 'yroth@mtpk.fr'),
('SAAIDIA', 'Ridha', 'rsaaidia@mtpk.fr'),
('SABATINI', 'Samuel', 'ssabatini@mtpk.fr'),
('SAIDI', 'Rachid', 'rsaidi@mtpk.fr'),
('SEGUIN', 'Miguel', 'mseguin@mtpk.fr'),
('SERREIR', 'Mohamed', 'mserreir@mtpk.fr'),
('SICOT', 'Bastien', 'bsicot@mtpk.fr'),
('SIMON', 'Yannick', 'ysimon@mtpk.fr'),
('SLANZI', 'Cristiano', 'cslanzi@mtpk.fr'),
('SYLVESTRE', 'Stéphane', 'ssylvestre@mtpk.fr'),
('TARLEY', 'Jérôme', 'jtarley@mtpk.fr'),
('THEZENAS', 'Annaëlle', 'athezenas@mtpk.fr'),
('THIVET', 'Julien', 'jthivet@mtpk.fr'),
('TOURNAT', 'Adrien', 'atournat@mtpk.fr'),
('VECIANA', 'Olivier', 'oveciana@mtpk.fr'),
('VERDIN', 'Christine', 'cverdin@mtpk.fr'),
('VERZEROLI', 'Pascal', 'pverzeroli@mtpk.fr'),
('VICTOR', 'Jérémy', 'jvictor@mtpk.fr'),
('VILLEGER', 'Solenne', 'svilleger@mtpk.fr'),
('WELE', 'Dahirou', 'dwele@mtpk.fr'),
('YAHIAOUI', 'Nathan', 'nyahiaoui@mtpk.fr');


create or replace TABLE T_R_DESCRIPTION_EVENEMENT (
	CODE_DESCRIPTION NUMBER(38,0) NOT NULL,
	LIBELLE_DESCRIPTION VARCHAR(500),
	CODE_TYPE_EVENEMENT NUMBER(38,0),
	IS_ACTIVE BOOLEAN DEFAULT TRUE,
	primary key (CODE_DESCRIPTION)
);

INSERT INTO T_R_DESCRIPTION_EVENEMENT (CODE_DESCRIPTION, CODE_TYPE_EVENEMENT, LIBELLE_DESCRIPTION, IS_ACTIVE)
VALUES
(1, 1, 'Foire aux vins', TRUE),
(2, 1, 'Foire aux plaisirs', TRUE),
(3, 1, 'Foire internationale de Bordeaux', TRUE),
(4, 1, 'Autre', TRUE),
(5, 2, 'Fête du fleuve - édition annuelle', TRUE),
(6, 2, 'Autre', TRUE),
(7, 3, 'Fête de la musique - 21 juin', TRUE),
(8, 3, 'Autre', TRUE),
(9, 4, 'Manifestation syndicale', TRUE),
(10, 4, 'Manifestation étudiante', TRUE),
(11, 4, 'Gilets jaunes', TRUE),
(12, 4, 'Autre', TRUE),
(13, 5, 'Marathon de Bordeaux', TRUE),
(14, 5, 'Semi-marathon', TRUE),
(15, 5, 'Course caritative', TRUE),
(16, 5, 'Autre', TRUE),
(17, 6, 'Carnaval des 2 rives', TRUE),
(18, 6, 'Autre', TRUE),
(19, 7, 'Concert Arkéa Arena', TRUE),
(20, 7, 'Concert Stade Matmut', TRUE),
(21, 7, 'Spectacle place des Quinconces', TRUE),
(22, 7, 'Autre', TRUE),
(23, 8, 'Match Girondins de Bordeaux', TRUE),
(24, 8, 'Match UBB (Rugby)', TRUE),
(25, 8, 'Autre', TRUE),
(26, 9, 'Marché des Capucins', TRUE),
(27, 9, 'Marché de Noël', TRUE),
(28, 9, 'Autre', TRUE),
(29, 10, 'Autre', TRUE),
(30, 11, 'Coupure fibre', TRUE),
(31, 11, 'Panne réseau opérateur', TRUE),
(32, 11, 'Autre', TRUE),
(33, 12, 'Barrière entrée bloquée', TRUE),
(34, 12, 'Barrière sortie bloquée', TRUE),
(35, 12, 'Lecteur badge HS', TRUE),
(36, 12, 'Autre', TRUE),
(37, 13, 'Peinture sol', TRUE),
(38, 13, 'Réfection éclairage', TRUE),
(39, 13, 'Maintenance ascenseur', TRUE),
(40, 13, 'Réparation ventilation', TRUE),
(41, 13, 'Autre', TRUE),
(42, 14, 'Travaux voirie', TRUE),
(43, 14, 'Travaux réseaux (eau/gaz/électricité)', TRUE),
(44, 14, 'Travaux tramway', TRUE),
(45, 14, 'Autre', TRUE),
(46, 15, 'Réservation exceptionnelle', TRUE),
(47, 15, 'Occupation abusive', TRUE),
(48, 15, 'Autre', TRUE),
(49, 16, 'Panne caisse automatique', TRUE),
(50, 16, 'Panne éclairage', TRUE),
(51, 16, 'Panne ventilation', TRUE),
(52, 16, 'Autre', TRUE),
(53, 17, 'Autre', TRUE);


create or replace TABLE T_R_DISTRICT (
	CODE_DISTRICT VARCHAR(10) NOT NULL,
	LIBELLE_DISTRICT VARCHAR(100),
	primary key (CODE_DISTRICT)
);

INSERT INTO T_R_DISTRICT (CODE_DISTRICT, LIBELLE_DISTRICT)
VALUES
(0, 'Non renseigné'),
(1, 'Centre'),
(2, 'Nord'),
(3, 'Sud');



create or replace TABLE T_R_EQUIPEMENT_ACCES (
	CODE_PARC VARCHAR(20) NOT NULL,
	NB_VOIES_ENTREES NUMBER(10,0),
	NB_VOIES_SORTIES NUMBER(10,0),
	NOM_PEAGEUR VARCHAR(100),
	NB_LECTEURS_PIETONS NUMBER(10,0),
	NB_LECTEURS_METSTATIONS NUMBER(10,0),
	NB_CAISSES NUMBER(10,0),
	NB_BORNES_PEAGE_ENTREES NUMBER(10,0),
	FLAG_DOUBLE_ENTREES VARCHAR(10),
	NB_BORNES_PEAGE_SORTIES NUMBER(10,0),
	FLAG_DOUBLE_SORTIES VARCHAR(10),
	FLAG_LECTURE_PLAQUE VARCHAR(10),
	NB_ASCENSEURS NUMBER(10,0),
	MARQUE_ASCENSEURS VARCHAR(100),
	NB_ESCALIERS NUMBER(10,0),
	NB_PORTAILS NUMBER(10,0),
	NB_PORTES_COULISSANTES NUMBER(10,0),
	NB_RIDEAUX_MOTORISES NUMBER(10,0),
	NB_BORNES_IRVE NUMBER(10,0),
	FLAG_GUIDAGE_PLACE VARCHAR(10),
	GABARIT_STANDARD VARCHAR(50),
	DATE_CREATION TIMESTAMP_NTZ(9),
	NOM_CREATEUR VARCHAR(100),
	DATE_MODIFICATION TIMESTAMP_NTZ(9),
	NOM_MODIFICATEUR VARCHAR(100),
	DATE_DEBUT TIMESTAMP_NTZ(9),
	DATE_FIN VARCHAR(20),
	IS_ACTIVE VARCHAR(10),
	DATE_MISE_SERVICE_ASCENSEUR DATE,
	FLAG_LOCKERS VARCHAR(10)
);

create or replace TABLE T_R_FLAG (
	CODE_FLAG VARCHAR(10) NOT NULL,
	LIBELLE_FLAG VARCHAR(100),
	primary key (CODE_FLAG)
);

INSERT INTO T_R_FLAG (CODE_FLAG, LIBELLE_FLAG)
VALUES
(-1, 'Non'),
(0, 'Non renseigné'),
(1, 'Oui');



create or replace TABLE T_R_GESTION (
	CODE_GESTION VARCHAR(10) NOT NULL,
	LIBELLE_GESTION VARCHAR(100),
	primary key (CODE_GESTION)
);

INSERT INTO T_R_GESTION (CODE_GESTION, LIBELLE_GESTION)
VALUES
(0, 'Non renseigné'),
(1, 'Conv (Cinema)'),
(2, 'Conv (clinique)'),
(3, 'Conv (Ehpad)'),
(4, 'Conv (SNCF)'),
(5, 'Conv (Syndic)'),
(6, 'Indigo'),
(7, 'MTPK');


create or replace TABLE T_R_IMPACT_EVENEMENT (
	CODE_IMPACT NUMBER(38,0) NOT NULL,
	LIBELLE_IMPACT VARCHAR(200),
	NIVEAU_SEVERITE NUMBER(38,0),
	IS_ACTIVE BOOLEAN DEFAULT TRUE,
	primary key (CODE_IMPACT)
);

INSERT INTO T_R_IMPACT_EVENEMENT (CODE_IMPACT, LIBELLE_IMPACT, NIVEAU_SEVERITE, IS_ACTIVE)
VALUES
(1, 'Aucun impact notable', 1, TRUE),
(2, 'Ralentissement', 2, TRUE),
(3, 'Surcharge temporaire', 2, TRUE),
(4, 'Accès restreint', 3, TRUE),
(5, 'Déviation imposée', 3, TRUE),
(6, 'Fermeture partielle', 3, TRUE),
(7, 'Blocage total', 4, TRUE);


create or replace TABLE T_R_NATURE_JURIDIQUE (
	CODE_NATURE_JURIDIQUE VARCHAR(10) NOT NULL,
	LIBELLE_NATURE_JURIDIQUE VARCHAR(200),
	primary key (CODE_NATURE_JURIDIQUE)
);

INSERT INTO T_R_NATURE_JURIDIQUE (CODE_NATURE_JURIDIQUE, LIBELLE_NATURE_JURIDIQUE)
VALUES
(0, 'Non renseigné'),
(1, 'Convention'),
(2, 'Mise en affectation'),
(3, 'Pleine Propriété');


create or replace TABLE T_R_PARC (
	CODE_PARC VARCHAR(20) NOT NULL,
	NOM_PARC VARCHAR(200),
	ADRESSE_PARC VARCHAR(500),
	CODE_VILLE VARCHAR(10),
	CODE_SECTEUR VARCHAR(10),
	CODE_DISTRICT VARCHAR(10),
	CODE_TYPE_PARC VARCHAR(10),
	CODE_FLAG_FOURRIERE VARCHAR(10),
	CODE_FLAG_METSTATION VARCHAR(10),
	DATE_CREATION TIMESTAMP_NTZ(9),
	NOM_CREATEUR VARCHAR(100),
	DATE_MODIFICATION TIMESTAMP_NTZ(9),
	NOM_MODIFICATEUR VARCHAR(100),
	DATE_DEBUT TIMESTAMP_NTZ(9),
	DATE_FIN VARCHAR(20),
	IS_ACTIVE VARCHAR(10)
);

INSERT INTO T_R_PARC (CODE_PARC, NOM_PARC, ADRESSE_PARC, CODE_VILLE, CODE_SECTEUR, CODE_DISTRICT, CODE_TYPE_PARC, CODE_FLAG_FOURRIERE, CODE_FLAG_METSTATION, DATE_CREATION, NOM_CREATEUR, DATE_MODIFICATION, NOM_MODIFICATEUR, DATE_DEBUT, DATE_FIN, IS_ACTIVE)
VALUES
('H8MAI', '8 Mai 1985', 'Cours Maréchal Juin', '1', '1', '1', '3', '1', '1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('HACHA', 'Allees de Chartres', 'Allées de Bristol', '1', '1', '1', '2', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('HALOR', 'Alsace Lorraine', '21 Cours d''Alsace-Lorraine', '1', '1', '1', '3', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('CAMED', 'Amedee', '3 rue des échoppes', '1', '2', '3', '2', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('CDUNA', 'Amplitude', '35 rue Renée Buthaud', '2', '2', '3', '1', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('PAREN', 'Arena', 'Rue Pierre Kaldor/ avenue Alfonséa', '3', '3', '3', '1', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('CBEAU', 'Beaujon', 'Impasse des Cossus', '1', '2', '2', '1', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('CBERG', 'Bergonie', '220 cours de l''Argonne', '1', '2', '3', '2', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('HBONN', 'Bonnac', '42 Rue du Château d''eau', '1', '1', '1', '3', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('PBORD', 'Bord''Oh', '14 Rue Andrée Putman', '2', '3', '1', '3', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('PBRAZZ', 'Brazza', '202 rue des Queyries Bdx', '1', '3', '1', '2', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('HCAJU', 'Camille Jullian', '2 Pl. Camille Jullian', '1', '1', '1', '3', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('HCCME', 'CC Meriadeck', 'Rue Révérend Père Dieuzaide', '1', '1', '2', '3', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('HCMON', 'Cite Mondiale', '20 Quai des Chartrons', '1', '1', '1', '3', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('CCSEG', 'Croix de Seguey', '33 rue de la croix de Seguey', '1', '2', '2', '2', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('HFDME', 'Front du Medoc', 'Rue Robert Lateulade', '1', '1', '2', '1', '1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('HGAMB', 'Gambetta', 'Rue Edmond Michelet', '1', '1', '2', '3', '-1', '1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('CGSJE', 'Gare Saint Jean', '36 rue Charles Domercq', '1', '2', '3', '3', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('CGPAR', 'Grand Parc', 'Rue du Docteur Finlay', '1', '2', '2', '1', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('HGHOM', 'Grands Hommes', '3 Place des Grands Hommes', '1', '1', '2', '3', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('PLAHA', 'Laharpe', '59 Avenue d''Eysines', '4', '3', '2', '2', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('HLHOT', 'Lhote', '5-7 Rue Lhôte', '1', '1', '2', '3', '-1', '1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('PLIBE', 'Liberation', '43 Avenue de la Libération', '4', '3', '2', '1', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('PMEGA', 'Megarama', 'Allée Serr', '2', '3', '1', '3', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('PMERI', 'Merignac', 'Place Charles de Gaulle', '5', '3', '2', '3', '-1', '1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('CPALU', 'Paludate', 'Quai de Paludate', '1', '2', '3', '1', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('PPESS', 'Pessac', 'Rue des Poilus', '6', '3', '3', '3', '-1', '1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('HPBER', 'Pey Berland', 'Place Pey Berland', '1', '1', '1', '3', '-1', '1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('CPBDX', 'Porte de Bordeaux', '48 rue Général de Larminat', '1', '2', '3', '3', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('HREPU', 'Republique', 'Place de la République', '1', '1', '1', '3', '-1', '1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('CBEGL', 'Rue de Begles', '120 rue de Bègles', '1', '2', '3', '3', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('PSECH', 'Secheries', '13 Allée de Francs', '7', '3', '3', '1', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('PUGC', 'UGC', 'Allée du 7ème art', '8', '3', '3', '3', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('HVICT', 'Victoire', 'Place de la Victoire', '1', '1', '1', '3', '-1', '1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('HVHUG', 'Victor Hugo', 'Place de la Ferme Richemont', '1', '1', '1', '1', '-1', '1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE');



create or replace TABLE T_R_PARC_EXPLOITATION (
	CODE_PARC VARCHAR(20) NOT NULL,
	NB_CAPACITE_VL_DT_THERMIQUE NUMBER(38,0),
	NB_CAPACITE_VL_DT_ELECTRIQUE NUMBER(38,0),
	NB_CAPACITE_VL_DT_PMR NUMBER(38,0),
	NB_CAPACITE_VL_DT_PMR_ELECTRIQUE NUMBER(38,0),
	NB_CAPACITE_VL_DT_MOTO NUMBER(38,0),
	NB_CAPACITE_VL_DT_VELO NUMBER(38,0),
	NB_CAPACITE_VL_DT_AUTRE NUMBER(38,0),
	COMMENTAIRE_AUTRE VARCHAR(500),
	NB_VOIES_ACCES NUMBER(38,0),
	NB_VOIES_SORTIES NUMBER(38,0),
	NB_ASCENCEUR NUMBER(38,0),
	NB_ESCALIER NUMBER(38,0),
	NB_PORTAIL NUMBER(38,0),
	NB_TRAPPE_EVACUATION_MOTORISEE NUMBER(38,0),
	NB_RIDEAUX_MOTORISEE NUMBER(38,0),
	DATE_CREATION TIMESTAMP_NTZ(9),
	NOM_CREATEUR VARCHAR(100),
	DATE_MODIFICATION TIMESTAMP_NTZ(9),
	NOM_MODIFICATEUR VARCHAR(100),
	DATE_DEBUT TIMESTAMP_NTZ(9),
	DATE_FIN VARCHAR(20),
	IS_ACTIVE BOOLEAN,
	NOM_PEAGEUR VARCHAR(100),
	NB_LECTEURS_PIETONS NUMBER(38,0),
	NB_LECTEURS_METSTATIONS NUMBER(38,0),
	NB_CAISSES NUMBER(38,0),
	NB_BORNES_PEAGES_ENTREES NUMBER(38,0),
	FLAG_DOUBLE_ENTREES VARCHAR(10),
	NB_BORNES_PEAGES_SORTIES NUMBER(38,0),
	FLAG_DOUBLE_SORTIES VARCHAR(10),
	FLAG_LECTURE_PLAQUE VARCHAR(10),
	MARQUE_ASCENCEUR VARCHAR(100),
	NB_PORTES_COULISSANTES NUMBER(38,0),
	NB_BORNES_IRVE NUMBER(38,0),
	NB_LOCKERS NUMBER(38,0),
	FLAG_GUIDAGE_PLACE VARCHAR(10),
	GABARIT_STANDARD VARCHAR(100),
	SURFACE NUMBER(38,0),
	DATE_MISE_EN_SERVICE_ASCENCEUR DATE,
	NIVEAU VARCHAR(50),
	NB_CAPACITE_VL NUMBER(10,0),
	NB_CAPACITE_EXPLOITEE NUMBER(10,0),
	NB_CAPACITE_TOTALE NUMBER(10,0)
);

create or replace TABLE T_R_PARC_JURIDIQUE (
	CODE_PARC VARCHAR(20) NOT NULL,
	MISE_EN_SERVICE VARCHAR(50),
	CODE_NATURE_JURIDIQUE VARCHAR(10),
	SIRET VARCHAR(50),
	CODE_FLAG_COPRO VARCHAR(10),
	DATE_CREATION TIMESTAMP_NTZ(9),
	NOM_CREATEUR VARCHAR(100),
	DATE_MODIFICATION TIMESTAMP_NTZ(9),
	NOM_MODIFICATEUR VARCHAR(100),
	DATE_DEBUT TIMESTAMP_NTZ(9),
	DATE_FIN VARCHAR(20),
	IS_ACTIVE BOOLEAN,
	TYPE_CONVENTION VARCHAR(200),
	NOM_TIERS_ATTENANT VARCHAR(200),
	NOM_COPRO VARCHAR(200)
);

create or replace TABLE T_R_PARC_SECURITE_INCENDIE (
	CODE_PARC VARCHAR(20) NOT NULL,
	EAE_SPRINKLEURS VARCHAR(50),
	NB_POSTES NUMBER(38,0),
	NB_TETES NUMBER(38,0),
	NB_EXTINCTEURS_TOTAL NUMBER(38,0),
	NB_BAC_A_SABLE NUMBER(38,0),
	DATE_CREATION TIMESTAMP_NTZ(9),
	NOM_CREATEUR VARCHAR(100),
	DATE_MODIFICATION TIMESTAMP_NTZ(9),
	NOM_MODIFICATEUR VARCHAR(100),
	DATE_DEBUT TIMESTAMP_NTZ(9),
	DATE_FIN VARCHAR(20),
	IS_ACTIVE BOOLEAN,
	FLAG_SSI VARCHAR(10),
	TYPE_SSI VARCHAR(100),
	MARQUE_SSI VARCHAR(100),
	NB_EXTRACTEURS NUMBER(38,0),
	NB_INSUFFLATEURS NUMBER(38,0),
	NB_COLONNES_SECHES NUMBER(38,0),
	NB_BAES NUMBER(38,0),
	TYPE_ALIMENTATION_BAES VARCHAR(100),
	NB_TRAPPE_EVACUATION_MOTORISEE NUMBER(38,0),
	TYPE_TARIFS_ELEC VARCHAR(100),
	FLAG_CELLULES_HT VARCHAR(10),
	FLAG_GROUPE_ELECTROGENE VARCHAR(10),
	CAPACITE_CUVE_FIOUL NUMBER(38,0),
	AVIS_COMMISSION VARCHAR(100),
	DATE_MISE_EN_SERVICE_SSI DATE,
	DATE_DERNIERE_COMMISSION DATE,
	FLAG_TGS VARCHAR(10),
	NB_PORTE_COMPARTIMENTAGE NUMBER(38,0),
	NB_DAI NUMBER(38,0),
	NB_DETECTION_CO_NO NUMBER(38,0)
);

create or replace TABLE T_R_PEAGEUR (
	CODE_PEAGEUR VARCHAR(10) NOT NULL,
	LIBELLE_PEAGEUR VARCHAR(100),
	primary key (CODE_PEAGEUR)
);

INSERT INTO T_R_PEAGEUR (CODE_PEAGEUR, LIBELLE_PEAGEUR)
VALUES
(1, 'DESIGNA'),
(2, 'HITACHI'),
(3, 'ORBILITY'),
(4, 'SKIDATA');


create or replace TABLE T_R_SECTEUR (
	CODE_SECTEUR VARCHAR(10) NOT NULL,
	LIBELLE_SECTEUR VARCHAR(100),
	primary key (CODE_SECTEUR)
);


INSERT INTO T_R_SECTEUR (CODE_SECTEUR, LIBELLE_SECTEUR)
VALUES
(0, 'Non renseigné'),
(1, 'Hypercentre'),
(2, 'Centre'),
(3, 'Periphérie');


create or replace TABLE T_R_TYPE_EVENEMENT (
	CODE_TYPE_EVENEMENT NUMBER(38,0) NOT NULL,
	LIBELLE_TYPE_EVENEMENT VARCHAR(200) NOT NULL,
	CATEGORIE VARCHAR(100) NOT NULL,
	IS_TRAVAUX BOOLEAN DEFAULT FALSE,
	IS_ACTIVE BOOLEAN DEFAULT TRUE,
	primary key (CODE_TYPE_EVENEMENT)
);


INSERT INTO T_R_TYPE_EVENEMENT (CODE_TYPE_EVENEMENT, LIBELLE_TYPE_EVENEMENT, CATEGORIE, IS_TRAVAUX, IS_ACTIVE)
VALUES
(1, 'Foire', 'Externe', FALSE, TRUE),
(2, 'Fête du fleuve', 'Externe', FALSE, TRUE),
(3, 'Fête de la musique', 'Externe', FALSE, TRUE),
(4, 'Manifestation', 'Externe', FALSE, TRUE),
(5, 'Marathon', 'Externe', FALSE, TRUE),
(6, 'Carnaval', 'Externe', FALSE, TRUE),
(7, 'Concert / Spectacle', 'Externe', FALSE, TRUE),
(8, 'Match / Événement sportif', 'Externe', FALSE, TRUE),
(9, 'Marché', 'Externe', FALSE, TRUE),
(10, 'Autre événement externe', 'Externe', FALSE, TRUE),
(11, 'Coupure internet', 'Technique', FALSE, TRUE),
(12, 'Barrière défectueuse', 'Technique', FALSE, TRUE),
(13, 'Travaux internes', 'Technique', TRUE, TRUE),
(14, 'Travaux externes', 'Technique', TRUE, TRUE),
(15, 'Indisponibilité de places', 'Technique', FALSE, TRUE),
(16, 'Panne équipement', 'Technique', FALSE, TRUE),
(17, 'Autre incident technique', 'Technique', FALSE, TRUE),
(18, 'Traveaux externes ville de Bordeaux', 'Technique', FALSE, TRUE);


create or replace TABLE T_R_TYPE_PARC (
	CODE_TYPE_PARC VARCHAR(10) NOT NULL,
	LIBELLE_TYPE_PARC VARCHAR(100),
	primary key (CODE_TYPE_PARC)
);



INSERT INTO T_R_TYPE_PARC (CODE_TYPE_PARC, LIBELLE_TYPE_PARC)
VALUES
(1, 'Infrastructure'),
(2, 'Superstructure'),
(3, 'Exterieur'),
(4, 'Infra et Superstructure');


create or replace TABLE T_R_VILLE (
	CODE_VILLE VARCHAR(10) NOT NULL,
	CODE_POSTAL VARCHAR(10),
	LIBELLE_VILLE VARCHAR(100),
	primary key (CODE_VILLE)
);

INSERT INTO T_R_VILLE (CODE_VILLE, CODE_POSTAL, LIBELLE_VILLE)
VALUES
(0, 'NR', 'Non renseigné'),
(1, '33000', 'Bordeaux'),
(2, '33100', 'Bordeaux'),
(3, '33270', 'Floirac'),
(4, '33110', 'Le Bouscat'),
(5, '33700', 'Merignac'),
(6, '33600', 'Pessac'),
(7, '33130', 'Bègles'),
(8, '33400', 'Talence');


-- ============================================================
USE ROLE R_DATA_ING_PRD;
USE DATABASE DB_REFERENTIEL_PRD;
USE SCHEMA S_REFERENTIEL;
-- ============================================================


-- ============================================================
-- SCRIPTS DE CREATION ET D'ALIMENTATION DES TABLES
-- Schema : DB_REFERENTIEL_PRD.S_REFERENTIEL
-- ============================================================

-- 2. CREATION DES TABLES
-- ============================================================


create or replace TABLE T_F_HISTORIQUE_EVENEMENT (
	CODE_EVENEMENT NUMBER(38,0),
	TITRE_EVENEMENT VARCHAR(500),
	TYPE_EVENEMENT VARCHAR(200),
	CATEGORIE VARCHAR(50),
	DESCRIPTION VARCHAR(1000),
	LIEU VARCHAR(200),
	VILLE VARCHAR(100),
	IMPACT VARCHAR(200),
	NIVEAU_SEVERITE NUMBER(38,0),
	DATE_DEBUT TIMESTAMP_NTZ(9),
	DATE_FIN TIMESTAMP_NTZ(9),
	IS_JOURNEE_PARTIELLE BOOLEAN,
	CRENEAU VARCHAR(50),
	NB_PLACES_IMPACTEES NUMBER(38,0),
	FERMETURE_TOTALE BOOLEAN,
	NB_PISTES_ENTREE_FERMEES NUMBER(38,0),
	NB_PISTES_SORTIE_FERMEES NUMBER(38,0),
	TYPE_TRAVAUX VARCHAR(50),
	CONTACT_INTERNE VARCHAR(200),
	CONTACT_EXTERNE VARCHAR(200),
	IS_TRAVAUX_PHASES BOOLEAN,
	COMMENTAIRE VARCHAR(2000),
	PARKINGS_IMPACTES VARCHAR(2000),
	IS_ACTIVE NUMBER(38,0),
	MODIFIE_PAR VARCHAR(100),
	ACTION VARCHAR(50),
	DATE_DEBUT_VALIDITE TIMESTAMP_NTZ(9),
	DATE_FIN_VALIDITE TIMESTAMP_NTZ(9)
);



create or replace TABLE T_F_PHASE_TRAVAUX (
	CODE_PHASE NUMBER(38,0) NOT NULL autoincrement start 1 increment 1 noorder,
	CODE_EVENEMENT NUMBER(38,0) NOT NULL,
	NUMERO_PHASE NUMBER(38,0),
	DATE_DEBUT TIMESTAMP_NTZ(9),
	DATE_FIN TIMESTAMP_NTZ(9),
	NB_PLACES_IMPACTEES NUMBER(38,0),
	COMMENTAIRE VARCHAR(1000),
	primary key (CODE_PHASE)
);



create or replace TABLE T_R_CONTACT_INTERNE (
	CODE_CONTACT NUMBER(38,0) NOT NULL autoincrement start 1 increment 1 noorder,
	NOM VARCHAR(200) NOT NULL,
	EMAIL VARCHAR(200) NOT NULL,
	SERVICE VARCHAR(100),
	IS_ACTIVE BOOLEAN DEFAULT TRUE,
	DATE_CREATION TIMESTAMP_NTZ(9) DEFAULT CURRENT_TIMESTAMP(),
	PRENOM VARCHAR(200),
	primary key (CODE_CONTACT)
);

-- Insertion des contacts
INSERT INTO T_R_CONTACT_INTERNE (NOM, PRENOM, EMAIL)
VALUES
('ABENZOAR', 'Magaly', 'mabenzoar@mtpk.fr'),
('ALANIC', 'Christophe', 'calanic@mtpk.fr'),
('ANDREOTTI', 'Nicolas', 'nandreotti@mtpk.fr'),
('ANONKRE', 'Franck', 'fanonkre@mtpk.fr'),
('ASO', 'Jonathan', 'jaso@mtpk.fr'),
('AUDIGEOS', 'Philippe', 'paudigeos@mtpk.fr'),
('AYELLA', 'Elvis', 'eayella@mtpk.fr'),
('BAGUELIN', 'Steven', 'sbaguelin@mtpk.fr'),
('BEDORA', 'Melanie', 'mbedora@mtpk.fr'),
('BELLAZEREG', 'Nasser', 'nbellazereg@mtpk.fr'),
('BENGRID', 'Aymen', 'abengrid@mtpk.fr'),
('BERGEROT', 'Matthieu', 'mbergerot@mtpk.fr'),
('BIRONNEAU', 'Matthias', 'mbironneau@mtpk.fr'),
('BISCARRO', 'Valérie', 'vbiscarro@mtpk.fr'),
('BOISUMEAU', 'Ludovic', 'lboisumeau@mtpk.fr'),
('BORDAS', 'Laurent', 'lbordas@mtpk.fr'),
('BORDIN-MORA', 'Céline', 'cbordinmora@mtpk.fr'),
('BOUARROUJ', 'Nahed', 'nbouarrouj@mtpk.fr'),
('BOUAT', 'Gaëtan', 'gbouat@mtpk.fr'),
('BOUDET', 'David', 'dboudet@mtpk.fr'),
('BOUDJEMA', 'Samir', 'sboudjema@mtpk.fr'),
('BOYANCE', 'Benoît', 'bboyance@mtpk.fr'),
('BREBINAUD', 'Paul', 'pbrebinaud@mtpk.fr'),
('CAMBON', 'Agathe', 'acambon@mtpk.fr'),
('CAR', 'Christophe', 'ccar@mtpk.fr'),
('CHAKOUH', 'Samy', 'schakouh@mtpk.fr'),
('CHALLEMET', 'Alice', 'achallemet@mtpk.fr'),
('CHERKI', 'Abderrafik', 'rcherki@mtpk.fr'),
('CHEVALIER', 'Mickaël', 'mchevalier@mtpk.fr'),
('CHEVALOT', 'Grégory', 'gchevalot@mtpk.fr'),
('COLLET', 'Patricia', 'pcollet@mtpk.fr'),
('COMBRET', 'Gaëtan', 'gcombret@mtpk.fr'),
('CRUZ', 'Cyril', 'ccruz@mtpk.fr'),
('CUING', 'André', 'acuing@mtpk.fr'),
('CURCI', 'Sabine', 'scurci@mtpk.fr'),
('DAUSSOIR TAUZIN', 'Kevin', 'kdaussoirtauzin@mtpk.fr'),
('DEBOURGE', 'Olivier', 'odebourge@mtpk.fr'),
('DECAUDAIN', 'Jean Jacques', 'jdecaudain@mtpk.fr'),
('DELAGE', 'Romain', 'rdelage@mtpk.fr'),
('DELAMARE', 'Hina', 'hdelamare@mtpk.fr'),
('DELPECH', 'Jean Pierre', 'jdelpech@mtpk.fr'),
('DENONAIN', 'Emma', 'edenonain@mtpk.fr'),
('DESNIOU', 'Jérémy', 'jdesniou@mtpk.fr'),
('DEVYLDER', 'Michaël', 'mdevylder@mtpk.fr'),
('DONINEAUX', 'Maxed', 'mdonineaux@mtpk.fr'),
('DOUET', 'Rémi', 'rdouet@mtpk.fr'),
('DRUILLET', 'Julie', 'jdruillet@mtpk.fr'),
('DUPART', 'Nicolas', 'ndupart@mtpk.fr'),
('ENOUS', 'Véronique', 'venous@mtpk.fr'),
('ETCHEGORRY', 'Jessica', 'jetchegorry@mtpk.fr'),
('EZELIN', 'Nicolas', 'nezelin@mtpk.fr'),
('FAIVRE', 'Frédéric', 'ffaivre@mtpk.fr'),
('FAURE', 'Jean-Baptiste', 'jbfaure@mtpk.fr'),
('FERCHAUT', 'Jérémy-William', 'jferchaut@mtpk.fr'),
('FOUCHER', 'Angélique', 'ahautreux@mtpk.fr'),
('FRICOT-DELAPLANCHE', 'Anthony', 'africotdelaplanche@mtpk.fr'),
('GAIDOT', 'Marianne', 'mgaidot@mtpk.fr'),
('GARCIA', 'Guillaume', 'ggarcia@mtpk.fr'),
('GARELLI', 'Fabienne', 'fgarelli@mtpk.fr'),
('GASO', 'Stéphane', 'sgaso@mtpk.fr'),
('GAUDUCHEAU', 'Francis', 'fgauducheau@mtpk.fr'),
('GAUTHIER', 'Virginie', 'vgauthier@mtpk.fr'),
('GOMBEAU', 'Jean-Michel', 'jgombeau@mtpk.fr'),
('GOMEZ', 'Eduardo', 'egomez@mtpk.fr'),
('GOMEZ', 'Jean-Louis', 'jlgomez@mtpk.fr'),
('GRAND', 'Sébastien', 'sgrand@mtpk.fr'),
('GRAS', 'Rémi', 'rgras@mtpk.fr'),
('GRIS', 'Cécile', 'cgris@mtpk.fr'),
('GUILARD', 'Francois', 'fguilard@mtpk.fr'),
('HAMROUNI', 'Ferid', 'fhamrouni@mtpk.fr'),
('HARZALLAH', 'Vincent', 'vharzallah@mtpk.fr'),
('HATINGUAIS', 'Charline', 'chatinguais@mtpk.fr'),
('HERMELIN', 'Benjamin', 'bhermelin@mtpk.fr'),
('HERVAUD', 'Benoît', 'bhervaud@mtpk.fr'),
('HIRIART', 'Charlotte', 'chiriart@mtpk.fr'),
('HOFFMANN', 'Charline', 'choffmann@mtpk.fr'),
('JACQUES', 'Jérémy', 'jjacques@mtpk.fr'),
('JACQUET', 'Cécile', 'cjacquet@mtpk.fr'),
('JORE', 'Aurélien', 'ajore@mtpk.fr'),
('KAMAL-EDINE', 'Adihamou', 'AKAMALEDINE@mtpk.fr'),
('KIRAT', 'Hinde', 'hkirat@mtpk.fr'),
('KRANITZ', 'Linda', 'lkranitz@mtpk.fr'),
('LABARBE', 'Nathalie', 'nlabarbe@mtpk.fr'),
('LABRUE', 'Sébastien', 'slabrue@mtpk.fr'),
('LACHAUD', 'Jean-Marie', 'jmlachaud@mtpk.fr'),
('LACOMBE', 'Mounira', 'mlacombe@mtpk.fr'),
('LACOMBE', 'Bruno', 'blacombe@mtpk.fr'),
('LAFAYE', 'Sylvie', 'slafaye@mtpk.fr'),
('LAPORT', 'Ludovic', 'llaport@mtpk.fr'),
('LARCEBEAU', 'Nicolas', 'nlarcebeau@mtpk.fr'),
('LARRAUX', 'Alexandre', 'alarraux@mtpk.fr'),
('LARTOT-DA LUZ RIJO', 'Frédéric', 'flartot@mtpk.fr'),
('LAVAUD', 'Julien', 'jlavaud@mtpk.fr'),
('LE QUELLEC', 'Gaëtan', 'glequellec@mtpk.fr'),
('LECUROU', 'Chrystelle', 'clecurou@mtpk.fr'),
('LEGRAS', 'Emma', 'elegras@mtpk.fr'),
('LEPARMENTIER', 'Alexandra', 'aleparmentier@mtpk.fr'),
('LEVEQUE', 'Justine', 'jleveque@mtpk.fr'),
('LEVY', 'Roger', 'rlevy@mtpk.fr'),
('LIMA', 'Daniel', 'dlima@mtpk.fr'),
('LOPEZ', 'Franck', 'flopez@mtpk.fr'),
('LORA', 'Guillaume', 'glora@mtpk.fr'),
('LOUREIRO', 'José Manuel', 'jloureiro@mtpk.fr'),
('MAILLE', 'Linda', 'lmaille@mtpk.fr'),
('MARCHAND', 'Nadège', 'nmarchand@mtpk.fr'),
('M''BARI', 'Emmanuel', 'embari@mtpk.fr'),
('MBENG-ONGOUA', 'Richard Wilfried', 'rmbengongoua@mtpk.fr'),
('MBOCK WENDJEL', 'Jacques', 'jmbockwendjel@mtpk.fr'),
('MICHELLET', 'Eva', 'emichellet@mtpk.fr'),
('M''NEMOSYME', 'Enric Paul', 'em''nemosyme@mtpk.fr'),
('MORISCOT', 'Fabrice', 'fmoriscot@mtpk.fr'),
('NADALIÉ', 'Inès', 'inadalie@mtpk.fr'),
('NAKU', 'Mireille', 'manaku@mtpk.fr'),
('NAWROCKI', 'Julien', 'jnawrocki@mtpk.fr'),
('NOWACKI', 'Pascal', 'pnowacki@mtpk.fr'),
('PAUWELS', 'Kévin', 'kpauwels@mtpk.fr'),
('PECOUT', 'Philippe', 'ppecout@mtpk.fr'),
('PELISSIER-HERMITTE', 'Thierry', 'tpelissierhermitte@mtpk.fr'),
('PERRUCHE', 'Céline', 'cperruche@mtpk.fr'),
('PHELIX', 'Thomas', 'tphelix@mtpk.fr'),
('PIERRIS', 'Jean Francois', 'jfpierris@mtpk.fr'),
('PINNA', 'Marc', 'mpinna@mtpk.fr'),
('PINTO', 'Victor', 'vpinto@mtpk.fr'),
('PLANAS', 'Jean Louis', 'jplanas@mtpk.fr'),
('POTHERAT-KOHLER', 'Jean-françois', 'jfpkohler@mtpk.fr'),
('RAHIMI', 'Saïd', 'srahimi@mtpk.fr'),
('RAQUIN', 'Arnaud', 'araquin@mtpk.fr'),
('RASAMIMANANA', 'Arimisa', 'arasamimanana@mtpk.fr'),
('RASOLOFOMANANA', 'Herilala', 'hrasolofomanana@mtpk.fr'),
('RÉMINY', 'Richard', 'rreminy@mtpk.fr'),
('REY', 'Karine', 'krey@mtpk.fr'),
('RIGAUT', 'Cyril', 'crigaut@mtpk.fr'),
('RIOS', 'Sebastien', 'srios@mtpk.fr'),
('RIVIERE', 'Guillaume', 'griviere@mtpk.fr'),
('ROBIN', 'Pierre', 'probin@mtpk.fr'),
('ROTH', 'Yoann', 'yroth@mtpk.fr'),
('SAAIDIA', 'Ridha', 'rsaaidia@mtpk.fr'),
('SABATINI', 'Samuel', 'ssabatini@mtpk.fr'),
('SAIDI', 'Rachid', 'rsaidi@mtpk.fr'),
('SEGUIN', 'Miguel', 'mseguin@mtpk.fr'),
('SERREIR', 'Mohamed', 'mserreir@mtpk.fr'),
('SICOT', 'Bastien', 'bsicot@mtpk.fr'),
('SIMON', 'Yannick', 'ysimon@mtpk.fr'),
('SLANZI', 'Cristiano', 'cslanzi@mtpk.fr'),
('SYLVESTRE', 'Stéphane', 'ssylvestre@mtpk.fr'),
('TARLEY', 'Jérôme', 'jtarley@mtpk.fr'),
('THEZENAS', 'Annaëlle', 'athezenas@mtpk.fr'),
('THIVET', 'Julien', 'jthivet@mtpk.fr'),
('TOURNAT', 'Adrien', 'atournat@mtpk.fr'),
('VECIANA', 'Olivier', 'oveciana@mtpk.fr'),
('VERDIN', 'Christine', 'cverdin@mtpk.fr'),
('VERZEROLI', 'Pascal', 'pverzeroli@mtpk.fr'),
('VICTOR', 'Jérémy', 'jvictor@mtpk.fr'),
('VILLEGER', 'Solenne', 'svilleger@mtpk.fr'),
('WELE', 'Dahirou', 'dwele@mtpk.fr'),
('YAHIAOUI', 'Nathan', 'nyahiaoui@mtpk.fr');


create or replace TABLE T_R_DESCRIPTION_EVENEMENT (
	CODE_DESCRIPTION NUMBER(38,0) NOT NULL,
	LIBELLE_DESCRIPTION VARCHAR(500),
	CODE_TYPE_EVENEMENT NUMBER(38,0),
	IS_ACTIVE BOOLEAN DEFAULT TRUE,
	primary key (CODE_DESCRIPTION)
);

INSERT INTO T_R_DESCRIPTION_EVENEMENT (CODE_DESCRIPTION, CODE_TYPE_EVENEMENT, LIBELLE_DESCRIPTION, IS_ACTIVE)
VALUES
(1, 1, 'Foire aux vins', TRUE),
(2, 1, 'Foire aux plaisirs', TRUE),
(3, 1, 'Foire internationale de Bordeaux', TRUE),
(4, 1, 'Autre', TRUE),
(5, 2, 'Fête du fleuve - édition annuelle', TRUE),
(6, 2, 'Autre', TRUE),
(7, 3, 'Fête de la musique - 21 juin', TRUE),
(8, 3, 'Autre', TRUE),
(9, 4, 'Manifestation syndicale', TRUE),
(10, 4, 'Manifestation étudiante', TRUE),
(11, 4, 'Gilets jaunes', TRUE),
(12, 4, 'Autre', TRUE),
(13, 5, 'Marathon de Bordeaux', TRUE),
(14, 5, 'Semi-marathon', TRUE),
(15, 5, 'Course caritative', TRUE),
(16, 5, 'Autre', TRUE),
(17, 6, 'Carnaval des 2 rives', TRUE),
(18, 6, 'Autre', TRUE),
(19, 7, 'Concert Arkéa Arena', TRUE),
(20, 7, 'Concert Stade Matmut', TRUE),
(21, 7, 'Spectacle place des Quinconces', TRUE),
(22, 7, 'Autre', TRUE),
(23, 8, 'Match Girondins de Bordeaux', TRUE),
(24, 8, 'Match UBB (Rugby)', TRUE),
(25, 8, 'Autre', TRUE),
(26, 9, 'Marché des Capucins', TRUE),
(27, 9, 'Marché de Noël', TRUE),
(28, 9, 'Autre', TRUE),
(29, 10, 'Autre', TRUE),
(30, 11, 'Coupure fibre', TRUE),
(31, 11, 'Panne réseau opérateur', TRUE),
(32, 11, 'Autre', TRUE),
(33, 12, 'Barrière entrée bloquée', TRUE),
(34, 12, 'Barrière sortie bloquée', TRUE),
(35, 12, 'Lecteur badge HS', TRUE),
(36, 12, 'Autre', TRUE),
(37, 13, 'Peinture sol', TRUE),
(38, 13, 'Réfection éclairage', TRUE),
(39, 13, 'Maintenance ascenseur', TRUE),
(40, 13, 'Réparation ventilation', TRUE),
(41, 13, 'Autre', TRUE),
(42, 14, 'Travaux voirie', TRUE),
(43, 14, 'Travaux réseaux (eau/gaz/électricité)', TRUE),
(44, 14, 'Travaux tramway', TRUE),
(45, 14, 'Autre', TRUE),
(46, 15, 'Réservation exceptionnelle', TRUE),
(47, 15, 'Occupation abusive', TRUE),
(48, 15, 'Autre', TRUE),
(49, 16, 'Panne caisse automatique', TRUE),
(50, 16, 'Panne éclairage', TRUE),
(51, 16, 'Panne ventilation', TRUE),
(52, 16, 'Autre', TRUE),
(53, 17, 'Autre', TRUE);


create or replace TABLE T_R_DISTRICT (
	CODE_DISTRICT VARCHAR(10) NOT NULL,
	LIBELLE_DISTRICT VARCHAR(100),
	primary key (CODE_DISTRICT)
);

INSERT INTO T_R_DISTRICT (CODE_DISTRICT, LIBELLE_DISTRICT)
VALUES
(0, 'Non renseigné'),
(1, 'Centre'),
(2, 'Nord'),
(3, 'Sud');



create or replace TABLE T_R_EQUIPEMENT_ACCES (
	CODE_PARC VARCHAR(20) NOT NULL,
	NB_VOIES_ENTREES NUMBER(10,0),
	NB_VOIES_SORTIES NUMBER(10,0),
	NOM_PEAGEUR VARCHAR(100),
	NB_LECTEURS_PIETONS NUMBER(10,0),
	NB_LECTEURS_METSTATIONS NUMBER(10,0),
	NB_CAISSES NUMBER(10,0),
	NB_BORNES_PEAGE_ENTREES NUMBER(10,0),
	FLAG_DOUBLE_ENTREES VARCHAR(10),
	NB_BORNES_PEAGE_SORTIES NUMBER(10,0),
	FLAG_DOUBLE_SORTIES VARCHAR(10),
	FLAG_LECTURE_PLAQUE VARCHAR(10),
	NB_ASCENSEURS NUMBER(10,0),
	MARQUE_ASCENSEURS VARCHAR(100),
	NB_ESCALIERS NUMBER(10,0),
	NB_PORTAILS NUMBER(10,0),
	NB_PORTES_COULISSANTES NUMBER(10,0),
	NB_RIDEAUX_MOTORISES NUMBER(10,0),
	NB_BORNES_IRVE NUMBER(10,0),
	FLAG_GUIDAGE_PLACE VARCHAR(10),
	GABARIT_STANDARD VARCHAR(50),
	DATE_CREATION TIMESTAMP_NTZ(9),
	NOM_CREATEUR VARCHAR(100),
	DATE_MODIFICATION TIMESTAMP_NTZ(9),
	NOM_MODIFICATEUR VARCHAR(100),
	DATE_DEBUT TIMESTAMP_NTZ(9),
	DATE_FIN VARCHAR(20),
	IS_ACTIVE VARCHAR(10),
	DATE_MISE_SERVICE_ASCENSEUR DATE,
	FLAG_LOCKERS VARCHAR(10)
);

create or replace TABLE T_R_FLAG (
	CODE_FLAG VARCHAR(10) NOT NULL,
	LIBELLE_FLAG VARCHAR(100),
	primary key (CODE_FLAG)
);

INSERT INTO T_R_FLAG (CODE_FLAG, LIBELLE_FLAG)
VALUES
(-1, 'Non'),
(0, 'Non renseigné'),
(1, 'Oui');



create or replace TABLE T_R_GESTION (
	CODE_GESTION VARCHAR(10) NOT NULL,
	LIBELLE_GESTION VARCHAR(100),
	primary key (CODE_GESTION)
);

INSERT INTO T_R_GESTION (CODE_GESTION, LIBELLE_GESTION)
VALUES
(0, 'Non renseigné'),
(1, 'Conv (Cinema)'),
(2, 'Conv (clinique)'),
(3, 'Conv (Ehpad)'),
(4, 'Conv (SNCF)'),
(5, 'Conv (Syndic)'),
(6, 'Indigo'),
(7, 'MTPK');


create or replace TABLE T_R_IMPACT_EVENEMENT (
	CODE_IMPACT NUMBER(38,0) NOT NULL,
	LIBELLE_IMPACT VARCHAR(200),
	NIVEAU_SEVERITE NUMBER(38,0),
	IS_ACTIVE BOOLEAN DEFAULT TRUE,
	primary key (CODE_IMPACT)
);

INSERT INTO T_R_IMPACT_EVENEMENT (CODE_IMPACT, LIBELLE_IMPACT, NIVEAU_SEVERITE, IS_ACTIVE)
VALUES
(1, 'Aucun impact notable', 1, TRUE),
(2, 'Ralentissement', 2, TRUE),
(3, 'Surcharge temporaire', 2, TRUE),
(4, 'Accès restreint', 3, TRUE),
(5, 'Déviation imposée', 3, TRUE),
(6, 'Fermeture partielle', 3, TRUE),
(7, 'Blocage total', 4, TRUE);


create or replace TABLE T_R_NATURE_JURIDIQUE (
	CODE_NATURE_JURIDIQUE VARCHAR(10) NOT NULL,
	LIBELLE_NATURE_JURIDIQUE VARCHAR(200),
	primary key (CODE_NATURE_JURIDIQUE)
);

INSERT INTO T_R_NATURE_JURIDIQUE (CODE_NATURE_JURIDIQUE, LIBELLE_NATURE_JURIDIQUE)
VALUES
(0, 'Non renseigné'),
(1, 'Convention'),
(2, 'Mise en affectation'),
(3, 'Pleine Propriété');


create or replace TABLE T_R_PARC (
	CODE_PARC VARCHAR(20) NOT NULL,
	NOM_PARC VARCHAR(200),
	ADRESSE_PARC VARCHAR(500),
	CODE_VILLE VARCHAR(10),
	CODE_SECTEUR VARCHAR(10),
	CODE_DISTRICT VARCHAR(10),
	CODE_TYPE_PARC VARCHAR(10),
	CODE_FLAG_FOURRIERE VARCHAR(10),
	CODE_FLAG_METSTATION VARCHAR(10),
	DATE_CREATION TIMESTAMP_NTZ(9),
	NOM_CREATEUR VARCHAR(100),
	DATE_MODIFICATION TIMESTAMP_NTZ(9),
	NOM_MODIFICATEUR VARCHAR(100),
	DATE_DEBUT TIMESTAMP_NTZ(9),
	DATE_FIN VARCHAR(20),
	IS_ACTIVE VARCHAR(10)
);

INSERT INTO T_R_PARC (CODE_PARC, NOM_PARC, ADRESSE_PARC, CODE_VILLE, CODE_SECTEUR, CODE_DISTRICT, CODE_TYPE_PARC, CODE_FLAG_FOURRIERE, CODE_FLAG_METSTATION, DATE_CREATION, NOM_CREATEUR, DATE_MODIFICATION, NOM_MODIFICATEUR, DATE_DEBUT, DATE_FIN, IS_ACTIVE)
VALUES
('H8MAI', '8 Mai 1985', 'Cours Maréchal Juin', '1', '1', '1', '3', '1', '1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('HACHA', 'Allees de Chartres', 'Allées de Bristol', '1', '1', '1', '2', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('HALOR', 'Alsace Lorraine', '21 Cours d''Alsace-Lorraine', '1', '1', '1', '3', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('CAMED', 'Amedee', '3 rue des échoppes', '1', '2', '3', '2', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('CDUNA', 'Amplitude', '35 rue Renée Buthaud', '2', '2', '3', '1', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('PAREN', 'Arena', 'Rue Pierre Kaldor/ avenue Alfonséa', '3', '3', '3', '1', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('CBEAU', 'Beaujon', 'Impasse des Cossus', '1', '2', '2', '1', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('CBERG', 'Bergonie', '220 cours de l''Argonne', '1', '2', '3', '2', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('HBONN', 'Bonnac', '42 Rue du Château d''eau', '1', '1', '1', '3', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('PBORD', 'Bord''Oh', '14 Rue Andrée Putman', '2', '3', '1', '3', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('PBRAZZ', 'Brazza', '202 rue des Queyries Bdx', '1', '3', '1', '2', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('HCAJU', 'Camille Jullian', '2 Pl. Camille Jullian', '1', '1', '1', '3', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('HCCME', 'CC Meriadeck', 'Rue Révérend Père Dieuzaide', '1', '1', '2', '3', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('HCMON', 'Cite Mondiale', '20 Quai des Chartrons', '1', '1', '1', '3', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('CCSEG', 'Croix de Seguey', '33 rue de la croix de Seguey', '1', '2', '2', '2', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('HFDME', 'Front du Medoc', 'Rue Robert Lateulade', '1', '1', '2', '1', '1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('HGAMB', 'Gambetta', 'Rue Edmond Michelet', '1', '1', '2', '3', '-1', '1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('CGSJE', 'Gare Saint Jean', '36 rue Charles Domercq', '1', '2', '3', '3', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('CGPAR', 'Grand Parc', 'Rue du Docteur Finlay', '1', '2', '2', '1', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('HGHOM', 'Grands Hommes', '3 Place des Grands Hommes', '1', '1', '2', '3', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('PLAHA', 'Laharpe', '59 Avenue d''Eysines', '4', '3', '2', '2', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('HLHOT', 'Lhote', '5-7 Rue Lhôte', '1', '1', '2', '3', '-1', '1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('PLIBE', 'Liberation', '43 Avenue de la Libération', '4', '3', '2', '1', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('PMEGA', 'Megarama', 'Allée Serr', '2', '3', '1', '3', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('PMERI', 'Merignac', 'Place Charles de Gaulle', '5', '3', '2', '3', '-1', '1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('CPALU', 'Paludate', 'Quai de Paludate', '1', '2', '3', '1', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('PPESS', 'Pessac', 'Rue des Poilus', '6', '3', '3', '3', '-1', '1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('HPBER', 'Pey Berland', 'Place Pey Berland', '1', '1', '1', '3', '-1', '1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('CPBDX', 'Porte de Bordeaux', '48 rue Général de Larminat', '1', '2', '3', '3', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('HREPU', 'Republique', 'Place de la République', '1', '1', '1', '3', '-1', '1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('CBEGL', 'Rue de Begles', '120 rue de Bègles', '1', '2', '3', '3', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('PSECH', 'Secheries', '13 Allée de Francs', '7', '3', '3', '1', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('PUGC', 'UGC', 'Allée du 7ème art', '8', '3', '3', '3', '-1', '-1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('HVICT', 'Victoire', 'Place de la Victoire', '1', '1', '1', '3', '-1', '1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE'),
('HVHUG', 'Victor Hugo', 'Place de la Ferme Richemont', '1', '1', '1', '1', '-1', '1', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), 'SYSTEM', CURRENT_TIMESTAMP(), NULL, 'TRUE');



create or replace TABLE T_R_PARC_EXPLOITATION (
	CODE_PARC VARCHAR(20) NOT NULL,
	NB_CAPACITE_VL_DT_THERMIQUE NUMBER(38,0),
	NB_CAPACITE_VL_DT_ELECTRIQUE NUMBER(38,0),
	NB_CAPACITE_VL_DT_PMR NUMBER(38,0),
	NB_CAPACITE_VL_DT_PMR_ELECTRIQUE NUMBER(38,0),
	NB_CAPACITE_VL_DT_MOTO NUMBER(38,0),
	NB_CAPACITE_VL_DT_VELO NUMBER(38,0),
	NB_CAPACITE_VL_DT_AUTRE NUMBER(38,0),
	COMMENTAIRE_AUTRE VARCHAR(500),
	NB_VOIES_ACCES NUMBER(38,0),
	NB_VOIES_SORTIES NUMBER(38,0),
	NB_ASCENCEUR NUMBER(38,0),
	NB_ESCALIER NUMBER(38,0),
	NB_PORTAIL NUMBER(38,0),
	NB_TRAPPE_EVACUATION_MOTORISEE NUMBER(38,0),
	NB_RIDEAUX_MOTORISEE NUMBER(38,0),
	DATE_CREATION TIMESTAMP_NTZ(9),
	NOM_CREATEUR VARCHAR(100),
	DATE_MODIFICATION TIMESTAMP_NTZ(9),
	NOM_MODIFICATEUR VARCHAR(100),
	DATE_DEBUT TIMESTAMP_NTZ(9),
	DATE_FIN VARCHAR(20),
	IS_ACTIVE BOOLEAN,
	NOM_PEAGEUR VARCHAR(100),
	NB_LECTEURS_PIETONS NUMBER(38,0),
	NB_LECTEURS_METSTATIONS NUMBER(38,0),
	NB_CAISSES NUMBER(38,0),
	NB_BORNES_PEAGES_ENTREES NUMBER(38,0),
	FLAG_DOUBLE_ENTREES VARCHAR(10),
	NB_BORNES_PEAGES_SORTIES NUMBER(38,0),
	FLAG_DOUBLE_SORTIES VARCHAR(10),
	FLAG_LECTURE_PLAQUE VARCHAR(10),
	MARQUE_ASCENCEUR VARCHAR(100),
	NB_PORTES_COULISSANTES NUMBER(38,0),
	NB_BORNES_IRVE NUMBER(38,0),
	NB_LOCKERS NUMBER(38,0),
	FLAG_GUIDAGE_PLACE VARCHAR(10),
	GABARIT_STANDARD VARCHAR(100),
	SURFACE NUMBER(38,0),
	DATE_MISE_EN_SERVICE_ASCENCEUR DATE,
	NIVEAU VARCHAR(50),
	NB_CAPACITE_VL NUMBER(10,0),
	NB_CAPACITE_EXPLOITEE NUMBER(10,0),
	NB_CAPACITE_TOTALE NUMBER(10,0)
);

create or replace TABLE T_R_PARC_JURIDIQUE (
	CODE_PARC VARCHAR(20) NOT NULL,
	MISE_EN_SERVICE VARCHAR(50),
	CODE_NATURE_JURIDIQUE VARCHAR(10),
	SIRET VARCHAR(50),
	CODE_FLAG_COPRO VARCHAR(10),
	DATE_CREATION TIMESTAMP_NTZ(9),
	NOM_CREATEUR VARCHAR(100),
	DATE_MODIFICATION TIMESTAMP_NTZ(9),
	NOM_MODIFICATEUR VARCHAR(100),
	DATE_DEBUT TIMESTAMP_NTZ(9),
	DATE_FIN VARCHAR(20),
	IS_ACTIVE BOOLEAN,
	TYPE_CONVENTION VARCHAR(200),
	NOM_TIERS_ATTENANT VARCHAR(200),
	NOM_COPRO VARCHAR(200)
);

create or replace TABLE T_R_PARC_SECURITE_INCENDIE (
	CODE_PARC VARCHAR(20) NOT NULL,
	EAE_SPRINKLEURS VARCHAR(50),
	NB_POSTES NUMBER(38,0),
	NB_TETES NUMBER(38,0),
	NB_EXTINCTEURS_TOTAL NUMBER(38,0),
	NB_BAC_A_SABLE NUMBER(38,0),
	DATE_CREATION TIMESTAMP_NTZ(9),
	NOM_CREATEUR VARCHAR(100),
	DATE_MODIFICATION TIMESTAMP_NTZ(9),
	NOM_MODIFICATEUR VARCHAR(100),
	DATE_DEBUT TIMESTAMP_NTZ(9),
	DATE_FIN VARCHAR(20),
	IS_ACTIVE BOOLEAN,
	FLAG_SSI VARCHAR(10),
	TYPE_SSI VARCHAR(100),
	MARQUE_SSI VARCHAR(100),
	NB_EXTRACTEURS NUMBER(38,0),
	NB_INSUFFLATEURS NUMBER(38,0),
	NB_COLONNES_SECHES NUMBER(38,0),
	NB_BAES NUMBER(38,0),
	TYPE_ALIMENTATION_BAES VARCHAR(100),
	NB_TRAPPE_EVACUATION_MOTORISEE NUMBER(38,0),
	TYPE_TARIFS_ELEC VARCHAR(100),
	FLAG_CELLULES_HT VARCHAR(10),
	FLAG_GROUPE_ELECTROGENE VARCHAR(10),
	CAPACITE_CUVE_FIOUL NUMBER(38,0),
	AVIS_COMMISSION VARCHAR(100),
	DATE_MISE_EN_SERVICE_SSI DATE,
	DATE_DERNIERE_COMMISSION DATE,
	FLAG_TGS VARCHAR(10),
	NB_PORTE_COMPARTIMENTAGE NUMBER(38,0),
	NB_DAI NUMBER(38,0),
	NB_DETECTION_CO_NO NUMBER(38,0)
);

create or replace TABLE T_R_PEAGEUR (
	CODE_PEAGEUR VARCHAR(10) NOT NULL,
	LIBELLE_PEAGEUR VARCHAR(100),
	primary key (CODE_PEAGEUR)
);

INSERT INTO T_R_PEAGEUR (CODE_PEAGEUR, LIBELLE_PEAGEUR)
VALUES
(1, 'DESIGNA'),
(2, 'HITACHI'),
(3, 'ORBILITY'),
(4, 'SKIDATA');


create or replace TABLE T_R_SECTEUR (
	CODE_SECTEUR VARCHAR(10) NOT NULL,
	LIBELLE_SECTEUR VARCHAR(100),
	primary key (CODE_SECTEUR)
);


INSERT INTO T_R_SECTEUR (CODE_SECTEUR, LIBELLE_SECTEUR)
VALUES
(0, 'Non renseigné'),
(1, 'Hypercentre'),
(2, 'Centre'),
(3, 'Periphérie');


create or replace TABLE T_R_TYPE_EVENEMENT (
	CODE_TYPE_EVENEMENT NUMBER(38,0) NOT NULL,
	LIBELLE_TYPE_EVENEMENT VARCHAR(200) NOT NULL,
	CATEGORIE VARCHAR(100) NOT NULL,
	IS_TRAVAUX BOOLEAN DEFAULT FALSE,
	IS_ACTIVE BOOLEAN DEFAULT TRUE,
	primary key (CODE_TYPE_EVENEMENT)
);


INSERT INTO T_R_TYPE_EVENEMENT (CODE_TYPE_EVENEMENT, LIBELLE_TYPE_EVENEMENT, CATEGORIE, IS_TRAVAUX, IS_ACTIVE)
VALUES
(1, 'Foire', 'Externe', FALSE, TRUE),
(2, 'Fête du fleuve', 'Externe', FALSE, TRUE),
(3, 'Fête de la musique', 'Externe', FALSE, TRUE),
(4, 'Manifestation', 'Externe', FALSE, TRUE),
(5, 'Marathon', 'Externe', FALSE, TRUE),
(6, 'Carnaval', 'Externe', FALSE, TRUE),
(7, 'Concert / Spectacle', 'Externe', FALSE, TRUE),
(8, 'Match / Événement sportif', 'Externe', FALSE, TRUE),
(9, 'Marché', 'Externe', FALSE, TRUE),
(10, 'Autre événement externe', 'Externe', FALSE, TRUE),
(11, 'Coupure internet', 'Technique', FALSE, TRUE),
(12, 'Barrière défectueuse', 'Technique', FALSE, TRUE),
(13, 'Travaux internes', 'Technique', TRUE, TRUE),
(14, 'Travaux externes', 'Technique', TRUE, TRUE),
(15, 'Indisponibilité de places', 'Technique', FALSE, TRUE),
(16, 'Panne équipement', 'Technique', FALSE, TRUE),
(17, 'Autre incident technique', 'Technique', FALSE, TRUE),
(18, 'Traveaux externes ville de Bordeaux', 'Technique', FALSE, TRUE);


create or replace TABLE T_R_TYPE_PARC (
	CODE_TYPE_PARC VARCHAR(10) NOT NULL,
	LIBELLE_TYPE_PARC VARCHAR(100),
	primary key (CODE_TYPE_PARC)
);



INSERT INTO T_R_TYPE_PARC (CODE_TYPE_PARC, LIBELLE_TYPE_PARC)
VALUES
(1, 'Infrastructure'),
(2, 'Superstructure'),
(3, 'Exterieur'),
(4, 'Infra et Superstructure');


create or replace TABLE T_R_VILLE (
	CODE_VILLE VARCHAR(10) NOT NULL,
	CODE_POSTAL VARCHAR(10),
	LIBELLE_VILLE VARCHAR(100),
	primary key (CODE_VILLE)
);

INSERT INTO T_R_VILLE (CODE_VILLE, CODE_POSTAL, LIBELLE_VILLE)
VALUES
(0, 'NR', 'Non renseigné'),
(1, '33000', 'Bordeaux'),
(2, '33100', 'Bordeaux'),
(3, '33270', 'Floirac'),
(4, '33110', 'Le Bouscat'),
(5, '33700', 'Merignac'),
(6, '33600', 'Pessac'),
(7, '33130', 'Bègles'),
(8, '33400', 'Talence');