select 'echo ' || cast(s.value as text) || ' > part_h.txt' from	
	-- Similarity Matrix of all documents in matrix frequency
        (select docid_row, docid_col, sum(v) as [value] from
	(select a.docid as [docid_row], b.docid as [docid_col], a.count * b.count as [v]
		from frequency a
		join frequency b
		on a.term = b.term
		where a.docid < b.docid
		and docid_row='10080_txt_crude' and docid_col='17035_txt_earn' -- optimization: pushing down selects reduces the size of intermediate results
	) c
	group by docid_row, docid_col) s
where docid_row='10080_txt_crude' and docid_col='17035_txt_earn';	
