/*
 Navicat Premium Data Transfer

 Source Server         : settingdb
 Source Server Type    : SQLite
 Source Server Version : 3008004
 Source Database       : main

 Target Server Type    : SQLite
 Target Server Version : 3008004
 File Encoding         : utf-8

 Date: 09/24/2015 09:03:29 AM
*/

PRAGMA foreign_keys = false;

-- ----------------------------
--  Table structure for setting
-- ----------------------------
DROP TABLE IF EXISTS "setting";
CREATE TABLE "setting" (
	 "id" int,
	 "key" varchar(50,0) NOT NULL,
	 "value" varchar(2000,0),
	 "comments" varchar(500,0),
	PRIMARY KEY("id")
);

-- ----------------------------
--  Records of setting
-- ----------------------------
BEGIN;
INSERT INTO "setting" VALUES (1, 'common_setting', 'common_setting', '通用站点');
INSERT INTO "setting" VALUES (2, 'proxies', 'proxies', '代理列表');
INSERT INTO "setting" VALUES (3, 'keywords', 'keywords', '关键字');
INSERT INTO "setting" VALUES (4, 'bloger', 'bloger', '博主');
COMMIT;

PRAGMA foreign_keys = true;
