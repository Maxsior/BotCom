-- MySQL dump 10.13  Distrib 5.7.23, for Linux (x86_64)

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `msgs`
--

DROP TABLE IF EXISTS `msgs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `msgs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `text` text NOT NULL,
  `id_from` int(11) NOT NULL,
  `id_to` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `msgs_uids_id_from__fk` (`id_from`),
  KEY `msgs_uids_id_to__fk` (`id_to`),
  CONSTRAINT `msgs_uids_id_from__fk` FOREIGN KEY (`id_from`) REFERENCES `uids` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `msgs_uids_id_to__fk` FOREIGN KEY (`id_to`) REFERENCES `uids` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `msgs`
--

LOCK TABLES `msgs` WRITE;
/*!40000 ALTER TABLE `msgs` DISABLE KEYS */;
/*!40000 ALTER TABLE `msgs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `uids`
--

DROP TABLE IF EXISTS `uids`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `uids` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uid` varchar(20) NOT NULL,
  `current` int(11) DEFAULT NULL,
  `real_id` varchar(30) NOT NULL,
  `social` varchar(10) NOT NULL,
  `name` varchar(50) NOT NULL,
  `nick` varchar(30),
  PRIMARY KEY (`id`),
  UNIQUE KEY `uid` (`uid`),
  UNIQUE KEY `vk` (`real_id`),
  KEY `uids_uids_id_fk` (`current`),
  CONSTRAINT `uids_uids_id_fk` FOREIGN KEY (`current`) REFERENCES `uids` (`id`) ON DELETE SET NULL ON UPDATE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `words`
--

DROP TABLE IF EXISTS `words`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `words` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `word` varchar(10) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `word_unique` (`word`)
) ENGINE=InnoDB AUTO_INCREMENT=58 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `words`
--

LOCK TABLES `words` WRITE;
/*!40000 ALTER TABLE `words` DISABLE KEYS */;
INSERT INTO `words` VALUES (23,'Бальзам'),(48,'Барабан'),(41,'Бомба'),(45,'Весна'),(3,'Ворон'),(5,'Врач'),(38,'Герой'),(20,'Гитара'),(31,'Гриб'),(19,'Директор'),(4,'Домкрат'),(52,'Друг'),(28,'Звезда'),(44,'Зима'),(10,'Зритель'),(21,'Игра'),(50,'Карта'),(24,'Квадрат'),(51,'Кино'),(1,'Книга'),(16,'Кот'),(7,'Крик'),(53,'Кролик'),(32,'Круг'),(26,'Лев'),(43,'Лето'),(17,'Лосось'),(18,'Маргарин'),(2,'Мастер'),(47,'Мехмат'),(11,'Молоко'),(34,'Нога'),(56,'Океан'),(27,'Омар'),(46,'Осень'),(14,'Паук'),(25,'Пила'),(22,'Роза'),(35,'Рука'),(13,'Рыба'),(15,'Рыжик'),(8,'Сказка'),(42,'Снег'),(29,'Союз'),(9,'Стих'),(40,'Страница'),(55,'Сыр'),(12,'Танк'),(49,'Титаник'),(30,'Точка'),(33,'Трава'),(36,'Учитель'),(39,'Художник'),(6,'Царь'),(37,'Цифра'),(54,'Яблоко');
/*!40000 ALTER TABLE `words` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-03-06 13:40:18
