# Pearl
Hi, 这是一个使用python编写的, 自研的大数据sql解析框架, 力图将大数据组件中的sql, 如hive sql, flink sql和spark sql等解析成AST, 以供sql语句校验, sql字段提取使用.
其实更酷的是, 我想到了一个大数据的应用场景: 数据仓库血缘关系文档的自动生成! 理论上, 只要我知道了数仓ETL的所有sql语句, 
我就可以通过这些sql语句解析出每一个表的每一个字段在整个数据仓库中的生命周期链路! 血缘关系文档的自动生成也就成了一件可以完成的事情!
目前暂时只支持flink sql, 还有很多功能没有完善, 继续加油吧!!!

Hi, this is a bigdata sql parsing framework written in python, which is aiming to parse bigdata sql, like hive sql, flink sql and spark sql etc. into ast.
so that we can use it to verify our sql or extract the output colums.
you know what, this is very useful if you want to auto generate the consanguinity relation document of your bigdata warehouse! In theories, as long as I have all the sqls
of my DW etl jobs, I am able to know the entire lifecycle of every column of every table in the data warehouse, which making it possible!
but currently, this framework just support flink sql and there are still many things to do, hope me well done then!!!
