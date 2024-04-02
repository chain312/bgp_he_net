/*
Navicat MySQL Data Transfer

Source Server         : 127.0.0.1
Source Server Version : 50726
Source Host           : localhost:3306
Source Database       : bgp_he

Target Server Type    : MYSQL
Target Server Version : 50726
File Encoding         : 65001

Date: 2024-03-30 15:39:26
*/

SET FOREIGN_KEY_CHECKS=0;
CREATE DATABASE IF NOT EXISTS bgp_he;
USE bgp_he;
-- ----------------------------
-- Table structure for as_details
-- ----------------------------
DROP TABLE IF EXISTS `as_details`;
CREATE TABLE `as_details` (
  `ASN` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `Prefix` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `Description` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `flag` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `type` int(11) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci ROW_FORMAT=DYNAMIC;

-- ----------------------------
-- Table structure for as_info
-- ----------------------------
DROP TABLE IF EXISTS `as_info`;
CREATE TABLE `as_info` (
  `Prefixes_Originated_all` int(11) DEFAULT NULL,
  `Prefixes_Originated_v4` int(11) DEFAULT NULL,
  `Prefixes_Originated_v6` int(11) DEFAULT NULL,
  `Prefixes_Announced_all` int(11) DEFAULT NULL,
  `Prefixes_Announced_v4` int(11) DEFAULT NULL,
  `Prefixes_Announced_v6` int(11) DEFAULT NULL,
  `ASN` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci ROW_FORMAT=DYNAMIC;

-- ----------------------------
-- Table structure for country
-- ----------------------------
DROP TABLE IF EXISTS `country`;
CREATE TABLE `country` (
  `ASN` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `Name` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `Adjacencies_v4` int(11) DEFAULT NULL,
  `Routes_v4` int(11) DEFAULT NULL,
  `Adjacencies_v6` int(11) DEFAULT NULL,
  `Routes_v6` int(11) DEFAULT NULL,
  `Crawled` int(11) DEFAULT NULL,
  PRIMARY KEY (`ASN`) USING BTREE
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci ROW_FORMAT=DYNAMIC;

-- ----------------------------
-- Table structure for report_world
-- ----------------------------
DROP TABLE IF EXISTS `report_world`;
CREATE TABLE `report_world` (
  `Description` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `CC` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `ASNs` int(11) NOT NULL,
  `CC1` varchar(255) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci ROW_FORMAT=DYNAMIC;
