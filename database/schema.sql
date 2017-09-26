drop table if exists calculos;
create table calculos (
  id integer primary key autoincrement,
  session text not null,
  input text,
  output text
  );