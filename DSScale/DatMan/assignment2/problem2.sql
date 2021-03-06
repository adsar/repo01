select 'echo ' || cast(d.value as text) || ' > part_g.txt' from
	-- Matrix Multiplication
       (select row_num, col_num, sum(v) as [value]
	from	(select a.row_num, b.col_num, a.value * b.value as [v]
		from a
		join b
		on a.col_num = b.row_num) c
	group by row_num, col_num) d
where row_num=2 and col_num=3;
