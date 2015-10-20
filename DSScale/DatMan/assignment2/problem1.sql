select 'echo ' || cast(count(*) as text) || ' > part_a.txt' from (
	select * 
	from frequency
	where docid='10398_txt_earn'
) a;

select 'echo ' || cast(count(*) as text) || ' > part_b.txt' from (
	select term
	from frequency
	where docid='10398_txt_earn' and count=1
) b;


select 'echo ' || cast(count(*) as text) || ' > part_c.txt' from (
	select term 
	from frequency
	where docid='10398_txt_earn' and count=1
union	select term
	from frequency
	where docid='925_txt_trade' and count=1
) c;


select 'echo ' || cast(count(*) as text) || ' > part_d.txt' from (
	select distinct docid
	from frequency
	where lower(term)='law' or lower(term)='legal'
) d;



select 'echo ' || cast(count(*) as text) || ' > part_e.txt' from (
	select * from 
		(select count(*) as dsize   -- changed to match grader error:  sum(*) (with duplicates) to count(*) unique terms
		from frequency
		group by docid) x
	where dsize>300
) e;


select 'echo ' || cast(count(*) as text) || ' > part_f.txt' from (
	select T.docid
	from (select distinct docid
		from frequency
		where lower(term)='transactions') T
	join (select distinct docid
		from frequency
		where lower(term)='world') W
	on T.docid = W.docid
) f;

