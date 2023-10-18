create table person (
	id	int,
	name varchar,
	height	int,
	birthplace	int,
	devilFruit int,
	words varchar,
	pict varchar
);

create table devilFruit (
	id int, 
	name varchar,
	ability varchar
);

create table pirate (
	id int,
	person_id int, 
	pirateGroup_id int, 
	bounty int
);

create table pirateGroup (
	id int, 
	captainid int,
	name varchar
); 

create table navy (
	id int,
	person_id int,
	class_id int, 
	base_id int
);

create table location (
	id int, 
	name varchar
);

create table class (
	id int, 
	name varchar
);

create table base (
	id int, 
	name varchar
);

create table LoginUser (
	username varchar,
	password varchar
);

insert into person select 1,'モンキー D ルフィー',120,0,1,"海賊王に俺はなる！",'1.png' where not exists (select id from person where id = 1);
insert into person select 2,'ドン・キホーテ ドフラミンゴ',6000,6,2,"勝者だけが正義だ","2.png" where not exists (select id from person where id = 2);
insert into person select 3,'ベビー5',500, 2,3,"わかった 喜んで死ぬわ！ それで役に立てるなら",'3.png' where not exists (select id from person where id = 3);
insert into person select 4,'バギー',130, 6,4,"俺がこの世で興味あるものは、お宝と酒だけだ",'4.png' where not exists (select id from person where id = 4);
insert into person select 5,'Mr.3',170, 1,5,"私がMr.3だとばれてしまうガネっ！",'5.png' where not exists (select id from person where id = 5);
insert into person select 6,'シャンクス',700,6,0,"この戦争を終わらせに来た",'6.png' where not exists (select id from person where id = 6);
insert into person select 7, 'ボルサリーノ', 500, 3, 6, "速度は…“重さ” “光”の速度で蹴られた事はあるかい",'7.png' where not exists (select id from person where id = 7);
insert into person select 8, 'コビー', 200, 1, 0, "僕でもなれるでしょうか", "8.png" where not exists (select id from person where id = 8);
insert into person select 9, 'サカズキ', 800, 1, 7, "先の時代の敗北者じゃけぇ", "9.png" where not exists (select id from person where id = 9);


insert into devilFruit values (0, "なし", "なし");
insert into devilFruit values (1, "ゴムゴムの実", "体がゴム人間になる");
insert into devilFruit values (2, "イトイトの実", "糸を自在に操れるようになる");
insert into devilFruit values (3, "ブキブキの実", "体を武器に変えられるようになる");
insert into devilFruit values (4, "バラバラの実", "体をバラバラにできる");
insert into devilFruit values (5, "ドルドルの実", "体が蝋のようになる");
insert into devilFruit values (6, "ピカピカの実", "光人間になる");
insert into devilFruit values (7, "マグマグの実", "マグマ人間になる");


insert into pirateGroup values (0, 0, "無所属");
insert into pirateGroup values (1, 1, "麦わらの一味");
insert into pirateGroup values (2, 2, "ドン・キホーテ海賊団");
insert into pirateGroup values (3, 4, "クロスギルド");
insert into pirateGroup values (4, 6, "赤髪海賊団");

insert into pirate values (1,1,1, 999999);
insert into pirate values (2,2,2, 999999);
insert into pirate values (3,3,2, 999999);
insert into pirate values (4,4,3, 999999);
insert into pirate values (5,5,3, 999999);
insert into pirate values (6,6,4, 999999);

insert into navy values (1, 7, 1, 6);
insert into navy values (2, 8, 4, 6);
insert into navy values (3, 9, 1, 3);


insert into location values (0, "不明");
insert into location values (1, "ノースブルー");
insert into location values (2, "サウスブルー");
insert into location values (3, "イーストブルー");
insert into location values (4, "ウェストブルー");
insert into location values (5, "マリージョア");
insert into location values (6, "グランドライン");

insert into class values (0, "不明");
INSERT INTO class VALUES (1, "元帥");
INSERT INTO class VALUES (2, "大将");
INSERT INTO class VALUES (3, "中将");
INSERT INTO class VALUES (4, "少将");
INSERT INTO class VALUES (5, "准将");
INSERT INTO class VALUES (6, "大佐");
INSERT INTO class VALUES (7, "中佐");
INSERT INTO class VALUES (8, "少佐");


insert into base values (0, "不明");
insert into base values (1, "G5");
insert into base values (2, "マリンフォード");
insert into base values (3, "SWORD");
insert into base values (4, "第16支部");
insert into base values (5, "第153支部");
insert into base values (6, "本部");

