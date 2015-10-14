

public class Selector2 implements PivotSelector {
	public int selectPivot(Integer[] a, int s, int e) {
		swap(a, s, e-1);
		return s;
	}
	
	private static void swap(Integer[] a, int x, int y) {
		int temp = a[x];
		a[x] = a[y];
		a[y] = temp;	
	}
}
