
public class QuickSort {
	
	// returns comps count
	public long Sort(Integer[] a, int s, int e, PivotSelector sel) {
		long n = e - s;
		
		// base case (n = 1)
		if (n <= 1) return 0;
		
		// Partition
		int i = partition(a, s, e, sel);
		
		// the pivot is in its final position, position a[i-1], now sort the sub-arrays at both sides
		
		long left_count = Sort(a, s, i-1, sel);
		long right_count = Sort(a, i, e, sel);
		
		return (n - 1) + left_count + right_count;
	}

	private int partition(Integer[] a, int s, int e, PivotSelector sel) {
		int p = sel.selectPivot(a, s, e);
		int pivot = a[p];
		int i = p + 1;
		
		for (int j=p+1; j<e; j++) {
			if (a[j] < pivot) {
				swap(a, i, j);
				i ++;
			}
		}
		
		swap(a, p, i-1);
		return i;
	}
	
	private void swap(Integer[] a, int x, int y) {
		int temp = a[x];
		a[x] = a[y];
		a[y] = temp;	
	}

}
