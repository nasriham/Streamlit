-- ============================================================
-- SCRIPTS DE CREATION ET D'ALIMENTATION DES TABLES
-- Schema : DB_REFERENTIEL_DEV.S_REFERENTIEL
-- Application : Gestion des évènements MetPark
-- ============================================================

-- 1. CREATION DU SCHEMA
-- ============================================================
CREATE SCHEMA IF NOT EXISTS DB_REFERENTIEL_DEV.S_REFERENTIEL
    COMMENT = 'Schema pour la gestion des evenements MetPark';


-- 2. CREATION DES TABLES
-- ============================================================

-- Table des types d'événements (Externe / Technique)
CREATE OR REPLACE TABLE DB_REFERENTIEL_DEV.S_REFERENTIEL.T_TYPE_EVENEMENT (
    CODE_TYPE_EVENEMENT NUMBER(38,0) PRIMARY KEY,
    LIBELLE_TYPE_EVENEMENT VARCHAR(200) NOT NULL,
    CATEGORIE VARCHAR(100) NOT NULL,  -- 'Externe' ou 'Technique'
    IS_TRAVAUX BOOLEAN DEFAULT FALSE, -- Flag pour activer les champs travaux
    IS_ACTIVE BOOLEAN DEFAULT TRUE
);

-- Table des descriptions/libellés prédéfinis par type
CREATE OR REPLACE TABLE DB_REFERENTIEL_DEV.S_REFERENTIEL.T_DESCRIPTION_EVENEMENT (
    CODE_DESCRIPTION NUMBER(38,0) PRIMARY KEY,
    CODE_TYPE_EVENEMENT NUMBER(38,0) NOT NULL,
    LIBELLE_DESCRIPTION VARCHAR(300) NOT NULL,
    IS_ACTIVE BOOLEAN DEFAULT TRUE
);

-- Table des lieux
CREATE OR REPLACE TABLE DB_REFERENTIEL_DEV.S_REFERENTIEL.T_LIEU_EVENEMENT (
    CODE_LIEU NUMBER(38,0) PRIMARY KEY,
    LIBELLE_LIEU VARCHAR(300) NOT NULL,
    VILLE VARCHAR(100),
    CODE_POSTAL VARCHAR(10),
    IS_ACTIVE BOOLEAN DEFAULT TRUE
);

-- Table des impacts
CREATE OR REPLACE TABLE DB_REFERENTIEL_DEV.S_REFERENTIEL.T_IMPACT_EVENEMENT (
    CODE_IMPACT NUMBER(38,0) PRIMARY KEY,
    LIBELLE_IMPACT VARCHAR(200) NOT NULL,
    NIVEAU_SEVERITE NUMBER(1,0),
    IS_ACTIVE BOOLEAN DEFAULT TRUE
);

-- Table de référence des parkings MetPark
CREATE OR REPLACE TABLE DB_REFERENTIEL_DEV.S_REFERENTIEL.T_PARKING (
    CODE_PARC NUMBER(38,0) PRIMARY KEY,
    NOM_PARC VARCHAR(200) NOT NULL,
    CAPACITE NUMBER(38,0),            -- Nombre total de places
    NB_PISTES_ENTREE NUMBER(38,0),    -- Nombre de pistes d'entrée
    NB_PISTES_SORTIE NUMBER(38,0),    -- Nombre de pistes de sortie
    IS_ACTIVE BOOLEAN DEFAULT TRUE
);

-- Table principale des événements
CREATE OR REPLACE TABLE DB_REFERENTIEL_DEV.S_REFERENTIEL.T_BASE_EVENEMENT (
    CODE_EVENEMENT NUMBER(38,0) NOT NULL PRIMARY KEY,
    TITRE_EVENEMENT VARCHAR(300) NOT NULL,
    CODE_TYPE_EVENEMENT NUMBER(38,0) NOT NULL,
    CODE_DESCRIPTION NUMBER(38,0),        -- Description prédéfinie (NULL si "Autre")
    DESCRIPTION_AUTRE VARCHAR(500),       -- Description libre si "Autre" sélectionné
    CODE_LIEU NUMBER(38,0),
    CODE_IMPACT NUMBER(38,0),
    DATE_DEBUT TIMESTAMP_NTZ(9) NOT NULL,
    DATE_FIN TIMESTAMP_NTZ(9),
    -- Journée partielle
    IS_JOURNEE_PARTIELLE BOOLEAN DEFAULT FALSE,
    CRENEAU VARCHAR(20),                  -- 'Matin', 'Après-midi', 'Nuit'
    -- Places impactées
    IS_PLACES_IMPACTEES BOOLEAN DEFAULT FALSE,
    NB_PLACES_IMPACTEES NUMBER(38,0),
    FERMETURE_TOTALE BOOLEAN DEFAULT FALSE,  -- Si TRUE, places dispo = 0
    -- Pistes impactées
    IS_PISTES_IMPACTEES BOOLEAN DEFAULT FALSE,
    NB_PISTES_ENTREE_FERMEES NUMBER(38,0),
    NB_PISTES_SORTIE_FERMEES NUMBER(38,0),
    -- Travaux spécifiques
    TYPE_TRAVAUX VARCHAR(20),             -- 'INTERNE', 'EXTERNE' (si type = travaux)
    CONTACT_INTERNE VARCHAR(200),
    CONTACT_EXTERNE VARCHAR(200),
    IS_TRAVAUX_PHASES BOOLEAN DEFAULT FALSE,
    -- Métadonnées
    COMMENTAIRE VARCHAR(2000),
    NOM_CREATEUR VARCHAR(100),
    NOM_MODIFICATEUR VARCHAR(100),
    DATE_CREATION TIMESTAMP_NTZ(9) DEFAULT CURRENT_TIMESTAMP(),
    DATE_MODIFICATION TIMESTAMP_NTZ(9),
    IS_ACTIVE BOOLEAN DEFAULT TRUE
);

-- Table de liaison événement <-> parking
CREATE OR REPLACE TABLE DB_REFERENTIEL_DEV.S_REFERENTIEL.T_EVENEMENT_PARC (
    CODE_EVENEMENT NUMBER(38,0) NOT NULL,
    CODE_PARC NUMBER(38,0) NOT NULL,
    NOM_PARC VARCHAR(200)
);

-- Table des phases de travaux
CREATE OR REPLACE TABLE DB_REFERENTIEL_DEV.S_REFERENTIEL.T_PHASE_TRAVAUX (
    CODE_PHASE NUMBER(38,0) NOT NULL AUTOINCREMENT PRIMARY KEY,
    CODE_EVENEMENT NUMBER(38,0) NOT NULL,
    NUMERO_PHASE NUMBER(38,0) NOT NULL,   -- Commence à 2
    DATE_DEBUT TIMESTAMP_NTZ(9) NOT NULL,
    DATE_FIN TIMESTAMP_NTZ(9) NOT NULL,
    NB_PLACES_IMPACTEES NUMBER(38,0),
    COMMENTAIRE VARCHAR(1000),            -- Secteur impacté
    DATE_CREATION TIMESTAMP_NTZ(9) DEFAULT CURRENT_TIMESTAMP()
);

-- Table d'historique (SCD2 - snapshot complet à chaque action)
CREATE OR REPLACE TABLE DB_REFERENTIEL_DEV.S_REFERENTIEL.T_HISTORIQUE_EVENEMENT (
    CODE_HISTORIQUE NUMBER(38,0) NOT NULL AUTOINCREMENT PRIMARY KEY,
    CODE_EVENEMENT NUMBER(38,0) NOT NULL,
    TITRE_EVENEMENT VARCHAR(300),
    TYPE_EVENEMENT VARCHAR(200),
    CATEGORIE VARCHAR(200),
    DESCRIPTION VARCHAR(500),
    LIEU VARCHAR(200),
    VILLE VARCHAR(200),
    IMPACT VARCHAR(200),
    NIVEAU_SEVERITE NUMBER(38,0),
    DATE_DEBUT TIMESTAMP_NTZ(9),
    DATE_FIN TIMESTAMP_NTZ(9),
    IS_JOURNEE_PARTIELLE BOOLEAN,
    CRENEAU VARCHAR(20),
    NB_PLACES_IMPACTEES NUMBER(38,0),
    FERMETURE_TOTALE BOOLEAN,
    NB_PISTES_ENTREE_FERMEES NUMBER(38,0),
    NB_PISTES_SORTIE_FERMEES NUMBER(38,0),
    TYPE_TRAVAUX VARCHAR(20),
    CONTACT_INTERNE VARCHAR(200),
    CONTACT_EXTERNE VARCHAR(200),
    IS_TRAVAUX_PHASES BOOLEAN,
    COMMENTAIRE VARCHAR(2000),
    PARKINGS_IMPACTES VARCHAR(2000),
    IS_ACTIVE NUMBER(1,0) DEFAULT 1,
    MODIFIE_PAR VARCHAR(100),
    ACTION VARCHAR(50),
    DATE_DEBUT_VALIDITE TIMESTAMP_NTZ(9) DEFAULT CURRENT_TIMESTAMP(),
    DATE_FIN_VALIDITE TIMESTAMP_NTZ(9)
);

-- Séquence pour les CODE_EVENEMENT
CREATE OR REPLACE SEQUENCE DB_REFERENTIEL_DEV.S_REFERENTIEL.SEQ_EVENEMENT
    START WITH 1 INCREMENT BY 1 ORDER;


-- 3. ALIMENTATION DES DONNEES DE REFERENCE
-- ============================================================

-- Types d'événements
INSERT INTO DB_REFERENTIEL_DEV.S_REFERENTIEL.T_TYPE_EVENEMENT VALUES
-- Événements externes / territoriaux
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
-- Événements techniques / opérationnels
(11, 'Coupure internet', 'Technique', FALSE, TRUE),
(12, 'Barrière défectueuse', 'Technique', FALSE, TRUE),
(13, 'Travaux internes', 'Technique', TRUE, TRUE),
(14, 'Travaux externes', 'Technique', TRUE, TRUE),
(15, 'Indisponibilité de places', 'Technique', FALSE, TRUE),
(16, 'Panne équipement', 'Technique', FALSE, TRUE),
(17, 'Autre incident technique', 'Technique', FALSE, TRUE);

-- Descriptions prédéfinies par type
INSERT INTO DB_REFERENTIEL_DEV.S_REFERENTIEL.T_DESCRIPTION_EVENEMENT VALUES
-- Foire
(1, 1, 'Foire aux vins', TRUE),
(2, 1, 'Foire aux plaisirs', TRUE),
(3, 1, 'Foire internationale de Bordeaux', TRUE),
(4, 1, 'Autre', TRUE),
-- Fête du fleuve
(5, 2, 'Fête du fleuve - édition annuelle', TRUE),
(6, 2, 'Autre', TRUE),
-- Fête de la musique
(7, 3, 'Fête de la musique - 21 juin', TRUE),
(8, 3, 'Autre', TRUE),
-- Manifestation
(9, 4, 'Manifestation syndicale', TRUE),
(10, 4, 'Manifestation étudiante', TRUE),
(11, 4, 'Gilets jaunes', TRUE),
(12, 4, 'Autre', TRUE),
-- Marathon
(13, 5, 'Marathon de Bordeaux', TRUE),
(14, 5, 'Semi-marathon', TRUE),
(15, 5, 'Course caritative', TRUE),
(16, 5, 'Autre', TRUE),
-- Carnaval
(17, 6, 'Carnaval des 2 rives', TRUE),
(18, 6, 'Autre', TRUE),
-- Concert / Spectacle
(19, 7, 'Concert Arkéa Arena', TRUE),
(20, 7, 'Concert Stade Matmut', TRUE),
(21, 7, 'Spectacle place des Quinconces', TRUE),
(22, 7, 'Autre', TRUE),
-- Match / Événement sportif
(23, 8, 'Match Girondins de Bordeaux', TRUE),
(24, 8, 'Match UBB (Rugby)', TRUE),
(25, 8, 'Autre', TRUE),
-- Marché
(26, 9, 'Marché des Capucins', TRUE),
(27, 9, 'Marché de Noël', TRUE),
(28, 9, 'Autre', TRUE),
-- Autre événement externe
(29, 10, 'Autre', TRUE),
-- Coupure internet
(30, 11, 'Coupure fibre', TRUE),
(31, 11, 'Panne réseau opérateur', TRUE),
(32, 11, 'Autre', TRUE),
-- Barrière défectueuse
(33, 12, 'Barrière entrée bloquée', TRUE),
(34, 12, 'Barrière sortie bloquée', TRUE),
(35, 12, 'Lecteur badge HS', TRUE),
(36, 12, 'Autre', TRUE),
-- Travaux internes
(37, 13, 'Peinture sol', TRUE),
(38, 13, 'Réfection éclairage', TRUE),
(39, 13, 'Maintenance ascenseur', TRUE),
(40, 13, 'Réparation ventilation', TRUE),
(41, 13, 'Autre', TRUE),
-- Travaux externes
(42, 14, 'Travaux voirie', TRUE),
(43, 14, 'Travaux réseaux (eau/gaz/électricité)', TRUE),
(44, 14, 'Travaux tramway', TRUE),
(45, 14, 'Autre', TRUE),
-- Indisponibilité de places
(46, 15, 'Réservation exceptionnelle', TRUE),
(47, 15, 'Occupation abusive', TRUE),
(48, 15, 'Autre', TRUE),
-- Panne équipement
(49, 16, 'Panne caisse automatique', TRUE),
(50, 16, 'Panne éclairage', TRUE),
(51, 16, 'Panne ventilation', TRUE),
(52, 16, 'Autre', TRUE),
-- Autre incident technique
(53, 17, 'Autre', TRUE);

-- Lieux
INSERT INTO DB_REFERENTIEL_DEV.S_REFERENTIEL.T_LIEU_EVENEMENT VALUES
(1, 'Centre-ville', 'Bordeaux', '33000', TRUE),
(2, 'Quartier gare Saint-Jean', 'Bordeaux', '33000', TRUE),
(3, 'Place de la Victoire', 'Bordeaux', '33000', TRUE),
(4, 'Quais de Bordeaux', 'Bordeaux', '33000', TRUE),
(5, 'Mériadeck', 'Bordeaux', '33000', TRUE),
(6, 'Gambetta', 'Bordeaux', '33000', TRUE),
(7, 'Chartrons', 'Bordeaux', '33000', TRUE),
(8, 'Lac / Parc des expositions', 'Bordeaux', '33300', TRUE),
(9, 'Rive droite - Bastide', 'Bordeaux', '33100', TRUE),
(10, 'Arena / Floirac', 'Floirac', '33270', TRUE),
(11, 'Pessac centre', 'Pessac', '33600', TRUE),
(12, 'Mérignac aéroport', 'Mérignac', '33700', TRUE),
(13, 'Talence université', 'Talence', '33400', TRUE);

-- Impacts
INSERT INTO DB_REFERENTIEL_DEV.S_REFERENTIEL.T_IMPACT_EVENEMENT VALUES
(1, 'Aucun impact notable', 1, TRUE),
(2, 'Ralentissement', 2, TRUE),
(3, 'Surcharge temporaire', 2, TRUE),
(4, 'Accès restreint', 3, TRUE),
(5, 'Déviation imposée', 3, TRUE),
(6, 'Fermeture partielle', 3, TRUE),
(7, 'Blocage total', 4, TRUE);

-- Parkings MetPark (avec capacités et pistes)
INSERT INTO DB_REFERENTIEL_DEV.S_REFERENTIEL.T_PARKING VALUES
(76, 'ALLEES de CHARTRES', 350, 2, 2, TRUE),
(77, 'ALLEES de CHARTRES Zone BUS', 20, 1, 1, TRUE),
(69, 'ALSACE LORRAINE', 450, 2, 2, TRUE),
(95, 'ARENA', 3000, 4, 4, TRUE),
(63, 'BEAUJON', 200, 1, 1, TRUE),
(163, 'BEAUJON 2 Roues', 30, 1, 1, TRUE),
(60, 'BERGONIE', 300, 2, 2, TRUE),
(160, 'BERGONIE Zone Privée', 50, 1, 1, TRUE),
(64, 'CROIX de SEGUEY', 250, 1, 1, TRUE),
(74, 'GRAND PARC', 500, 2, 2, TRUE),
(174, 'GRAND PARC 2 Roues', 40, 1, 1, TRUE),
(75, 'GRAND PARC Moto', 30, 1, 1, TRUE),
(65, 'LHOTE', 180, 1, 1, TRUE),
(1, 'Parking Commun', 100, 1, 1, TRUE),
(145, 'SECHERIE', 400, 2, 2, TRUE),
(147, 'SECHERIE 2 Roues', 35, 1, 1, TRUE),
(146, 'SECHERIE Moto', 25, 1, 1, TRUE),
(170, 'VICTOR HUGO 2 Roues', 40, 1, 1, TRUE),
(168, 'VICTOR HUGO Entresol', 200, 1, 1, TRUE),
(68, 'VICTOR HUGO Etage', 300, 2, 2, TRUE),
(169, 'VICTOR HUGO Sous-Sol', 250, 1, 1, TRUE);


-- 4. ALIMENTATION DES DONNEES EXEMPLE
-- ============================================================

-- Événements
INSERT INTO DB_REFERENTIEL_DEV.S_REFERENTIEL.T_BASE_EVENEMENT
(CODE_EVENEMENT, TITRE_EVENEMENT, CODE_TYPE_EVENEMENT, CODE_DESCRIPTION, DESCRIPTION_AUTRE,
 CODE_LIEU, CODE_IMPACT, DATE_DEBUT, DATE_FIN,
 IS_JOURNEE_PARTIELLE, CRENEAU,
 IS_PLACES_IMPACTEES, NB_PLACES_IMPACTEES, FERMETURE_TOTALE,
 IS_PISTES_IMPACTEES, NB_PISTES_ENTREE_FERMEES, NB_PISTES_SORTIE_FERMEES,
 TYPE_TRAVAUX, CONTACT_INTERNE, CONTACT_EXTERNE, IS_TRAVAUX_PHASES,
 COMMENTAIRE, NOM_CREATEUR, DATE_CREATION, IS_ACTIVE)
VALUES
-- Événement externe : Foire aux vins
(1, 'Foire aux vins 2025', 1, 1, NULL,
 8, 3, '2025-06-25 09:00:00', '2025-06-29 20:00:00',
 FALSE, NULL,
 FALSE, NULL, FALSE,
 FALSE, NULL, NULL,
 NULL, NULL, NULL, FALSE,
 'Événement au Parc des Expositions - forte affluence parking Lac', 'HNASRI', CURRENT_TIMESTAMP(), TRUE),

-- Événement externe : Marathon
(2, 'Marathon de Bordeaux 2025', 5, 13, NULL,
 4, 5, '2025-06-22 06:00:00', '2025-06-22 16:00:00',
 TRUE, 'Matin',
 FALSE, NULL, FALSE,
 FALSE, NULL, NULL,
 NULL, NULL, NULL, FALSE,
 'Fermeture des quais - déviation vers parkings périphériques', 'HNASRI', CURRENT_TIMESTAMP(), TRUE),

-- Événement externe : Concert
(3, 'Concert Arkéa Arena - Juillet', 7, 19, NULL,
 10, 3, '2025-07-05 18:00:00', '2025-07-05 23:59:00',
 TRUE, 'Nuit',
 FALSE, NULL, FALSE,
 FALSE, NULL, NULL,
 NULL, NULL, NULL, FALSE,
 'Affluence forte attendue - 15000 spectateurs', 'HNASRI', CURRENT_TIMESTAMP(), TRUE),

-- Événement technique : Coupure internet
(4, 'Coupure fibre Alsace Lorraine', 11, 30, NULL,
 1, 4, '2025-07-01 08:00:00', '2025-07-01 18:00:00',
 FALSE, NULL,
 FALSE, NULL, FALSE,
 FALSE, NULL, NULL,
 NULL, NULL, NULL, FALSE,
 'Intervention opérateur sur la fibre - TPE et barrières en mode dégradé', 'HNASRI', CURRENT_TIMESTAMP(), TRUE),

-- Travaux internes avec phasage
(5, 'Peinture sol Niveau -2 Victor Hugo', 13, 37, NULL,
 1, 6, '2025-07-01 00:00:00', '2025-09-30 23:59:00',
 FALSE, NULL,
 TRUE, 50, FALSE,
 FALSE, NULL, NULL,
 'INTERNE', 'Jean Dupont - 06.12.34.56.78', NULL, TRUE,
 'Peinture sol sur 3 mois - phases de 2 semaines avec rotation des zones', 'HNASRI', CURRENT_TIMESTAMP(), TRUE),

-- Travaux externes avec fermeture totale
(6, 'Travaux voirie rue Bergonié', 14, 42, NULL,
 1, 7, '2025-08-01 00:00:00', '2025-08-15 23:59:00',
 FALSE, NULL,
 TRUE, NULL, TRUE,
 TRUE, 1, 1,
 'EXTERNE', 'Marie Martin - 06.98.76.54.32', 'Eurovia - M. Robert - 05.56.12.34.56', FALSE,
 'Fermeture totale du parking Bergonié pendant les travaux de voirie', 'HNASRI', CURRENT_TIMESTAMP(), TRUE);

-- Liaison événements <-> parkings
INSERT INTO DB_REFERENTIEL_DEV.S_REFERENTIEL.T_EVENEMENT_PARC (CODE_EVENEMENT, CODE_PARC, NOM_PARC) VALUES
(1, 74, 'GRAND PARC'),
(1, 75, 'GRAND PARC Moto'),
(2, 76, 'ALLEES de CHARTRES'),
(2, 63, 'BEAUJON'),
(3, 95, 'ARENA'),
(4, 69, 'ALSACE LORRAINE'),
(5, 68, 'VICTOR HUGO Etage'),
(5, 169, 'VICTOR HUGO Sous-Sol'),
(6, 60, 'BERGONIE');

-- Phases de travaux pour l'événement 5 (Peinture sol Victor Hugo)
INSERT INTO DB_REFERENTIEL_DEV.S_REFERENTIEL.T_PHASE_TRAVAUX
(CODE_EVENEMENT, NUMERO_PHASE, DATE_DEBUT, DATE_FIN, NB_PLACES_IMPACTEES, COMMENTAIRE)
VALUES
(5, 2, '2025-07-15 00:00:00', '2025-07-31 23:59:00', 30, 'Zone A - Niveau -2 côté ascenseur'),
(5, 3, '2025-08-01 00:00:00', '2025-08-15 23:59:00', 50, 'Zone B - Niveau -2 côté escalier'),
(5, 4, '2025-08-16 00:00:00', '2025-08-31 23:59:00', 40, 'Zone C - Niveau -2 fond de parking'),
(5, 5, '2025-09-01 00:00:00', '2025-09-15 23:59:00', 25, 'Zone D - Niveau -2 rampe accès'),
(5, 6, '2025-09-16 00:00:00', '2025-09-30 23:59:00', 20, 'Finitions et marquages au sol');

-- Historique (snapshots de création)
INSERT INTO DB_REFERENTIEL_DEV.S_REFERENTIEL.T_HISTORIQUE_EVENEMENT
(CODE_EVENEMENT, TITRE_EVENEMENT, TYPE_EVENEMENT, CATEGORIE, DESCRIPTION,
 LIEU, VILLE, IMPACT, NIVEAU_SEVERITE, DATE_DEBUT, DATE_FIN,
 IS_JOURNEE_PARTIELLE, CRENEAU, NB_PLACES_IMPACTEES, FERMETURE_TOTALE,
 NB_PISTES_ENTREE_FERMEES, NB_PISTES_SORTIE_FERMEES,
 TYPE_TRAVAUX, CONTACT_INTERNE, CONTACT_EXTERNE, IS_TRAVAUX_PHASES,
 COMMENTAIRE, PARKINGS_IMPACTES, IS_ACTIVE, MODIFIE_PAR, ACTION, DATE_DEBUT_VALIDITE, DATE_FIN_VALIDITE)
VALUES
(1, 'Foire aux vins 2025', 'Foire', 'Externe', 'Foire aux vins',
 'Lac / Parc des expositions', 'Bordeaux', 'Surcharge temporaire', 2, '2025-06-25 09:00:00', '2025-06-29 20:00:00',
 FALSE, NULL, NULL, FALSE, NULL, NULL, NULL, NULL, NULL, FALSE,
 'Événement au Parc des Expositions - forte affluence parking Lac', 'GRAND PARC, GRAND PARC Moto', 1, 'HNASRI', 'CREATION', CURRENT_TIMESTAMP(), NULL),

(2, 'Marathon de Bordeaux 2025', 'Marathon', 'Externe', 'Marathon de Bordeaux',
 'Quais de Bordeaux', 'Bordeaux', 'Déviation imposée', 3, '2025-06-22 06:00:00', '2025-06-22 16:00:00',
 TRUE, 'Matin', NULL, FALSE, NULL, NULL, NULL, NULL, NULL, FALSE,
 'Fermeture des quais - déviation vers parkings périphériques', 'ALLEES de CHARTRES, BEAUJON', 1, 'HNASRI', 'CREATION', CURRENT_TIMESTAMP(), NULL),

(3, 'Concert Arkéa Arena - Juillet', 'Concert / Spectacle', 'Externe', 'Concert Arkéa Arena',
 'Arena / Floirac', 'Floirac', 'Surcharge temporaire', 2, '2025-07-05 18:00:00', '2025-07-05 23:59:00',
 TRUE, 'Nuit', NULL, FALSE, NULL, NULL, NULL, NULL, NULL, FALSE,
 'Affluence forte attendue - 15000 spectateurs', 'ARENA', 1, 'HNASRI', 'CREATION', CURRENT_TIMESTAMP(), NULL),

(4, 'Coupure fibre Alsace Lorraine', 'Coupure internet', 'Technique', 'Coupure fibre',
 'Centre-ville', 'Bordeaux', 'Accès restreint', 3, '2025-07-01 08:00:00', '2025-07-01 18:00:00',
 FALSE, NULL, NULL, FALSE, NULL, NULL, NULL, NULL, NULL, FALSE,
 'Intervention opérateur sur la fibre - TPE et barrières en mode dégradé', 'ALSACE LORRAINE', 1, 'HNASRI', 'CREATION', CURRENT_TIMESTAMP(), NULL),

(5, 'Peinture sol Niveau -2 Victor Hugo', 'Travaux internes', 'Technique', 'Peinture sol',
 'Centre-ville', 'Bordeaux', 'Fermeture partielle', 3, '2025-07-01 00:00:00', '2025-09-30 23:59:00',
 FALSE, NULL, 50, FALSE, NULL, NULL, 'INTERNE', 'Jean Dupont - 06.12.34.56.78', NULL, TRUE,
 'Peinture sol sur 3 mois - phases de 2 semaines avec rotation des zones', 'VICTOR HUGO Etage, VICTOR HUGO Sous-Sol', 1, 'HNASRI', 'CREATION', CURRENT_TIMESTAMP(), NULL),

(6, 'Travaux voirie rue Bergonié', 'Travaux externes', 'Technique', 'Travaux voirie',
 'Centre-ville', 'Bordeaux', 'Blocage total', 4, '2025-08-01 00:00:00', '2025-08-15 23:59:00',
 FALSE, NULL, NULL, TRUE, 1, 1, 'EXTERNE', 'Marie Martin - 06.98.76.54.32', 'Eurovia - M. Robert - 05.56.12.34.56', FALSE,
 'Fermeture totale du parking Bergonié pendant les travaux de voirie', 'BERGONIE', 1, 'HNASRI', 'CREATION', CURRENT_TIMESTAMP(), NULL);

-- Mise à jour de la séquence pour commencer après les données insérées
ALTER SEQUENCE DB_REFERENTIEL_DEV.S_REFERENTIEL.SEQ_EVENEMENT SET START WITH 7;
