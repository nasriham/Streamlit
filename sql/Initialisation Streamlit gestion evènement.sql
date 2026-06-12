

USE ROLE R_DATA_ING_PRD;
USE DATABASE DB_REFERENTIEL_PRD;
USE SCHEMA S_REFERENTIEL;


-- ============================================================
-- SCRIPTS DE CREATION ET D'ALIMENTATION DES TABLES
-- Schema : DB_REFERENTIEL_PRD.S_REFERENTIEL
-- ============================================================

-- 1. CREATION DU SCHEMA
-- ============================================================
CREATE SCHEMA IF NOT EXISTS DB_REFERENTIEL_PRD.S_REFERENTIEL
    COMMENT = 'Schema pour la gestion des evenements MetPark';


-- 2. CREATION DES TABLES
-- ============================================================

-- Table des types d'événements
CREATE OR REPLACE TABLE DB_REFERENTIEL_PRD.S_REFERENTIEL.T_TYPE_EVENEMENT (
    CODE_TYPE_EVENEMENT NUMBER(38,0),
    LIBELLE_TYPE_EVENEMENT VARCHAR(200),
    CATEGORIE VARCHAR(100),
    IS_ACTIVE BOOLEAN
);

-- Table des lieux
CREATE OR REPLACE TABLE DB_REFERENTIEL_PRD.S_REFERENTIEL.T_LIEU_EVENEMENT (
    CODE_LIEU NUMBER(38,0),
    LIBELLE_LIEU VARCHAR(300),
    VILLE VARCHAR(100),
    CODE_POSTAL VARCHAR(10),
    IS_ACTIVE BOOLEAN
);

-- Table des impacts
CREATE OR REPLACE TABLE DB_REFERENTIEL_PRD.S_REFERENTIEL.T_IMPACT_EVENEMENT (
    CODE_IMPACT NUMBER(38,0),
    LIBELLE_IMPACT VARCHAR(200),
    NIVEAU_SEVERITE NUMBER(1,0),
    IS_ACTIVE BOOLEAN
);

-- Table principale des événements
CREATE OR REPLACE TABLE DB_REFERENTIEL_PRD.S_REFERENTIEL.T_BASE_EVENEMENT (
    CODE_EVENEMENT NUMBER(38,0) NOT NULL PRIMARY KEY,
    TITRE_EVENEMENT VARCHAR(300) NOT NULL,
    CODE_TYPE_EVENEMENT NUMBER(38,0) NOT NULL,
    CODE_LIEU NUMBER(38,0) NOT NULL,
    CODE_IMPACT NUMBER(38,0) NOT NULL,
    DATE_DEBUT TIMESTAMP_NTZ(9) NOT NULL,
    DATE_FIN TIMESTAMP_NTZ(9),
    COMMENTAIRE VARCHAR(2000),
    NOM_CREATEUR VARCHAR(100),
    NOM_MODIFICATEUR VARCHAR(100),
    DATE_CREATION TIMESTAMP_NTZ(9) DEFAULT CURRENT_TIMESTAMP(),
    DATE_MODIFICATION TIMESTAMP_NTZ(9),
    IS_ACTIVE BOOLEAN DEFAULT TRUE
);

-- Table de liaison événement <-> parking
CREATE OR REPLACE TABLE DB_REFERENTIEL_PRD.S_REFERENTIEL.T_EVENEMENT_PARC (
    CODE_EVENEMENT NUMBER(38,0),
    CODE_PARC VARCHAR(20),
    NOM_PARC VARCHAR(200)
);

-- Table de référence des parkings MetPark
CREATE OR REPLACE TABLE DB_REFERENTIEL_PRD.S_REFERENTIEL.T_PARKING (
    CODE_PARC NUMBER(38,0) PRIMARY KEY,
    NOM_PARC VARCHAR(200) NOT NULL,
    IS_ACTIVE BOOLEAN DEFAULT TRUE
);

-- Table d'historique (SCD2 - snapshot complet à chaque action)
CREATE OR REPLACE TABLE DB_REFERENTIEL_PRD.S_REFERENTIEL.T_HISTORIQUE_EVENEMENT (
    CODE_HISTORIQUE NUMBER(38,0) NOT NULL AUTOINCREMENT PRIMARY KEY,
    CODE_EVENEMENT NUMBER(38,0) NOT NULL,
    TITRE_EVENEMENT VARCHAR(300),
    TYPE_EVENEMENT VARCHAR(200),
    CATEGORIE VARCHAR(200),
    LIEU VARCHAR(200),
    VILLE VARCHAR(200),
    IMPACT VARCHAR(200),
    NIVEAU_SEVERITE NUMBER(38,0),
    DATE_DEBUT TIMESTAMP_NTZ(9),
    DATE_FIN TIMESTAMP_NTZ(9),
    COMMENTAIRE VARCHAR(2000),
    PARKINGS_IMPACTES VARCHAR(2000),
    IS_ACTIVE NUMBER(1,0) DEFAULT 1,
    MODIFIE_PAR VARCHAR(100),
    ACTION VARCHAR(50),
    DATE_DEBUT_VALIDITE TIMESTAMP_NTZ(9) DEFAULT CURRENT_TIMESTAMP(),
    DATE_FIN_VALIDITE TIMESTAMP_NTZ(9)
);

-- Séquence pour les CODE_EVENEMENT
CREATE OR REPLACE SEQUENCE DB_REFERENTIEL_PRD.S_REFERENTIEL.SEQ_EVENEMENT
    START WITH 1 INCREMENT BY 1 ORDER;


-- 3. ALIMENTATION DES DONNEES DE REFERENCE
-- ============================================================

-- Types d'événements
INSERT INTO DB_REFERENTIEL_PRD.S_REFERENTIEL.T_TYPE_EVENEMENT VALUES
(1, 'Travaux voirie', 'Infrastructure', TRUE),
(2, 'Travaux parking', 'Infrastructure', TRUE),
(3, 'Marathon / Course à pied', 'Événement sportif', TRUE),
(4, 'Match / Événement sportif', 'Événement sportif', TRUE),
(5, 'Foire / Marché', 'Événement commercial', TRUE),
(6, 'Concert / Spectacle', 'Événement culturel', TRUE),
(7, 'Fête municipale', 'Événement culturel', TRUE),
(8, 'Manifestation', 'Perturbation sociale', TRUE),
(9, 'Grève transports', 'Perturbation sociale', TRUE),
(10, 'Inondation', 'Catastrophe naturelle', TRUE),
(11, 'Tempête / Intempéries', 'Catastrophe naturelle', TRUE),
(12, 'Incendie', 'Catastrophe naturelle', TRUE),
(13, 'Accident véhicule', 'Incident', TRUE),
(14, 'Panne équipement majeure', 'Incident technique', TRUE),
(15, 'Fermeture administrative', 'Réglementaire', TRUE),
(16, 'Surcharge exceptionnelle', 'Affluence', TRUE),
(17, 'Période de vacances', 'Affluence', TRUE),
(18, 'Déviation circulation', 'Infrastructure', TRUE);

-- Lieux
INSERT INTO DB_REFERENTIEL_PRD.S_REFERENTIEL.T_LIEU_EVENEMENT VALUES
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
INSERT INTO DB_REFERENTIEL_PRD.S_REFERENTIEL.T_IMPACT_EVENEMENT VALUES
(1, 'Aucun impact notable', 1, TRUE),
(2, 'Ralentissement', 2, TRUE),
(3, 'Surcharge temporaire', 2, TRUE),
(4, 'Accès restreint', 3, TRUE),
(5, 'Déviation imposée', 3, TRUE),
(6, 'Fermeture partielle', 3, TRUE),
(7, 'Blocage total', 4, TRUE);

-- Parkings MetPark
INSERT INTO DB_REFERENTIEL_PRD.S_REFERENTIEL.T_PARKING VALUES
(76, 'ALLEES de CHARTRES', TRUE),
(77, 'ALLEES de CHARTRES Zone BUS', TRUE),
(69, 'ALSACE LORRAINE', TRUE),
(95, 'ARENA', TRUE),
(63, 'BEAUJON', TRUE),
(163, 'BEAUJON 2 Roues', TRUE),
(60, 'BERGONIE', TRUE),
(160, 'BERGONIE Zone Privée', TRUE),
(64, 'CROIX de SEGUEY', TRUE),
(74, 'GRAND PARC', TRUE),
(174, 'GRAND PARC 2 Roues', TRUE),
(75, 'GRAND PARC Moto', TRUE),
(65, 'LHOTE', TRUE),
(1, 'Parking Commun', TRUE),
(145, 'SECHERIE', TRUE),
(147, 'SECHERIE 2 Roues', TRUE),
(146, 'SECHERIE Moto', TRUE),
(170, 'VICTOR HUGO 2 Roues', TRUE),
(168, 'VICTOR HUGO Entresol', TRUE),
(68, 'VICTOR HUGO Etage', TRUE),
(169, 'VICTOR HUGO Sous-Sol', TRUE);






  ALTER GIT REPOSITORY DB_REFERENTIEL_DEV.S_REFERENTIEL.GIT_STREAMLIT_DEV FETCH;

CREATE OR REPLACE STREAMLIT DB_REFERENTIEL_DEV.S_REFERENTIEL.GESTION_EVENEMENTS
  ROOT_LOCATION = '@DB_REFERENTIEL_DEV.S_REFERENTIEL.GIT_STREAMLIT_DEV/branches/main/gestion-evenements'
  MAIN_FILE = 'streamlit_app.py'
  QUERY_WAREHOUSE = 'WH_HORS_PRODUCTION';

  ALTER STREAMLIT DB_REFERENTIEL_DEV.S_REFERENTIEL.GESTION_EVENEMENTS 
  SET TITLE = 'Gestion des évènements';


use role R_DATA_ING_PRD ;

CREATE OR REPLACE STREAMLIT DB_REFERENTIEL_PRD.S_REFERENTIEL.GESTION_EVENEMENTS
  ROOT_LOCATION = '@DB_REFERENTIEL_PRD.S_REFERENTIEL.GIT_STREAMLIT_PRD/branches/main/gestion-evenements'
  MAIN_FILE = 'streamlit_app.py'
  QUERY_WAREHOUSE = 'WH_HORS_PRODUCTION'
  TITLE = 'Gestion des évènements';


create or replace streamlit GESTION_EVENEMENTS
	root_location='@DB_REFERENTIEL_PRD.S_REFERENTIEL.GIT_STREAMLIT_PRD/branches/main/gestion-evenements'
	main_file='streamlit_app.py'
	query_warehouse='WH_HORS_PRODUCTION'
	title='Gestion des évènements';


SELECT GET_DDL('STREAMLIT', 'DB_REFERENTIEL_PRD.S_REFERENTIEL.GESTION_EVENEMENTS');