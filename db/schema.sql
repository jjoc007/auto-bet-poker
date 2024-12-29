CREATE DATABASE `poker`;


-- poker.flop definition

CREATE TABLE `flop` (
  `card_1` varchar(3) NOT NULL,
  `card_2` varchar(3) NOT NULL,
  `card_3` varchar(3) NOT NULL,
  `card_4` varchar(3) NOT NULL,
  `card_5` varchar(3) NOT NULL,
  `players` int NOT NULL,
  `win_probability` float NOT NULL,
  PRIMARY KEY (`card_1`,`card_2`,`card_3`,`card_4`,`card_5`,`players`)
);


-- poker.hand definition

CREATE TABLE `hand` (
  `card_1` varchar(3) NOT NULL,
  `card_2` varchar(3) NOT NULL,
  `players` int NOT NULL,
  `win_probability` float NOT NULL,
  PRIMARY KEY (`card_1`,`card_2`,`players`)
);


-- poker.game definition

CREATE TABLE `game` (
  `id` bigint NOT NULL,
  `players` tinyint NOT NULL,
  `player1` varchar(200) DEFAULT NULL,
  `player2` varchar(200) DEFAULT NULL,
  `player3` varchar(100) DEFAULT NULL,
  `player4` varchar(100) DEFAULT NULL,
  `player5` varchar(100) DEFAULT NULL,
  `player6` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
);


-- poker.player definition

CREATE TABLE `player` (
  `name` varchar(100) NOT NULL,
  `rating` smallint DEFAULT NULL,
  PRIMARY KEY (`name`)
);


-- poker.player_action definition

CREATE TABLE `player_action` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `player_name` varchar(100) NOT NULL,
  `phase` varchar(100) NOT NULL,
  `player_action` varchar(100) NOT NULL,
  `game_id` bigint NOT NULL,
  `card_1` varchar(100) DEFAULT NULL,
  `card_2` varchar(100) DEFAULT NULL,
  `card_3` varchar(100) DEFAULT NULL,
  `card_4` varchar(100) DEFAULT NULL,
  `card_5` varchar(100) DEFAULT NULL,
  `cash` varchar(100) DEFAULT NULL,
  `position` smallint DEFAULT NULL,
  `bet` varchar(100) DEFAULT NULL,
  `ante` varchar(100) DEFAULT NULL,
  `stack` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
);


CREATE TABLE friend_cards (
    id bigint AUTO_INCREMENT PRIMARY KEY,
    game_id bigint NOT NULL,
    player_name VARCHAR(255) NOT NULL,
    card_1 VARCHAR(10) NOT NULL,
    card_2 VARCHAR(10) NOT NULL
);