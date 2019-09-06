/*
Navicat MySQL Data Transfer

Source Server         : my
Source Server Version : 50725
Source Host           : localhost:3306
Source Database       : test

Target Server Type    : MYSQL
Target Server Version : 50725
File Encoding         : 65001

Date: 2019-09-06 17:07:21
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `trade_word_nephogram`
-- ----------------------------
DROP TABLE IF EXISTS `trade_word_nephogram`;
CREATE TABLE `trade_word_nephogram` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `begin_time` varchar(16) NOT NULL COMMENT '开始时间',
  `end_time` varchar(16) NOT NULL COMMENT '结束时间',
  `picture_name` varchar(16) NOT NULL COMMENT '图片名称',
  PRIMARY KEY (`id`,`picture_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='新浪大盘评论词云图地址';

-- ----------------------------
-- Records of trade_word_nephogram
-- ----------------------------
