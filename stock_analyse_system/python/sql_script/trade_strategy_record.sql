/*
Navicat MySQL Data Transfer

Source Server         : my
Source Server Version : 50725
Source Host           : localhost:3306
Source Database       : test

Target Server Type    : MYSQL
Target Server Version : 50725
File Encoding         : 65001

Date: 2019-10-08 18:17:16
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `trade_strategy_record`
-- ----------------------------
DROP TABLE IF EXISTS `trade_strategy_record`;
CREATE TABLE `trade_strategy_record` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `stock_name` varchar(64) DEFAULT NULL COMMENT '股票名称',
  `stock_code` varchar(12) DEFAULT NULL COMMENT '股票代码',
  `current_price` decimal(10,4) DEFAULT NULL COMMENT '当前价格',
  `current_rate` decimal(10,4) DEFAULT NULL COMMENT '当前涨幅',
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  `strategy_category` tinyint(3) DEFAULT NULL COMMENT '策略类别 1 竞价选股  2 雪球组合',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8 COMMENT='策略选股记录表';

-- ----------------------------
-- Records of trade_strategy_record
-- ----------------------------
INSERT INTO `trade_strategy_record` VALUES ('1', '光大银行', 'SH601818', '4.0900', '3.8100', '2019-10-08 00:00:00', '2019-10-08 00:00:00', '1');
INSERT INTO `trade_strategy_record` VALUES ('2', '光大银行', 'SH601818', '4.0900', '3.8100', '2019-10-08 18:10:55', '2019-10-08 18:10:55', '1');
INSERT INTO `trade_strategy_record` VALUES ('3', '光大银行', 'SH601818', '4.0900', '3.8100', '2019-10-08 18:15:46', '2019-10-08 18:15:46', '1');
INSERT INTO `trade_strategy_record` VALUES ('4', '平安银行', 'SZ000001', '16.2000', '3.9100', '2019-10-08 18:15:58', '2019-10-08 18:15:58', '1');
INSERT INTO `trade_strategy_record` VALUES ('5', '兴业银行', 'SH601166', '17.9600', '2.4500', '2019-10-08 18:16:00', '2019-10-08 18:16:00', '1');
INSERT INTO `trade_strategy_record` VALUES ('6', '金冠股份', 'SZ300510', '8.5800', '3.8700', '2019-10-08 18:16:02', '2019-10-08 18:16:02', '1');
INSERT INTO `trade_strategy_record` VALUES ('7', '南京银行', 'SH601009', '8.7800', '2.2100', '2019-10-08 18:16:04', '2019-10-08 18:16:04', '1');
INSERT INTO `trade_strategy_record` VALUES ('8', '正邦科技', 'SZ002157', '15.5600', '2.9800', '2019-10-08 18:16:06', '2019-10-08 18:16:06', '1');
