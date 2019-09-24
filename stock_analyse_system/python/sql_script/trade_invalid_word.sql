/*
Navicat MySQL Data Transfer

Source Server         : my
Source Server Version : 50725
Source Host           : localhost:3306
Source Database       : test

Target Server Type    : MYSQL
Target Server Version : 50725
File Encoding         : 65001

Date: 2019-09-24 18:23:00
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `trade_invalid_word`
-- ----------------------------
DROP TABLE IF EXISTS `trade_invalid_word`;
CREATE TABLE `trade_invalid_word` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `invalid_word` varchar(64) DEFAULT NULL COMMENT '无效字符串',
  PRIMARY KEY (`id`),
  UNIQUE KEY `invalid_word` (`invalid_word`)
) ENGINE=InnoDB AUTO_INCREMENT=48 DEFAULT CHARSET=utf8 COMMENT='词云图无效词汇过滤';

-- ----------------------------
-- Records of trade_invalid_word
-- ----------------------------
INSERT INTO `trade_invalid_word` VALUES ('20', 'A股');
INSERT INTO `trade_invalid_word` VALUES ('44', '上证');
INSERT INTO `trade_invalid_word` VALUES ('19', '个股');
INSERT INTO `trade_invalid_word` VALUES ('28', '也许');
INSERT INTO `trade_invalid_word` VALUES ('45', '亿元');
INSERT INTO `trade_invalid_word` VALUES ('3', '今天');
INSERT INTO `trade_invalid_word` VALUES ('18', '但是');
INSERT INTO `trade_invalid_word` VALUES ('15', '出现');
INSERT INTO `trade_invalid_word` VALUES ('8', '分析');
INSERT INTO `trade_invalid_word` VALUES ('17', '午后');
INSERT INTO `trade_invalid_word` VALUES ('26', '发稿');
INSERT INTO `trade_invalid_word` VALUES ('21', '可以');
INSERT INTO `trade_invalid_word` VALUES ('5', '大盘');
INSERT INTO `trade_invalid_word` VALUES ('10', '如果');
INSERT INTO `trade_invalid_word` VALUES ('33', '家数');
INSERT INTO `trade_invalid_word` VALUES ('24', '就是');
INSERT INTO `trade_invalid_word` VALUES ('14', '左右');
INSERT INTO `trade_invalid_word` VALUES ('34', '已经');
INSERT INTO `trade_invalid_word` VALUES ('4', '市场');
INSERT INTO `trade_invalid_word` VALUES ('25', '截至');
INSERT INTO `trade_invalid_word` VALUES ('9', '所以');
INSERT INTO `trade_invalid_word` VALUES ('2', '指数');
INSERT INTO `trade_invalid_word` VALUES ('16', '操作');
INSERT INTO `trade_invalid_word` VALUES ('47', '新浪');
INSERT INTO `trade_invalid_word` VALUES ('32', '时报');
INSERT INTO `trade_invalid_word` VALUES ('6', '板块');
INSERT INTO `trade_invalid_word` VALUES ('13', '概率');
INSERT INTO `trade_invalid_word` VALUES ('22', '没有');
INSERT INTO `trade_invalid_word` VALUES ('29', '现在');
INSERT INTO `trade_invalid_word` VALUES ('35', '股份');
INSERT INTO `trade_invalid_word` VALUES ('1', '行情');
INSERT INTO `trade_invalid_word` VALUES ('31', '证券');
INSERT INTO `trade_invalid_word` VALUES ('46', '财经');
INSERT INTO `trade_invalid_word` VALUES ('7', '资金');
INSERT INTO `trade_invalid_word` VALUES ('12', '趋势');
INSERT INTO `trade_invalid_word` VALUES ('27', '还是');
INSERT INTO `trade_invalid_word` VALUES ('11', '这个');
