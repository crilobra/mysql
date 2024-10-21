DROP TABLE nao.hashtag;
DROP TABLE nao.tweet;
CREATE TABLE nao.tweet (
    `id` int(11) NOT NULL AUTO_INCREMENT,
	id_tweet varchar(30) NOT NULL,
	texto varchar(1000) NULL,
	usuario varchar(100) NULL,
	fecha DATETIME NULL,
	retweets NUMERIC NULL,
	favoritos NUMERIC NULL,
	CONSTRAINT tweet_pk PRIMARY KEY (id)
) charset utf8mb4;
CREATE TABLE `hashtag` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hashtags` varchar(500) DEFAULT NULL,
  `id_tweets` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `hashtag_tweet_FK` (`id_tweets`),
  CONSTRAINT `hashtag_tweet_FK` FOREIGN KEY (`id_tweets`) REFERENCES `tweet` (`id`)
) charset utf8mb4;

