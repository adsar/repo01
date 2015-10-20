--keyword query

create temp view corpus as
	select * from frequency
	union select 'q' as docid, 'washington' as term, 1 as count
	union select 'q' as docid, 'taxes' as term, 1 as count
	union select 'q' as docid, 'treasury' as term, 1 as count;
	

select 'echo ' || cast(s.value as text) || ' > part_i.txt' from	
	-- Similarity Matrix (not normalized) of all documents in matrix corpus
        (select docid_row, docid_col, sum(v) as [value] from
		(select a.docid as [docid_row], b.docid as [docid_col], a.count * b.count as [v]
			from corpus a
			join corpus b
			on a.term = b.term
			where a.docid < b.docid) c
	group by docid_row, docid_col) s
where docid_row='q' or docid_col='q'
order by s.value desc
limit 20;	
