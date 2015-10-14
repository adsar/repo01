public class Selector3 implements PivotSelector {
	public int selectPivot(Integer[] a, int s, int e) {
		int central = (s + e - 1) / 2;
		int median = 0;
		
		int min = a[s];
		if (a[central] < min) min = a[central];
		if (a[e-1] < min) min = a[e-1];
		
		int max = a[s];
		if (a[central] > max) max = a[central];
		if (a[e-1] > max) max = a[e-1];
		
		if(a[s] != min && a[s] != max) median = s;
		else if(a[central] != min && a[central] != max) median = central;
		else if(a[e-1] != min && a[e-1] != max) median = e-1;

		swap(a, s, median);
		return s;
	}
	
	private static void swap(Integer[] a, int x, int y) {
		int temp = a[x];
		a[x] = a[y];
		a[y] = temp;	
	}	
}

