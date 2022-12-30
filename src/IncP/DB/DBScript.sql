-- MySQL dump 10.13  Distrib 5.5.27, for FreeBSD8.0 (i386)
--
-- Host: localhost    Database: app_front_office2
-- ------------------------------------------------------
-- Server version	5.5.27-log

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
-- Table structure for table `Fo_Doc`
--

DROP TABLE IF EXISTS `Fo_Doc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Fo_Doc` (
  `Doc_ID` int(11) NOT NULL AUTO_INCREMENT,
  `Meta_ID` int(11) NOT NULL COMMENT '��� ���� ���������',
  `DocChild_ID` int(11) NOT NULL COMMENT '��� ���������',
  `Deleted` tinyint(1) DEFAULT '0' COMMENT '������� �� ��������',
  `Firm` int(11) NOT NULL COMMENT '����������� ����� �����',
  `Code` varchar(12) CHARACTER SET cp1251 NOT NULL COMMENT '����� ��������� ������������� �������������',
  `Description` text CHARACTER SET cp1251 COMMENT '��������',
  `DateCreate` datetime NOT NULL COMMENT '���� ��������',
  `DateModify` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT '���� ���������� ���������',
  `DateDoc` datetime NOT NULL COMMENT '���� �� ������� �������� ��������',
  `BasedOn_ID` int(11) DEFAULT NULL COMMENT '������ �� ��������� ������ ���������',
  PRIMARY KEY (`Doc_ID`),
  UNIQUE KEY `ID` (`Doc_ID`),
  UNIQUE KEY `Code` (`Code`),
  UNIQUE KEY `Code_2` (`Code`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COMMENT='������� ��������.\r\n��� ��������� ����������� �� ����';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Fo_Doc`
--

LOCK TABLES `Fo_Doc` WRITE;
/*!40000 ALTER TABLE `Fo_Doc` DISABLE KEYS */;
INSERT INTO `Fo_Doc` VALUES (1,1,1,0,1,'1',NULL,'0000-00-00 00:00:00','0000-00-00 00:00:00','0000-00-00 00:00:00',NULL),(2,2,2,0,2,'2',NULL,'0000-00-00 00:00:00','0000-00-00 00:00:00','0000-00-00 00:00:00',NULL);
/*!40000 ALTER TABLE `Fo_Doc` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Fo_Doc_IntegrationMinus`
--

DROP TABLE IF EXISTS `Fo_Doc_IntegrationMinus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Fo_Doc_IntegrationMinus` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Store_ID` int(11) NOT NULL COMMENT '����� �� ������� ����������',
  `Ware_ID` int(11) NOT NULL COMMENT '�����-������� ��� ������������',
  `Qty` decimal(11,0) DEFAULT NULL COMMENT '���������� ����������',
  `Weight` double(15,3) DEFAULT NULL COMMENT '���� �������, �� ����� ���',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='��������: ���������������� ������';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Fo_Doc_IntegrationMinus`
--

LOCK TABLES `Fo_Doc_IntegrationMinus` WRITE;
/*!40000 ALTER TABLE `Fo_Doc_IntegrationMinus` DISABLE KEYS */;
/*!40000 ALTER TABLE `Fo_Doc_IntegrationMinus` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Fo_Doc_IntegrationMinus_Table_Ware`
--

DROP TABLE IF EXISTS `Fo_Doc_IntegrationMinus_Table_Ware`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Fo_Doc_IntegrationMinus_Table_Ware` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Parent_ID` int(11) DEFAULT NULL,
  `Wares_ID` int(11) NOT NULL COMMENT '�����',
  `Unit_ID` int(11) DEFAULT NULL COMMENT '������� ���������',
  `Factor` double(15,3) DEFAULT NULL COMMENT '�����������',
  `Qty` double(15,3) NOT NULL COMMENT '���������� ������',
  `Price` double(15,3) NOT NULL COMMENT '���� ������',
  `Sum` double(15,3) NOT NULL COMMENT '�����',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='���.�����: �����\r\n��������: ���������������� (Fo_Doc_Integra';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Fo_Doc_IntegrationMinus_Table_Ware`
--

LOCK TABLES `Fo_Doc_IntegrationMinus_Table_Ware` WRITE;
/*!40000 ALTER TABLE `Fo_Doc_IntegrationMinus_Table_Ware` DISABLE KEYS */;
/*!40000 ALTER TABLE `Fo_Doc_IntegrationMinus_Table_Ware` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Fo_Doc_IntegrationPlus`
--

DROP TABLE IF EXISTS `Fo_Doc_IntegrationPlus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Fo_Doc_IntegrationPlus` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Store_ID` int(11) NOT NULL COMMENT '����� �� ������� ����������',
  `Ware_ID` int(11) NOT NULL COMMENT '�����-������� ��� ������������',
  `Qty` decimal(11,0) DEFAULT NULL COMMENT '���������� ����������',
  `Weight` double(15,3) DEFAULT NULL COMMENT '���� �������, �� ����� ���',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='��������: ������������ ������';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Fo_Doc_IntegrationPlus`
--

LOCK TABLES `Fo_Doc_IntegrationPlus` WRITE;
/*!40000 ALTER TABLE `Fo_Doc_IntegrationPlus` DISABLE KEYS */;
/*!40000 ALTER TABLE `Fo_Doc_IntegrationPlus` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Fo_Doc_IntegrationPlus_Ware`
--

DROP TABLE IF EXISTS `Fo_Doc_IntegrationPlus_Ware`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Fo_Doc_IntegrationPlus_Ware` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Parent_ID` int(11) DEFAULT NULL,
  `Wares_ID` int(11) NOT NULL COMMENT '�����',
  `Unit_ID` int(11) DEFAULT NULL COMMENT '������� ���������',
  `Factor` double(15,3) DEFAULT NULL COMMENT '�����������',
  `Qty` double(15,3) NOT NULL COMMENT '���������� ������',
  `Price` double(15,3) NOT NULL COMMENT '���� ������',
  `Sum` double(15,3) NOT NULL COMMENT '�����',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='���.�����: �����\r\n��������: ������������. (Fo_Doc_Integratio';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Fo_Doc_IntegrationPlus_Ware`
--

LOCK TABLES `Fo_Doc_IntegrationPlus_Ware` WRITE;
/*!40000 ALTER TABLE `Fo_Doc_IntegrationPlus_Ware` DISABLE KEYS */;
/*!40000 ALTER TABLE `Fo_Doc_IntegrationPlus_Ware` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Fo_Doc_Inventory`
--

DROP TABLE IF EXISTS `Fo_Doc_Inventory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Fo_Doc_Inventory` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Parent_ID` int(11) NOT NULL,
  `Store_ID` int(11) NOT NULL COMMENT '��� ������',
  `Chairman_ID` int(11) DEFAULT NULL COMMENT '��� ����� �������. Ref_Emploee',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COMMENT='��������: �������������� ';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Fo_Doc_Inventory`
--

LOCK TABLES `Fo_Doc_Inventory` WRITE;
/*!40000 ALTER TABLE `Fo_Doc_Inventory` DISABLE KEYS */;
INSERT INTO `Fo_Doc_Inventory` VALUES (1,0,1,NULL),(2,0,2,NULL);
/*!40000 ALTER TABLE `Fo_Doc_Inventory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Fo_Doc_Inventory_Table_Event`
--

DROP TABLE IF EXISTS `Fo_Doc_Inventory_Table_Event`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Fo_Doc_Inventory_Table_Event` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Wares_ID` int(11) NOT NULL COMMENT '��� ������',
  `EventDate` datetime NOT NULL COMMENT '����� �������� ������',
  `entered_rest` decimal(15,4) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  KEY `event_time` (`EventDate`),
  KEY `products_id` (`Wares_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Fo_Doc_Inventory_Table_Event`
--

LOCK TABLES `Fo_Doc_Inventory_Table_Event` WRITE;
/*!40000 ALTER TABLE `Fo_Doc_Inventory_Table_Event` DISABLE KEYS */;
/*!40000 ALTER TABLE `Fo_Doc_Inventory_Table_Event` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Fo_Doc_Inventory_Table_Ware`
--

DROP TABLE IF EXISTS `Fo_Doc_Inventory_Table_Ware`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Fo_Doc_Inventory_Table_Ware` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Parent_ID` int(11) NOT NULL,
  `Wares_ID` int(11) NOT NULL COMMENT '��� ������',
  `Unit_ID` int(11) DEFAULT NULL COMMENT '������� ���������',
  `Factor` decimal(11,0) DEFAULT NULL COMMENT '����������',
  `Price` double(15,3) NOT NULL COMMENT '����������� ����',
  `BugQty` double(15,3) DEFAULT NULL COMMENT '���������� �� �����������',
  `BugSum` double(15,3) DEFAULT NULL COMMENT '����� �� �����������',
  `FactQty` double(15,3) DEFAULT NULL COMMENT '����������� ����������',
  `FactSum` double(15,3) DEFAULT NULL COMMENT '����������� �����',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='���.�����: ������\r\n��������: �������������� (Fo_Doc_Inventor';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Fo_Doc_Inventory_Table_Ware`
--

LOCK TABLES `Fo_Doc_Inventory_Table_Ware` WRITE;
/*!40000 ALTER TABLE `Fo_Doc_Inventory_Table_Ware` DISABLE KEYS */;
/*!40000 ALTER TABLE `Fo_Doc_Inventory_Table_Ware` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Fo_Doc_Invoice`
--

DROP TABLE IF EXISTS `Fo_Doc_Invoice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Fo_Doc_Invoice` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='��������: ����';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Fo_Doc_Invoice`
--

LOCK TABLES `Fo_Doc_Invoice` WRITE;
/*!40000 ALTER TABLE `Fo_Doc_Invoice` DISABLE KEYS */;
/*!40000 ALTER TABLE `Fo_Doc_Invoice` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Fo_Doc_Invoice_Table_Ware`
--

DROP TABLE IF EXISTS `Fo_Doc_Invoice_Table_Ware`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Fo_Doc_Invoice_Table_Ware` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Parent_ID` int(11) DEFAULT NULL,
  `Wares_ID` int(11) NOT NULL,
  `Unint_ID` int(11) NOT NULL COMMENT '������� ���������',
  `Qty` double(15,3) NOT NULL COMMENT '���������� ������',
  `Factor` double(15,3) NOT NULL DEFAULT '1.000' COMMENT '�����������',
  `Price` double(15,3) NOT NULL COMMENT '���� ������',
  `Discount` double(15,3) DEFAULT NULL COMMENT '������ �� ������',
  `Sum` double(15,3) NOT NULL COMMENT '�����',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='���.�����: ������\r\n��������: ����. (Fo_Doc_Invoice.ID=Parent';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Fo_Doc_Invoice_Table_Ware`
--

LOCK TABLES `Fo_Doc_Invoice_Table_Ware` WRITE;
/*!40000 ALTER TABLE `Fo_Doc_Invoice_Table_Ware` DISABLE KEYS */;
/*!40000 ALTER TABLE `Fo_Doc_Invoice_Table_Ware` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Fo_Doc_MoneyMinus`
--

DROP TABLE IF EXISTS `Fo_Doc_MoneyMinus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Fo_Doc_MoneyMinus` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `MoneyBox_ID` int(11) DEFAULT NULL COMMENT '�����',
  `Customer_ID` int(11) NOT NULL COMMENT '� ���� ��������',
  `Currency_ID` int(11) NOT NULL COMMENT '������',
  `Sum` double(15,3) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='��������: ������ �����';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Fo_Doc_MoneyMinus`
--

LOCK TABLES `Fo_Doc_MoneyMinus` WRITE;
/*!40000 ALTER TABLE `Fo_Doc_MoneyMinus` DISABLE KEYS */;
/*!40000 ALTER TABLE `Fo_Doc_MoneyMinus` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Fo_Doc_MoneyPlus`
--

DROP TABLE IF EXISTS `Fo_Doc_MoneyPlus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Fo_Doc_MoneyPlus` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `MoneyBox_ID` int(11) DEFAULT NULL COMMENT '�����',
  `Customer_ID` int(11) NOT NULL COMMENT '� ���� ��������',
  `Currency_ID` int(11) NOT NULL COMMENT '������',
  `Sum` double(15,3) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='��������: ������ �����\r\n';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Fo_Doc_MoneyPlus`
--

LOCK TABLES `Fo_Doc_MoneyPlus` WRITE;
/*!40000 ALTER TABLE `Fo_Doc_MoneyPlus` DISABLE KEYS */;
/*!40000 ALTER TABLE `Fo_Doc_MoneyPlus` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Fo_Doc_Purchase`
--

DROP TABLE IF EXISTS `Fo_Doc_Purchase`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Fo_Doc_Purchase` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Customer_ID` int(11) NOT NULL COMMENT '� ���� ��������',
  `Store_ID` int(11) NOT NULL COMMENT '����� �� ������� ����������',
  `Currency_ID` int(11) NOT NULL COMMENT '������',
  `CustomerDocNum` varchar(16) DEFAULT NULL COMMENT '����� ��������� � ����������',
  `DatePay` date DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COMMENT='��������: ������� ������';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Fo_Doc_Purchase`
--

LOCK TABLES `Fo_Doc_Purchase` WRITE;
/*!40000 ALTER TABLE `Fo_Doc_Purchase` DISABLE KEYS */;
INSERT INTO `Fo_Doc_Purchase` VALUES (1,1,2,4,NULL,NULL),(2,2,2,2,NULL,NULL);
/*!40000 ALTER TABLE `Fo_Doc_Purchase` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Fo_Doc_Purchase_Table_Ware`
--

DROP TABLE IF EXISTS `Fo_Doc_Purchase_Table_Ware`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Fo_Doc_Purchase_Table_Ware` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Parent_ID` int(11) DEFAULT NULL,
  `Wares_ID` int(11) NOT NULL,
  `Unit_ID` int(11) DEFAULT NULL COMMENT '������� ���������',
  `Factor` double(15,3) NOT NULL DEFAULT '1.000' COMMENT '����������',
  `Qty` double(15,3) NOT NULL,
  `Price` double(15,3) NOT NULL,
  `Discount` double(15,3) DEFAULT NULL COMMENT '������',
  `Sum` double(15,3) NOT NULL,
  `Serials` mediumtext COMMENT '�������� ������',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='���.�����: ������\r\n��������: ������ ������ (Fo_Doc_Purchase.';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Fo_Doc_Purchase_Table_Ware`
--

LOCK TABLES `Fo_Doc_Purchase_Table_Ware` WRITE;
/*!40000 ALTER TABLE `Fo_Doc_Purchase_Table_Ware` DISABLE KEYS */;
/*!40000 ALTER TABLE `Fo_Doc_Purchase_Table_Ware` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Fo_Doc_Remain`
--

DROP TABLE IF EXISTS `Fo_Doc_Remain`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Fo_Doc_Remain` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Store_ID` int(11) NOT NULL COMMENT '��� ������',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='��������: ���� �������� ������';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Fo_Doc_Remain`
--

LOCK TABLES `Fo_Doc_Remain` WRITE;
/*!40000 ALTER TABLE `Fo_Doc_Remain` DISABLE KEYS */;
/*!40000 ALTER TABLE `Fo_Doc_Remain` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Fo_Doc_Remain_Table_Ware`
--

DROP TABLE IF EXISTS `Fo_Doc_Remain_Table_Ware`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Fo_Doc_Remain_Table_Ware` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Parent_ID` int(11) DEFAULT NULL,
  `Wares_ID` int(11) NOT NULL COMMENT '�����',
  `Unit_ID` int(11) DEFAULT NULL COMMENT '������� ���������',
  `Factor` double(15,3) NOT NULL DEFAULT '1.000' COMMENT '����������',
  `Qty` double(15,3) NOT NULL,
  `Price` double(15,3) NOT NULL,
  `Sum` double(15,3) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='���.�����: ������\r\n��������: ���� ��������';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Fo_Doc_Remain_Table_Ware`
--

LOCK TABLES `Fo_Doc_Remain_Table_Ware` WRITE;
/*!40000 ALTER TABLE `Fo_Doc_Remain_Table_Ware` DISABLE KEYS */;
/*!40000 ALTER TABLE `Fo_Doc_Remain_Table_Ware` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Fo_Doc_ReturnRetail`
--

DROP TABLE IF EXISTS `Fo_Doc_ReturnRetail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Fo_Doc_ReturnRetail` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Customer_ID` int(11) NOT NULL COMMENT '� ���� ��������',
  `Store_ID` int(11) NOT NULL COMMENT '����� �� ������� ����������',
  `Currency_ID` int(11) NOT NULL COMMENT '������',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='��������: ������� ������';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Fo_Doc_ReturnRetail`
--

LOCK TABLES `Fo_Doc_ReturnRetail` WRITE;
/*!40000 ALTER TABLE `Fo_Doc_ReturnRetail` DISABLE KEYS */;
/*!40000 ALTER TABLE `Fo_Doc_ReturnRetail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Fo_Doc_ReturnRetail_Table_Ware`
--

DROP TABLE IF EXISTS `Fo_Doc_ReturnRetail_Table_Ware`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Fo_Doc_ReturnRetail_Table_Ware` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Parent_ID` int(11) DEFAULT NULL,
  `Wares_ID` int(11) NOT NULL,
  `Unit_ID` int(11) DEFAULT NULL COMMENT '������� ���������',
  `Factor` double(15,3) NOT NULL DEFAULT '1.000' COMMENT '����������',
  `Qty` double(15,3) NOT NULL,
  `Price` double(15,3) NOT NULL,
  `Discount` double(15,3) DEFAULT NULL COMMENT '������',
  `Sum` double(15,3) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='���.�����: ������\r\n��������: ������ ������ (Fo_Doc_Purchase.';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Fo_Doc_ReturnRetail_Table_Ware`
--

LOCK TABLES `Fo_Doc_ReturnRetail_Table_Ware` WRITE;
/*!40000 ALTER TABLE `Fo_Doc_ReturnRetail_Table_Ware` DISABLE KEYS */;
/*!40000 ALTER TABLE `Fo_Doc_ReturnRetail_Table_Ware` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Fo_Doc_ReturnToSupplier`
--

DROP TABLE IF EXISTS `Fo_Doc_ReturnToSupplier`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Fo_Doc_ReturnToSupplier` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Customer_ID` int(11) NOT NULL COMMENT '� ���� ��������',
  `Store_ID` int(11) NOT NULL COMMENT '����� �� ������� ����������',
  `Currency_ID` int(11) NOT NULL COMMENT '������',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='��������: ������� ������';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Fo_Doc_ReturnToSupplier`
--

LOCK TABLES `Fo_Doc_ReturnToSupplier` WRITE;
/*!40000 ALTER TABLE `Fo_Doc_ReturnToSupplier` DISABLE KEYS */;
/*!40000 ALTER TABLE `Fo_Doc_ReturnToSupplier` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Fo_Doc_ReturnToSupplier_Table_Ware`
--

DROP TABLE IF EXISTS `Fo_Doc_ReturnToSupplier_Table_Ware`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Fo_Doc_ReturnToSupplier_Table_Ware` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Parent_ID` int(11) DEFAULT NULL,
  `Wares_ID` int(11) NOT NULL,
  `Unit_ID` int(11) DEFAULT NULL COMMENT '������� ���������',
  `Factor` double(15,3) NOT NULL DEFAULT '1.000' COMMENT '����������',
  `Qty` double(15,3) NOT NULL,
  `Price` double(15,3) NOT NULL,
  `Discount` double(15,3) DEFAULT NULL COMMENT '������',
  `Sum` double(15,3) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='���.�����: ������\r\n��������: ������ ������ (Fo_Doc_Purchase.';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Fo_Doc_ReturnToSupplier_Table_Ware`
--

LOCK TABLES `Fo_Doc_ReturnToSupplier_Table_Ware` WRITE;
/*!40000 ALTER TABLE `Fo_Doc_ReturnToSupplier_Table_Ware` DISABLE KEYS */;
/*!40000 ALTER TABLE `Fo_Doc_ReturnToSupplier_Table_Ware` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Fo_Doc_Sale`
--

DROP TABLE IF EXISTS `Fo_Doc_Sale`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Fo_Doc_Sale` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Customer_ID` int(11) NOT NULL COMMENT '� ���� ��������',
  `Store_ID` int(11) NOT NULL COMMENT '����� �� ������� ����������',
  `Currency_ID` int(11) NOT NULL COMMENT '������',
  `Middleman_ID` int(11) DEFAULT NULL COMMENT '���������',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='��������: ������� ������';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Fo_Doc_Sale`
--

LOCK TABLES `Fo_Doc_Sale` WRITE;
/*!40000 ALTER TABLE `Fo_Doc_Sale` DISABLE KEYS */;
/*!40000 ALTER TABLE `Fo_Doc_Sale` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Fo_Doc_Sale_Table_Ware`
--

DROP TABLE IF EXISTS `Fo_Doc_Sale_Table_Ware`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Fo_Doc_Sale_Table_Ware` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Parent_ID` int(11) DEFAULT NULL,
  `Wares_ID` int(11) NOT NULL,
  `Unit_ID` int(11) DEFAULT NULL COMMENT '������� ���������',
  `Factor` double(15,3) DEFAULT NULL COMMENT '����������',
  `Qty` double(15,3) NOT NULL,
  `Price` double(15,3) NOT NULL,
  `Discount` double(15,3) DEFAULT NULL COMMENT '������',
  `Sum` double(15,3) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='���.�����: ������\r\n��������: ������� ������ (Fo_Doc_Sale.ID=';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Fo_Doc_Sale_Table_Ware`
--

LOCK TABLES `Fo_Doc_Sale_Table_Ware` WRITE;
/*!40000 ALTER TABLE `Fo_Doc_Sale_Table_Ware` DISABLE KEYS */;
/*!40000 ALTER TABLE `Fo_Doc_Sale_Table_Ware` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Fo_Doc_Shift`
--

DROP TABLE IF EXISTS `Fo_Doc_Shift`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Fo_Doc_Shift` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `StoreFrom_ID` int(11) NOT NULL COMMENT '����� � �������� ����������',
  `StoreTo_ID` int(11) NOT NULL COMMENT '����� ���� ����������',
  `WhoFrom` int(11) DEFAULT NULL COMMENT '��� ��������',
  `WhoTo` int(11) DEFAULT NULL COMMENT '��� �������',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='��������: ���������������� ������';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Fo_Doc_Shift`
--

LOCK TABLES `Fo_Doc_Shift` WRITE;
/*!40000 ALTER TABLE `Fo_Doc_Shift` DISABLE KEYS */;
/*!40000 ALTER TABLE `Fo_Doc_Shift` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Fo_Doc_Shift_Table_Ware`
--

DROP TABLE IF EXISTS `Fo_Doc_Shift_Table_Ware`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Fo_Doc_Shift_Table_Ware` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Parent_ID` int(11) DEFAULT NULL,
  `Wares_ID` int(11) NOT NULL,
  `Qty` double(15,3) NOT NULL COMMENT '���������� ������',
  `Price` double(15,3) NOT NULL COMMENT '���������� ������',
  `Sum` double(15,3) NOT NULL COMMENT '�����',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='���.�����: ������\r\n��������: �����������';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Fo_Doc_Shift_Table_Ware`
--

LOCK TABLES `Fo_Doc_Shift_Table_Ware` WRITE;
/*!40000 ALTER TABLE `Fo_Doc_Shift_Table_Ware` DISABLE KEYS */;
/*!40000 ALTER TABLE `Fo_Doc_Shift_Table_Ware` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Fo_Doc_SurMinus`
--

DROP TABLE IF EXISTS `Fo_Doc_SurMinus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Fo_Doc_SurMinus` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Store_ID` int(11) NOT NULL COMMENT '��� ������',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='��������: �������� ������';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Fo_Doc_SurMinus`
--

LOCK TABLES `Fo_Doc_SurMinus` WRITE;
/*!40000 ALTER TABLE `Fo_Doc_SurMinus` DISABLE KEYS */;
/*!40000 ALTER TABLE `Fo_Doc_SurMinus` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Fo_Doc_SurMinus_Table_Ware`
--

DROP TABLE IF EXISTS `Fo_Doc_SurMinus_Table_Ware`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Fo_Doc_SurMinus_Table_Ware` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Parent_ID` int(11) DEFAULT NULL,
  `Wares_ID` int(11) NOT NULL,
  `Unit_ID` int(11) DEFAULT NULL COMMENT '������� ���������',
  `Factor` double(15,3) DEFAULT NULL COMMENT '����������',
  `Qty` double(15,3) NOT NULL,
  `Price` double(15,3) NOT NULL,
  `Sum` double(15,3) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='���.�����: ������\r\n��������: �������� ������ (Fo_Doc_SurMinu';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Fo_Doc_SurMinus_Table_Ware`
--

LOCK TABLES `Fo_Doc_SurMinus_Table_Ware` WRITE;
/*!40000 ALTER TABLE `Fo_Doc_SurMinus_Table_Ware` DISABLE KEYS */;
/*!40000 ALTER TABLE `Fo_Doc_SurMinus_Table_Ware` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Fo_Doc_SurPlus`
--

DROP TABLE IF EXISTS `Fo_Doc_SurPlus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Fo_Doc_SurPlus` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Store_ID` int(11) NOT NULL COMMENT '��� ������',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='��������: ��������� ������� ������';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Fo_Doc_SurPlus`
--

LOCK TABLES `Fo_Doc_SurPlus` WRITE;
/*!40000 ALTER TABLE `Fo_Doc_SurPlus` DISABLE KEYS */;
/*!40000 ALTER TABLE `Fo_Doc_SurPlus` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Fo_Doc_SurPlus_Table_Ware`
--

DROP TABLE IF EXISTS `Fo_Doc_SurPlus_Table_Ware`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Fo_Doc_SurPlus_Table_Ware` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Parent_ID` int(11) DEFAULT NULL,
  `Wares_ID` int(11) NOT NULL,
  `Unit_ID` int(11) DEFAULT NULL COMMENT '������� ���������',
  `Factor` double(15,3) NOT NULL DEFAULT '1.000' COMMENT '����������',
  `Qty` double(15,3) NOT NULL,
  `Price` double(15,3) NOT NULL,
  `Sum` double(15,3) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='���.�����: ������\r\n��������: ������������� ������ (Fo_Doc_Su';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Fo_Doc_SurPlus_Table_Ware`
--

LOCK TABLES `Fo_Doc_SurPlus_Table_Ware` WRITE;
/*!40000 ALTER TABLE `Fo_Doc_SurPlus_Table_Ware` DISABLE KEYS */;
/*!40000 ALTER TABLE `Fo_Doc_SurPlus_Table_Ware` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Fo_Enum`
--

DROP TABLE IF EXISTS `Fo_Enum`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Fo_Enum` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `SubGroup_ID` int(11) NOT NULL COMMENT '��� ���������',
  `Deleted` tinyint(1) DEFAULT '0',
  `Symbol` varchar(8) NOT NULL COMMENT '�������������',
  `ShortName` varchar(16) NOT NULL,
  `Name` varchar(32) DEFAULT NULL,
  `Description` tinytext,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8 COMMENT='����������: �����';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Fo_Enum`
--

LOCK TABLES `Fo_Enum` WRITE;
/*!40000 ALTER TABLE `Fo_Enum` DISABLE KEYS */;
INSERT INTO `Fo_Enum` VALUES (1,1,NULL,'','��.','�����',NULL),(2,1,NULL,'','��','�������',NULL),(3,1,NULL,'','��','����',NULL),(4,1,NULL,'','��','����',NULL),(5,2,NULL,'','���','�������',NULL),(6,2,NULL,'','��','�����',NULL),(7,3,NULL,'','�����',NULL,NULL),(8,3,NULL,'','�������',NULL,NULL),(9,3,NULL,'','���������',NULL,NULL),(10,4,NULL,'','���','����������',NULL),(11,4,NULL,'','���','�����',NULL),(12,5,NULL,'','���','����',NULL),(13,5,NULL,'','�����','������',NULL),(16,5,0,'reserv','������','������',NULL);
/*!40000 ALTER TABLE `Fo_Enum` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Fo_Meta`
--

DROP TABLE IF EXISTS `Fo_Meta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Fo_Meta` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Type` enum('Doc','Ref','Enum') NOT NULL,
  `Deleted` tinyint(1) NOT NULL DEFAULT '0',
  `TableName` varchar(32) NOT NULL,
  `Description` text,
  UNIQUE KEY `ID` (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COMMENT='����������';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Fo_Meta`
--

LOCK TABLES `Fo_Meta` WRITE;
/*!40000 ALTER TABLE `Fo_Meta` DISABLE KEYS */;
INSERT INTO `Fo_Meta` VALUES (1,'Doc',0,'Fo_Doc_IntegrationMinus',NULL),(2,'Doc',0,'Fo_Doc_IntegrationPlus',NULL);
/*!40000 ALTER TABLE `Fo_Meta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Fo_Ref`
--

DROP TABLE IF EXISTS `Fo_Ref`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Fo_Ref` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Deleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT '������� �� ��������',
  `IsGroup` tinyint(1) NOT NULL COMMENT '������� ������ ��� �������',
  `Ref` int(11) NOT NULL,
  `Order` int(11) DEFAULT NULL COMMENT '������� � ������',
  `Code` int(11) NOT NULL COMMENT '���������� ���. ���������� �������������',
  `Name` varchar(128) CHARACTER SET cp1251 NOT NULL,
  `ShortName` varchar(32) CHARACTER SET cp1251 DEFAULT NULL,
  `Description` text CHARACTER SET cp1251,
  `Image` varchar(64) CHARACTER SET cp1251 DEFAULT NULL COMMENT '���� � �������',
  `DateCreate` datetime DEFAULT NULL,
  `DateModify` datetime DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Fo_Ref`
--

LOCK TABLES `Fo_Ref` WRITE;
/*!40000 ALTER TABLE `Fo_Ref` DISABLE KEYS */;
INSERT INTO `Fo_Ref` VALUES (1,0,1,1,NULL,1,'Ivanov Name',NULL,NULL,NULL,NULL,NULL),(2,0,1,2,NULL,21,'Petrov Name',NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `Fo_Ref` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Fo_RefM_BankAccount`
--

DROP TABLE IF EXISTS `Fo_RefM_BankAccount`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Fo_RefM_BankAccount` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Parent_ID` int(11) DEFAULT NULL COMMENT '��� �������� �����������',
  `ParentExt_ID` int(11) DEFAULT NULL COMMENT '����� �����������',
  `Bank_ID` int(11) NOT NULL COMMENT '��� �����',
  `Currency_ID` int(11) NOT NULL COMMENT '��� ������',
  `Account` varchar(32) DEFAULT NULL COMMENT '��������� ����',
  `DateBegin` date DEFAULT NULL COMMENT '���� �������� �����',
  `DateExpired` date DEFAULT NULL COMMENT '���� �������� �����',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='����������: ���������� �����';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Fo_RefM_BankAccount`
--

LOCK TABLES `Fo_RefM_BankAccount` WRITE;
/*!40000 ALTER TABLE `Fo_RefM_BankAccount` DISABLE KEYS */;
/*!40000 ALTER TABLE `Fo_RefM_BankAccount` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Fo_Ref_Address`
--

DROP TABLE IF EXISTS `Fo_Ref_Address`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Fo_Ref_Address` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `ZIP` varchar(8) DEFAULT '' COMMENT '�������� ������',
  `Country_ID` int(11) DEFAULT NULL,
  `Region` varchar(32) DEFAULT NULL COMMENT '������',
  `Town` varchar(32) DEFAULT NULL COMMENT '�����',
  `Street` varchar(32) DEFAULT NULL COMMENT '�����',
  `House` varchar(32) DEFAULT NULL COMMENT '���',
  `Flat` varchar(8) DEFAULT NULL COMMENT '����',
  `Porch` varchar(8) DEFAULT NULL COMMENT '�������',
  `Secret` varchar(8) DEFAULT NULL COMMENT '��� �����',
  `Latitude` double(15,6) DEFAULT NULL,
  `Longitude` double(15,6) DEFAULT NULL,
  `Hint` varchar(64) DEFAULT NULL COMMENT '���',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='����������: ������';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Fo_Ref_Address`
--

LOCK TABLES `Fo_Ref_Address` WRITE;
/*!40000 ALTER TABLE `Fo_Ref_Address` DISABLE KEYS */;
/*!40000 ALTER TABLE `Fo_Ref_Address` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Fo_Ref_Asset`
--

DROP TABLE IF EXISTS `Fo_Ref_Asset`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Fo_Ref_Asset` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Producer_ID` int(11) DEFAULT NULL COMMENT '��� �������������',
  `Country_ID` int(11) DEFAULT NULL COMMENT '������ �������������',
  `Price` decimal(11,0) DEFAULT NULL COMMENT '������� ����',
  `WorkNumber` varchar(16) DEFAULT NULL COMMENT '��������� �����',
  `PassNumber` varchar(16) DEFAULT NULL COMMENT '����� ��������',
  `Model` int(11) DEFAULT NULL COMMENT '������',
  `DateRelease` int(11) DEFAULT NULL COMMENT '���� �������',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='����������: �������� ��������';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Fo_Ref_Asset`
--

LOCK TABLES `Fo_Ref_Asset` WRITE;
/*!40000 ALTER TABLE `Fo_Ref_Asset` DISABLE KEYS */;
/*!40000 ALTER TABLE `Fo_Ref_Asset` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Fo_Ref_Bank`
--

DROP TABLE IF EXISTS `Fo_Ref_Bank`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Fo_Ref_Bank` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `BIC` int(11) NOT NULL COMMENT '��� ',
  `Address` varchar(32) DEFAULT NULL COMMENT '����� ',
  `Manager` varchar(32) DEFAULT NULL COMMENT '���������� ����, �������',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='����������: �����';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Fo_Ref_Bank`
--

LOCK TABLES `Fo_Ref_Bank` WRITE;
/*!40000 ALTER TABLE `Fo_Ref_Bank` DISABLE KEYS */;
/*!40000 ALTER TABLE `Fo_Ref_Bank` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Fo_Ref_Country`
--

DROP TABLE IF EXISTS `Fo_Ref_Country`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Fo_Ref_Country` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='����������: ������';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Fo_Ref_Country`
--

LOCK TABLES `Fo_Ref_Country` WRITE;
/*!40000 ALTER TABLE `Fo_Ref_Country` DISABLE KEYS */;
/*!40000 ALTER TABLE `Fo_Ref_Country` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Fo_Ref_Currency`
--

DROP TABLE IF EXISTS `Fo_Ref_Currency`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Fo_Ref_Currency` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Period_Rate` decimal(15,4) DEFAULT NULL COMMENT '������������� ��������. ���� ������',
  `Presentation` varchar(4) DEFAULT NULL COMMENT '������ ���� ''$''',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='����������: ������';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Fo_Ref_Currency`
--

LOCK TABLES `Fo_Ref_Currency` WRITE;
/*!40000 ALTER TABLE `Fo_Ref_Currency` DISABLE KEYS */;
/*!40000 ALTER TABLE `Fo_Ref_Currency` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Fo_Ref_Currency_Period_Rate`
--

DROP TABLE IF EXISTS `Fo_Ref_Currency_Period_Rate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Fo_Ref_Currency_Period_Rate` (
  `ID` int(11) NOT NULL,
  `OnDate` datetime NOT NULL COMMENT '����',
  `Value` decimal(15,4) DEFAULT NULL COMMENT '�������� �� ����',
  PRIMARY KEY (`ID`,`OnDate`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='������������� ��������: ���� ������';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Fo_Ref_Currency_Period_Rate`
--

LOCK TABLES `Fo_Ref_Currency_Period_Rate` WRITE;
/*!40000 ALTER TABLE `Fo_Ref_Currency_Period_Rate` DISABLE KEYS */;
/*!40000 ALTER TABLE `Fo_Ref_Currency_Period_Rate` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Fo_Ref_Customer`
--

DROP TABLE IF EXISTS `Fo_Ref_Customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Fo_Ref_Customer` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Personal_ID` int(11) DEFAULT NULL COMMENT '������ ���.����',
  `Address_ID` int(11) DEFAULT NULL COMMENT '�����',
  `Juridical_ID` int(11) DEFAULT NULL COMMENT '����� ������������',
  `Enum_Type` int(11) NOT NULL COMMENT '��� �����������. �����������,���������� ����',
  `TaxCode` varchar(12) DEFAULT NULL COMMENT '��������� ���',
  `Director_ID` int(11) DEFAULT NULL COMMENT '�������� (Personal_ID)',
  `Bugalter_ID` int(11) DEFAULT NULL COMMENT '��������� (Personal_ID)',
  `Manager_ID` int(11) DEFAULT NULL COMMENT '�������� (Personal_ID)',
  `DiscountCard_ID` int(11) DEFAULT NULL COMMENT '�������� ������',
  `Emploee_ID` int(11) DEFAULT NULL COMMENT '������������ ��������� �� ������������',
  `Contract_ID` int(11) DEFAULT NULL COMMENT '�������',
  `Login` varchar(16) DEFAULT NULL COMMENT '��� ������� ����� www',
  `Password` varchar(16) DEFAULT NULL COMMENT '������ ������� ����� www',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COMMENT='����������: �����������';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Fo_Ref_Customer`
--

LOCK TABLES `Fo_Ref_Customer` WRITE;
/*!40000 ALTER TABLE `Fo_Ref_Customer` DISABLE KEYS */;
INSERT INTO `Fo_Ref_Customer` VALUES (1,NULL,NULL,NULL,2,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(2,NULL,NULL,NULL,2,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `Fo_Ref_Customer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Fo_Ref_Customer_BindGrp`
--

DROP TABLE IF EXISTS `Fo_Ref_Customer_BindGrp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Fo_Ref_Customer_BindGrp` (
  `IDI` int(11) NOT NULL,
  `IDG` int(11) NOT NULL,
  PRIMARY KEY (`IDI`,`IDG`),
  KEY `IDG` (`IDG`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='������: ����������� � �� ������ ';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Fo_Ref_Customer_BindGrp`
--

LOCK TABLES `Fo_Ref_Customer_BindGrp` WRITE;
/*!40000 ALTER TABLE `Fo_Ref_Customer_BindGrp` DISABLE KEYS */;
/*!40000 ALTER TABLE `Fo_Ref_Customer_BindGrp` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Fo_Ref_Customer_Table_Contract`
--

DROP TABLE IF EXISTS `Fo_Ref_Customer_Table_Contract`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Fo_Ref_Customer_Table_Contract` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Parent_ID` int(11) DEFAULT NULL,
  `DateBegin` date DEFAULT NULL,
  `DateExpired` date DEFAULT NULL,
  `Discount` decimal(11,0) DEFAULT NULL COMMENT '������� ������',
  `DaysDelay` int(11) DEFAULT NULL COMMENT '�������� ������� � ����',
  `Credit` double(15,3) DEFAULT NULL COMMENT '������������ ����� �������',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='����������: ������';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Fo_Ref_Customer_Table_Contract`
--

LOCK TABLES `Fo_Ref_Customer_Table_Contract` WRITE;
/*!40000 ALTER TABLE `Fo_Ref_Customer_Table_Contract` DISABLE KEYS */;
/*!40000 ALTER TABLE `Fo_Ref_Customer_Table_Contract` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Fo_Ref_DiscountCard`
--

DROP TABLE IF EXISTS `Fo_Ref_DiscountCard`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Fo_Ref_DiscountCard` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `CardCode` varchar(13) NOT NULL,
  `DateLastModified` datetime DEFAULT NULL,
  `DateLastUse` datetime DEFAULT NULL,
  `NumberOfUse` int(11) NOT NULL DEFAULT '0',
  `Sum` decimal(11,0) DEFAULT NULL,
  `Printed` tinyint(4) NOT NULL DEFAULT '0',
  `Status` tinyint(4) NOT NULL DEFAULT '1',
  PRIMARY KEY (`ID`),
  UNIQUE KEY `discount_card_code` (`CardCode`),
  UNIQUE KEY `CardCode` (`CardCode`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='����������: ������ ������';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Fo_Ref_DiscountCard`
--

LOCK TABLES `Fo_Ref_DiscountCard` WRITE;
/*!40000 ALTER TABLE `Fo_Ref_DiscountCard` DISABLE KEYS */;
/*!40000 ALTER TABLE `Fo_Ref_DiscountCard` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Fo_Ref_Emploee`
--

DROP TABLE IF EXISTS `Fo_Ref_Emploee`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Fo_Ref_Emploee` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Position_ID` int(11) NOT NULL COMMENT '���������',
  `Address_ID` int(11) DEFAULT NULL COMMENT '�����',
  `Personal_ID` int(11) DEFAULT NULL COMMENT '������ ������',
  `DateIn` date NOT NULL,
  `DateOut` date NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='����������: ����������';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Fo_Ref_Emploee`
--

LOCK TABLES `Fo_Ref_Emploee` WRITE;
/*!40000 ALTER TABLE `Fo_Ref_Emploee` DISABLE KEYS */;
/*!40000 ALTER TABLE `Fo_Ref_Emploee` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Fo_Ref_Emploee_BindGrp`
--

DROP TABLE IF EXISTS `Fo_Ref_Emploee_BindGrp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Fo_Ref_Emploee_BindGrp` (
  `IDI` int(11) NOT NULL,
  `IDG` int(11) NOT NULL,
  PRIMARY KEY (`IDI`,`IDG`),
  KEY `IDG` (`IDG`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='������: ���������� � �� ������ ';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Fo_Ref_Emploee_BindGrp`
--

LOCK TABLES `Fo_Ref_Emploee_BindGrp` WRITE;
/*!40000 ALTER TABLE `Fo_Ref_Emploee_BindGrp` DISABLE KEYS */;
/*!40000 ALTER TABLE `Fo_Ref_Emploee_BindGrp` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Fo_Ref_Emploee_Period_Position`
--

DROP TABLE IF EXISTS `Fo_Ref_Emploee_Period_Position`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Fo_Ref_Emploee_Period_Position` (
  `ID` int(11) NOT NULL,
  `OnDate` datetime NOT NULL COMMENT '����',
  `Value` decimal(15,4) DEFAULT NULL COMMENT '�������� �� ����',
  PRIMARY KEY (`ID`,`OnDate`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='������������� ��������: ���� ������';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Fo_Ref_Emploee_Period_Position`
--

LOCK TABLES `Fo_Ref_Emploee_Period_Position` WRITE;
/*!40000 ALTER TABLE `Fo_Ref_Emploee_Period_Position` DISABLE KEYS */;
/*!40000 ALTER TABLE `Fo_Ref_Emploee_Period_Position` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Fo_Ref_Juridical`
--

DROP TABLE IF EXISTS `Fo_Ref_Juridical`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Fo_Ref_Juridical` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='����������: ����� ������������ (���, ���...)';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Fo_Ref_Juridical`
--

LOCK TABLES `Fo_Ref_Juridical` WRITE;
/*!40000 ALTER TABLE `Fo_Ref_Juridical` DISABLE KEYS */;
/*!40000 ALTER TABLE `Fo_Ref_Juridical` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Fo_Ref_OurFirm`
--

DROP TABLE IF EXISTS `Fo_Ref_OurFirm`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Fo_Ref_OurFirm` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Address_ID` int(11) DEFAULT NULL COMMENT '�����',
  `TaxCode` varchar(12) DEFAULT NULL COMMENT '��������� ���',
  `Director_ID` int(11) DEFAULT NULL COMMENT '��������, �������',
  `Bugalter_ID` int(11) DEFAULT NULL COMMENT '���������, �������',
  `ManagerID` int(11) DEFAULT NULL COMMENT '��������, �������',
  `Cashier_ID` int(11) DEFAULT NULL,
  `Store_ID` int(11) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='����������: ���� �����';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Fo_Ref_OurFirm`
--

LOCK TABLES `Fo_Ref_OurFirm` WRITE;
/*!40000 ALTER TABLE `Fo_Ref_OurFirm` DISABLE KEYS */;
/*!40000 ALTER TABLE `Fo_Ref_OurFirm` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Fo_Ref_Personal`
--

DROP TABLE IF EXISTS `Fo_Ref_Personal`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Fo_Ref_Personal` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Enum_Gender` int(11) NOT NULL,
  `DOB` date NOT NULL DEFAULT '0000-00-00',
  `FirstName` varchar(32) NOT NULL DEFAULT '',
  `LastName` varchar(32) NOT NULL DEFAULT '',
  `MiddleName` varchar(32) NOT NULL,
  `Phone` varchar(32) NOT NULL DEFAULT '',
  `eMail` varchar(32) NOT NULL DEFAULT '',
  `ICQ` varchar(16) NOT NULL DEFAULT '',
  `Passport` varchar(32) DEFAULT NULL,
  `www` varchar(32) DEFAULT NULL COMMENT '�������� ��������',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='����������: ������������ ������';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Fo_Ref_Personal`
--

LOCK TABLES `Fo_Ref_Personal` WRITE;
/*!40000 ALTER TABLE `Fo_Ref_Personal` DISABLE KEYS */;
/*!40000 ALTER TABLE `Fo_Ref_Personal` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Fo_Ref_Position`
--

DROP TABLE IF EXISTS `Fo_Ref_Position`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Fo_Ref_Position` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='����������: ���������';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Fo_Ref_Position`
--

LOCK TABLES `Fo_Ref_Position` WRITE;
/*!40000 ALTER TABLE `Fo_Ref_Position` DISABLE KEYS */;
/*!40000 ALTER TABLE `Fo_Ref_Position` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Fo_Ref_Producer`
--

DROP TABLE IF EXISTS `Fo_Ref_Producer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Fo_Ref_Producer` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Address_ID` int(11) DEFAULT NULL,
  `www` varchar(16) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='����������: �������������';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Fo_Ref_Producer`
--

LOCK TABLES `Fo_Ref_Producer` WRITE;
/*!40000 ALTER TABLE `Fo_Ref_Producer` DISABLE KEYS */;
/*!40000 ALTER TABLE `Fo_Ref_Producer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Fo_Ref_Store`
--

DROP TABLE IF EXISTS `Fo_Ref_Store`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Fo_Ref_Store` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Enum_Type` int(11) NOT NULL,
  `FIFO` tinyint(1) NOT NULL DEFAULT '1',
  `Responsible_ID` int(11) DEFAULT NULL COMMENT '������������� �� ������',
  `Address_ID` int(11) DEFAULT NULL,
  `Phone` varchar(16) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='����������: ������';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Fo_Ref_Store`
--

LOCK TABLES `Fo_Ref_Store` WRITE;
/*!40000 ALTER TABLE `Fo_Ref_Store` DISABLE KEYS */;
/*!40000 ALTER TABLE `Fo_Ref_Store` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Fo_Ref_Stores_BindGrp`
--

DROP TABLE IF EXISTS `Fo_Ref_Stores_BindGrp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Fo_Ref_Stores_BindGrp` (
  `IDI` int(11) NOT NULL,
  `IDG` int(11) NOT NULL,
  PRIMARY KEY (`IDI`,`IDG`),
  KEY `IDG` (`IDG`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='������: ������ � �� ������ ';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Fo_Ref_Stores_BindGrp`
--

LOCK TABLES `Fo_Ref_Stores_BindGrp` WRITE;
/*!40000 ALTER TABLE `Fo_Ref_Stores_BindGrp` DISABLE KEYS */;
/*!40000 ALTER TABLE `Fo_Ref_Stores_BindGrp` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Fo_Ref_User`
--

DROP TABLE IF EXISTS `Fo_Ref_User`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Fo_Ref_User` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Emploee_ID` int(11) DEFAULT NULL COMMENT '���������',
  `Deny` tinyint(1) DEFAULT '0' COMMENT '������ ��������',
  `DateBegin` date NOT NULL,
  `DateExpired` date NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='����������: ����������';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Fo_Ref_User`
--

LOCK TABLES `Fo_Ref_User` WRITE;
/*!40000 ALTER TABLE `Fo_Ref_User` DISABLE KEYS */;
/*!40000 ALTER TABLE `Fo_Ref_User` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Fo_Ref_Ware`
--

DROP TABLE IF EXISTS `Fo_Ref_Ware`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Fo_Ref_Ware` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Markup` int(11) DEFAULT NULL COMMENT '�����������',
  `Producer_ID` int(11) DEFAULT NULL COMMENT '��� �������������',
  `Country_ID` int(11) DEFAULT NULL COMMENT '������ �������������',
  `Price_ID` int(11) DEFAULT NULL,
  `Articul` varchar(16) DEFAULT NULL COMMENT '�������',
  `Sertificate` varchar(16) DEFAULT NULL COMMENT '����������',
  `IsPuplic` tinyint(1) DEFAULT '1' COMMENT '���������� � �����-�����',
  `IsWeight` tinyint(1) DEFAULT NULL COMMENT '������� ��� �������',
  `IsDenyDiscount` tinyint(1) DEFAULT '0' COMMENT '��������� ������ � ��������� ����������',
  `IsExcise` tinyint(1) DEFAULT '0' COMMENT '�����',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='����������: ������';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Fo_Ref_Ware`
--

LOCK TABLES `Fo_Ref_Ware` WRITE;
/*!40000 ALTER TABLE `Fo_Ref_Ware` DISABLE KEYS */;
/*!40000 ALTER TABLE `Fo_Ref_Ware` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Fo_Ref_Ware_BindGrp`
--

DROP TABLE IF EXISTS `Fo_Ref_Ware_BindGrp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Fo_Ref_Ware_BindGrp` (
  `IDI` int(11) NOT NULL,
  `IDG` int(11) NOT NULL,
  PRIMARY KEY (`IDI`,`IDG`),
  KEY `IDG` (`IDG`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='������: ������ � �� ������ ';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Fo_Ref_Ware_BindGrp`
--

LOCK TABLES `Fo_Ref_Ware_BindGrp` WRITE;
/*!40000 ALTER TABLE `Fo_Ref_Ware_BindGrp` DISABLE KEYS */;
/*!40000 ALTER TABLE `Fo_Ref_Ware_BindGrp` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Fo_Ref_Ware_Table_Lot`
--

DROP TABLE IF EXISTS `Fo_Ref_Ware_Table_Lot`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Fo_Ref_Ware_Table_Lot` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Parent_ID` int(11) DEFAULT NULL COMMENT '��� ��������',
  `Doc_ID` int(11) NOT NULL,
  `Price` decimal(11,0) DEFAULT NULL,
  `DateDoc` datetime DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='����������: ������';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Fo_Ref_Ware_Table_Lot`
--

LOCK TABLES `Fo_Ref_Ware_Table_Lot` WRITE;
/*!40000 ALTER TABLE `Fo_Ref_Ware_Table_Lot` DISABLE KEYS */;
/*!40000 ALTER TABLE `Fo_Ref_Ware_Table_Lot` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Fo_Ref_Ware_Table_Price`
--

DROP TABLE IF EXISTS `Fo_Ref_Ware_Table_Price`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Fo_Ref_Ware_Table_Price` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Parent_ID` int(11) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='����������: ����';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Fo_Ref_Ware_Table_Price`
--

LOCK TABLES `Fo_Ref_Ware_Table_Price` WRITE;
/*!40000 ALTER TABLE `Fo_Ref_Ware_Table_Price` DISABLE KEYS */;
/*!40000 ALTER TABLE `Fo_Ref_Ware_Table_Price` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Fo_Ref_Ware_Table_Reserve`
--

DROP TABLE IF EXISTS `Fo_Ref_Ware_Table_Reserve`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Fo_Ref_Ware_Table_Reserve` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Parent_ID` int(11) DEFAULT NULL COMMENT '��� ��������',
  `Store_ID` int(11) NOT NULL,
  `Minimum` double(15,3) DEFAULT NULL COMMENT '�����������',
  `Maximum` double(15,3) DEFAULT NULL COMMENT '���',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='����������: �����������-������������ ����� �� ������';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Fo_Ref_Ware_Table_Reserve`
--

LOCK TABLES `Fo_Ref_Ware_Table_Reserve` WRITE;
/*!40000 ALTER TABLE `Fo_Ref_Ware_Table_Reserve` DISABLE KEYS */;
/*!40000 ALTER TABLE `Fo_Ref_Ware_Table_Reserve` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Fo_Ref_Ware_Table_Similar`
--

DROP TABLE IF EXISTS `Fo_Ref_Ware_Table_Similar`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Fo_Ref_Ware_Table_Similar` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Parent_ID` int(11) DEFAULT NULL COMMENT '��� ��������',
  `Ware_ID` int(11) DEFAULT NULL COMMENT '�����',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='����������: ������� �����';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Fo_Ref_Ware_Table_Similar`
--

LOCK TABLES `Fo_Ref_Ware_Table_Similar` WRITE;
/*!40000 ALTER TABLE `Fo_Ref_Ware_Table_Similar` DISABLE KEYS */;
/*!40000 ALTER TABLE `Fo_Ref_Ware_Table_Similar` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Fo_Ref_Ware_Table_Unit`
--

DROP TABLE IF EXISTS `Fo_Ref_Ware_Table_Unit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Fo_Ref_Ware_Table_Unit` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Parent_ID` int(11) DEFAULT NULL COMMENT '��� ��������',
  `Enum_Type` int(11) NOT NULL COMMENT '������������. ������� ���������',
  `Factor` double(15,3) DEFAULT NULL COMMENT '�����������',
  `Weight` double(15,3) DEFAULT NULL COMMENT '���',
  `Length` double(15,3) DEFAULT NULL COMMENT '������',
  `Width` double(15,3) DEFAULT NULL COMMENT '������',
  `Height` double(15,3) DEFAULT NULL COMMENT '������',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='����������: ������� ���������';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Fo_Ref_Ware_Table_Unit`
--

LOCK TABLES `Fo_Ref_Ware_Table_Unit` WRITE;
/*!40000 ALTER TABLE `Fo_Ref_Ware_Table_Unit` DISABLE KEYS */;
/*!40000 ALTER TABLE `Fo_Ref_Ware_Table_Unit` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary table structure for view `VDoc_DocInventory`
--

DROP TABLE IF EXISTS `VDoc_DocInventory`;
/*!50001 DROP VIEW IF EXISTS `VDoc_DocInventory`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `VDoc_DocInventory` (
  `Deleted` tinyint NOT NULL,
  `DocChild_ID` tinyint NOT NULL,
  `Firm` tinyint NOT NULL,
  `Code` tinyint NOT NULL,
  `Description` tinyint NOT NULL,
  `DateCreate` tinyint NOT NULL,
  `DateModify` tinyint NOT NULL,
  `DateDoc` tinyint NOT NULL,
  `BasedOn_ID` tinyint NOT NULL,
  `ID` tinyint NOT NULL,
  `Store_ID` tinyint NOT NULL,
  `Chairman_ID` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Final view structure for view `VDoc_DocInventory`
--

/*!50001 DROP TABLE IF EXISTS `VDoc_DocInventory`*/;
/*!50001 DROP VIEW IF EXISTS `VDoc_DocInventory`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`front_office`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `VDoc_DocInventory` AS select `T1`.`Deleted` AS `Deleted`,`T1`.`DocChild_ID` AS `DocChild_ID`,`T1`.`Firm` AS `Firm`,`T1`.`Code` AS `Code`,`T1`.`Description` AS `Description`,`T1`.`DateCreate` AS `DateCreate`,`T1`.`DateModify` AS `DateModify`,`T1`.`DateDoc` AS `DateDoc`,`T1`.`BasedOn_ID` AS `BasedOn_ID`,`T2`.`ID` AS `ID`,`T2`.`Store_ID` AS `Store_ID`,`T2`.`Chairman_ID` AS `Chairman_ID` from (`Fo_Doc` `T1` join `Fo_Doc_Inventory` `T2`) where (`T1`.`DocChild_ID` = `T2`.`ID`) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2012-10-28 20:08:33
